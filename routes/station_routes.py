from flask import Blueprint, render_template, request, redirect, session
from models.db import get_db
from ai.recommender import recommend_station
from blockchain.payment import process_payment

station_bp = Blueprint("station", __name__)

# ===============================
# OWNER: ADD CHARGING STATION
# ===============================
@station_bp.route("/owner/add-station", methods=["GET", "POST"])
def add_station():
    if session.get("role") != "owner":
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        chargers = int(request.form["chargers"])
        price = float(request.form["price"])
        green_score = int(request.form["green_score"])
        owner_id = session.get("user_id")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO stations (name, location, chargers, price, green_score, owner_id, approved)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (name, location, chargers, price, green_score, owner_id))
        conn.commit()
        conn.close()

        return redirect("/owner/stations")

    return render_template("owner_add_station.html")


# ===============================
# OWNER: VIEW OWN STATIONS
# ===============================
@station_bp.route("/owner/stations")
def owner_stations():
    if session.get("role") != "owner":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, location, chargers, price, green_score
        FROM stations
        WHERE owner_id=?
    """, (session.get("user_id"),))
    stations = cur.fetchall()
    conn.close()

    return render_template("owner_stations.html", stations=stations)


# ===============================
# USER: VIEW ALL STATIONS
# ===============================
@station_bp.route("/user/stations")
def user_stations():
    if session.get("role") != "user":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, location, chargers, price, green_score
        FROM stations
        WHERE approved = 1
        ORDER BY name ASC
    """)

    stations = cur.fetchall()
    conn.close()

    return render_template("user_stations.html", stations=stations)


# ===============================
# USER: AI RECOMMENDATION
# ===============================
@station_bp.route("/user/recommend", methods=["GET", "POST"])
def recommend():
    if session.get("role") != "user":
        return redirect("/login")

    if request.method == "POST":
        battery = int(request.form["battery"])
        distance = int(request.form["distance"])

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT name, location, chargers, price, green_score
            FROM stations
        """)
        stations = cur.fetchall()
        conn.close()

        best_station = recommend_station(battery, distance, stations)

        return render_template("recommend_result.html", station=best_station)

    return render_template("recommend_form.html")


# ===============================
# USER: CHARGE STATION (WITH QUEUE)
# ===============================
@station_bp.route("/user/charge/<station_name>", methods=["GET", "POST"])
def charge_station(station_name):
    if session.get("role") != "user":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    # Prevent blacklisted users from starting charging
    cur.execute("SELECT blacklisted FROM users WHERE id=?", (session.get('user_id'),))
    b = cur.fetchone()
    if b and b[0]:
        conn.close()
        return "Account is blacklisted"

    # Get total chargers
    cur.execute(
        "SELECT chargers FROM stations WHERE name=?",
        (station_name,)
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return "Station not found"

    total_chargers = row[0]

    # Count active sessions
    cur.execute(
        "SELECT COUNT(*) FROM charging_sessions WHERE station_name=? AND status='Active'",
        (station_name,)
    )
    active_sessions = cur.fetchone()[0]

    # ===============================
    # IF STATION FULL → ADD TO QUEUE
    # ===============================
    if active_sessions >= total_chargers:
        # Prevent duplicate queue entry
        cur.execute("""
            SELECT COUNT(*) FROM waiting_queue
            WHERE station_name=? AND user_id=?
        """, (station_name, session.get("user_id")))
        already_queued = cur.fetchone()[0]

        if already_queued == 0:
            cur.execute("""
                INSERT INTO waiting_queue (station_name, user_id)
                VALUES (?, ?)
            """, (station_name, session.get("user_id")))
            conn.commit()

        # Get queue position
        cur.execute("""
            SELECT COUNT(*)
            FROM waiting_queue
            WHERE station_name=?
              AND joined_at <= (
                SELECT joined_at FROM waiting_queue
                WHERE station_name=? AND user_id=?
                ORDER BY joined_at ASC
                LIMIT 1
              )
        """, (station_name, station_name, session.get("user_id")))

        position = cur.fetchone()[0]
        conn.close()

        return render_template(
            "queue_status.html",
            station_name=station_name,
            position=position
        )

    # ===============================
    # START CHARGING
    # ===============================
    if request.method == "POST":
        units = float(request.form["units"])
        price = float(request.form["price"])
        amount = units * price

        payment = process_payment(amount)

        cur.execute("""
            INSERT INTO charging_sessions
            (user_id, station_name, units, amount, tx_hash, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session.get("user_id"),
            station_name,
            units,
            amount,
            payment["tx_hash"],
            "Active"
        ))

        conn.commit()
        conn.close()

        return redirect("/user/history")

    conn.close()
    return render_template("charge_form.html", station_name=station_name)


# ===============================
# USER: COMPLETE CHARGING
# ===============================
@station_bp.route("/user/complete/<int:session_id>")
def complete_charging(session_id):
    if session.get("role") != "user":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    # Get station name
    cur.execute(
        "SELECT station_name FROM charging_sessions WHERE id=?",
        (session_id,)
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return redirect("/user/history")

    station_name = row[0]

    # Mark session completed
    cur.execute(
        "UPDATE charging_sessions SET status='Completed' WHERE id=?",
        (session_id,)
    )

    # Remove first user from queue (FIFO)
    cur.execute("""
        DELETE FROM waiting_queue
        WHERE id = (
            SELECT id FROM waiting_queue
            WHERE station_name=?
            ORDER BY joined_at ASC
            LIMIT 1
        )
    """, (station_name,))

    conn.commit()
    conn.close()

    return redirect("/user/history")


# ===============================
# USER: CHECK QUEUE STATUS (API)
# ===============================
@station_bp.route("/api/queue-status/<station_name>")
def check_queue_status(station_name):
    """
    API endpoint to check if user can now charge
    Returns JSON with queue position and availability
    """
    if session.get("role") != "user":
        return {"error": "Unauthorized"}, 403

    conn = get_db()
    cur = conn.cursor()

    # Get total chargers
    cur.execute(
        "SELECT chargers FROM stations WHERE name=?",
        (station_name,)
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return {"error": "Station not found"}, 404

    total_chargers = row[0]

    # Count active sessions
    cur.execute(
        "SELECT COUNT(*) FROM charging_sessions WHERE station_name=? AND status='Active'",
        (station_name,)
    )
    active_sessions = cur.fetchone()[0]

    # Check if user is still in queue
    cur.execute("""
        SELECT COUNT(*) FROM waiting_queue
        WHERE station_name=? AND user_id=?
    """, (station_name, session.get("user_id")))
    in_queue = cur.fetchone()[0]

    if not in_queue:
        conn.close()
        return {"error": "Not in queue"}, 400

    # Get queue position
    cur.execute("""
        SELECT COUNT(*)
        FROM waiting_queue
        WHERE station_name=?
          AND joined_at <= (
            SELECT joined_at FROM waiting_queue
            WHERE station_name=? AND user_id=?
            ORDER BY joined_at ASC
            LIMIT 1
          )
    """, (station_name, station_name, session.get("user_id")))

    position = cur.fetchone()[0]

    # Check if slot is available (position is 1 or less and not all chargers are in use)
    can_charge = position <= 1 and active_sessions < total_chargers

    conn.close()

    return {
        "position": position,
        "active_sessions": active_sessions,
        "total_chargers": total_chargers,
        "can_charge": can_charge
    }


# ===============================# USER: CHARGING HISTORY
# ===============================
@station_bp.route("/user/history")
def charging_history():
    if session.get("role") != "user":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, station_name, units, amount, tx_hash, status, started_at, completed_at
        FROM charging_sessions
        WHERE user_id=?
        ORDER BY id DESC
    """, (session.get("user_id"),))
    history = cur.fetchall()
    conn.close()

    return render_template("charging_history.html", history=history)


# ===============================
# USER: STOP/COMPLETE CHARGING
# ===============================
@station_bp.route("/user/stop-charging/<int:session_id>", methods=["POST"])
def stop_charging(session_id):
    if session.get("role") != "user":
        return {"error": "Unauthorized"}, 403

    conn = get_db()
    cur = conn.cursor()

    # Verify this is the user's session
    cur.execute("""
        SELECT id, station_name, status FROM charging_sessions
        WHERE id=? AND user_id=?
    """, (session_id, session.get("user_id")))
    
    session_data = cur.fetchone()
    if not session_data:
        conn.close()
        return {"error": "Session not found"}, 404

    session_id_check, station_name, current_status = session_data

    if current_status != "Active":
        conn.close()
        return {"error": "Only active sessions can be stopped"}, 400

    # Compute duration and ensure amount is recorded, then mark as completed
    from datetime import datetime
    # Fetch start time, units and existing amount
    cur.execute("SELECT started_at, units, amount, station_name FROM charging_sessions WHERE id=?", (session_id,))
    info = cur.fetchone()
    started_at, units, existing_amount, station = info

    # Parse started_at (SQLite default format: YYYY-MM-DD HH:MM:SS)
    def parse_ts(ts):
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts)
        except Exception:
            from datetime import datetime as _dt
            try:
                return _dt.strptime(ts.split('.')[0], "%Y-%m-%d %H:%M:%S")
            except Exception:
                return None

    start_dt = parse_ts(started_at)
    now = datetime.now()
    duration_minutes = None
    if start_dt:
        duration_minutes = int((now - start_dt).total_seconds() // 60)

    # If amount missing or zero, compute from station price
    amount_to_set = existing_amount
    if not existing_amount:
        cur.execute("SELECT price FROM stations WHERE name=?", (station,))
        r = cur.fetchone()
        price = r[0] if r else 0
        amount_to_set = units * price if units else 0

    cur.execute("""
        UPDATE charging_sessions 
        SET status='Completed', completed_at=?, duration_minutes=?, amount=?
        WHERE id=?
    """, (now, duration_minutes, amount_to_set, session_id))

    # Remove first user from queue (for next user)
    cur.execute("""
        DELETE FROM waiting_queue
        WHERE id = (
            SELECT id FROM waiting_queue
            WHERE station_name=?
            ORDER BY joined_at ASC
            LIMIT 1
        )
    """, (station_name,))

    conn.commit()
    conn.close()

    return {"status": "success", "message": "Charging stopped"}, 200


# ===============================
# OWNER: GET ACTIVE CHARGING SESSIONS
# ===============================
@station_bp.route("/owner/active-sessions")
def owner_active_sessions():
    if session.get("role") != "owner":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    # Get all stations owned by this owner
    cur.execute("""
        SELECT id, name FROM stations WHERE owner_id=?
    """, (session.get("user_id"),))
    
    owner_stations = cur.fetchall()
    station_ids = [s[0] for s in owner_stations]

    if not station_ids:
        conn.close()
        return render_template("owner_active_sessions.html", sessions=[])

    # Get active charging sessions for these stations
    placeholders = ','.join('?' * len(owner_stations))
    station_names = [s[1] for s in owner_stations]
    
    cur.execute(f"""
        SELECT cs.id, cs.user_id, cs.station_name, cs.units, cs.amount, 
               cs.status, cs.started_at, u.name, u.email
        FROM charging_sessions cs
        JOIN users u ON cs.user_id = u.id
        WHERE cs.station_name IN ({placeholders})
        AND cs.status = 'Active'
        ORDER BY cs.started_at DESC
    """, station_names)
    
    sessions = cur.fetchall()
    conn.close()

    return render_template("owner_active_sessions.html", sessions=sessions)


# ===============================
# OWNER: COMPLETE USER'S CHARGING
# ===============================
@station_bp.route("/owner/complete-charging/<int:session_id>", methods=["POST"])
def owner_complete_charging(session_id):
    if session.get("role") != "owner":
        return {"error": "Unauthorized"}, 403

    conn = get_db()
    cur = conn.cursor()

    # Get session and verify ownership
    cur.execute("""
        SELECT cs.id, cs.station_name, cs.status, s.owner_id
        FROM charging_sessions cs
        JOIN stations s ON cs.station_name = s.name
        WHERE cs.id=?
    """, (session_id,))
    
    session_data = cur.fetchone()
    if not session_data:
        conn.close()
        return {"error": "Session not found"}, 404

    session_id_check, station_name, status, owner_id = session_data

    if owner_id != session.get("user_id"):
        conn.close()
        return {"error": "Unauthorized"}, 403

    if status != "Active":
        conn.close()
        return {"error": "Only active sessions can be completed"}, 400

    # Compute duration and ensure amount is recorded, then mark as completed
    from datetime import datetime
    cur.execute("SELECT started_at, units, amount FROM charging_sessions WHERE id=?", (session_id,))
    info = cur.fetchone()
    started_at, units, existing_amount = info

    def parse_ts(ts):
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts)
        except Exception:
            from datetime import datetime as _dt
            try:
                return _dt.strptime(ts.split('.')[0], "%Y-%m-%d %H:%M:%S")
            except Exception:
                return None

    start_dt = parse_ts(started_at)
    now = datetime.now()
    duration_minutes = None
    if start_dt:
        duration_minutes = int((now - start_dt).total_seconds() // 60)

    amount_to_set = existing_amount
    if not existing_amount:
        cur.execute("SELECT price FROM stations WHERE name=?", (station_name,))
        r = cur.fetchone()
        price = r[0] if r else 0
        amount_to_set = units * price if units else 0

    cur.execute("""
        UPDATE charging_sessions 
        SET status='Completed', completed_at=?, duration_minutes=?, amount=?
        WHERE id=?
    """, (now, duration_minutes, amount_to_set, session_id))

    # Remove first user from queue
    cur.execute("""
        DELETE FROM waiting_queue
        WHERE id = (
            SELECT id FROM waiting_queue
            WHERE station_name=?
            ORDER BY joined_at ASC
            LIMIT 1
        )
    """, (station_name,))

    conn.commit()
    conn.close()

    return {"status": "success", "message": "Charging completed"}, 200


# ===============================
# OWNER: CANCEL USER'S CHARGING
# ===============================
@station_bp.route("/owner/cancel-charging/<int:session_id>", methods=["POST"])
def owner_cancel_charging(session_id):
    if session.get("role") != "owner":
        return {"error": "Unauthorized"}, 403

    conn = get_db()
    cur = conn.cursor()

    # Get session and verify ownership
    cur.execute("""
        SELECT cs.id, cs.station_name, cs.status, s.owner_id
        FROM charging_sessions cs
        JOIN stations s ON cs.station_name = s.name
        WHERE cs.id=?
    """, (session_id,))
    
    session_data = cur.fetchone()
    if not session_data:
        conn.close()
        return {"error": "Session not found"}, 404

    session_id_check, station_name, status, owner_id = session_data

    if owner_id != session.get("user_id"):
        conn.close()
        return {"error": "Unauthorized"}, 403

    # Mark as cancelled (set completed_at)
    from datetime import datetime
    cur.execute("SELECT started_at FROM charging_sessions WHERE id=?", (session_id,))
    started_at = cur.fetchone()[0]

    def parse_ts(ts):
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts)
        except Exception:
            from datetime import datetime as _dt
            try:
                return _dt.strptime(ts.split('.')[0], "%Y-%m-%d %H:%M:%S")
            except Exception:
                return None

    start_dt = parse_ts(started_at)
    now = datetime.now()
    duration_minutes = None
    if start_dt:
        duration_minutes = int((now - start_dt).total_seconds() // 60)

    cur.execute("""
        UPDATE charging_sessions 
        SET status='Cancelled', completed_at=?, duration_minutes=?
        WHERE id=?
    """, (now, duration_minutes, session_id))

    conn.commit()
    conn.close()

    return {"status": "success", "message": "Charging cancelled"}, 200
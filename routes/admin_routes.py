from flask import Blueprint, render_template, request, redirect, session
from models.db import get_db

admin_bp = Blueprint("admin", __name__)

# Admin Login
@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username, password)
        )
        admin = cur.fetchone()
        conn.close()

        if admin:
            session["admin_logged_in"] = True
            return redirect("/admin/dashboard")
        else:
            return "Invalid Admin Credentials"

    return render_template("admin_login.html")


# Admin Dashboard
@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM stations")
    total_stations = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM charging_sessions")
    total_sessions = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(amount), 0) FROM charging_sessions")
    total_revenue = cur.fetchone()[0]

    print("TOTAL USERS:", total_users)
    print("TOTAL STATIONS:", total_stations)
    print("TOTAL SESSIONS:", total_sessions)
    print("TOTAL REVENUE:", total_revenue)

    cur.execute("""
        SELECT station_name, units, amount, tx_hash, status
        FROM charging_sessions
    """)
    sessions = cur.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_stations=total_stations,
        total_sessions=total_sessions,
        total_revenue=total_revenue,
        sessions=sessions
    )



# Admin Logout
@admin_bp.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect("/admin/login")

from flask import Blueprint, render_template, request, redirect, session
from models.db import get_db
from ai.recommender import recommend_station
from blockchain.payment import process_payment

station_bp = Blueprint("station", __name__)

# Owner: Add charging station
@station_bp.route("/owner/add-station", methods=["GET", "POST"])
def add_station():
    if session.get("role") != "owner":
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        chargers = request.form["chargers"]
        price = request.form["price"]
        green_score = request.form["green_score"]
        owner_id = session.get("user_id")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO stations (name, location, chargers, price, green_score, owner_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, location, chargers, price, green_score, owner_id))
        conn.commit()
        conn.close()

        return redirect("/owner/stations")

    return render_template("owner_add_station.html")


# Owner: View own stations
@station_bp.route("/owner/stations")
def owner_stations():
    if session.get("role") != "owner":
        return redirect("/login")

    owner_id = session.get("user_id")
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT name, location, chargers, price, green_score FROM stations WHERE owner_id=?",
        (owner_id,)
    )
    stations = cur.fetchall()
    conn.close()

    return render_template("owner_stations.html", stations=stations)


# User: View all stations
@station_bp.route("/user/stations")
def user_stations():
    if session.get("role") != "user":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT name, location, chargers, price, green_score FROM stations"
    )
    stations = cur.fetchall()
    conn.close()

    return render_template("user_stations.html", stations=stations)


@station_bp.route("/user/recommend", methods=["GET", "POST"])
def recommend():
    if session.get("role") != "user":
        return redirect("/login")

    if request.method == "POST":
        battery = int(request.form["battery"])
        distance = int(request.form["distance"])

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT name, location, chargers, price, green_score FROM stations"
        )
        stations = cur.fetchall()
        conn.close()

        best_station = recommend_station(battery, distance, stations)

        return render_template(
            "recommend_result.html",
            station=best_station
        )
    
    

    return render_template("recommend_form.html")
@station_bp.route("/user/charge/<station_name>", methods=["GET", "POST"])
def charge_station(station_name):
    if session.get("role") != "user":
        return redirect("/login")

    if request.method == "POST":
        units = float(request.form["units"])
        price = float(request.form["price"])
        amount = units * price

        payment = process_payment(amount)

        conn = get_db()
        cur = conn.cursor()
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
            "Completed"
        ))
        conn.commit()
        conn.close()

        return redirect("/user/history")

    return render_template("charge_form.html", station_name=station_name)

@station_bp.route("/user/history")
def charging_history():
    if session.get("role") != "user":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT station_name, units, amount, tx_hash, status
        FROM charging_sessions
        WHERE user_id=?
    """, (session.get("user_id"),))
    history = cur.fetchall()
    conn.close()

    return render_template("charging_history.html", history=history)





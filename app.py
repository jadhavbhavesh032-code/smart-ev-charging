from flask import Flask, redirect, render_template, session
from models.db import init_db, get_db
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp 
from routes.station_routes import station_bp

app = Flask(__name__)
app.secret_key = "secret123"  # required for session

# Initialize DB
init_db()

# Pre-create admin
def create_admin():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )
        conn.commit()
    conn.close()

create_admin()

# Register blueprint
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp) 
app.register_blueprint(station_bp)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/user/dashboard")
def user_dashboard():
    if session.get("role") != "user":
        return redirect("/login")
    return render_template("user_dashboard.html")


@app.route("/owner/dashboard")
def owner_dashboard():
    if session.get("role") != "owner":
        return redirect("/login")
    return render_template("owner_dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)

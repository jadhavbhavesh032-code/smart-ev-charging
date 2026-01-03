import sqlite3
import os

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

def get_db():
    return sqlite3.connect("database/ev.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Admin table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # Users table (EV users + station owners)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # Charging stations table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        chargers INTEGER,
        price REAL,
        green_score INTEGER,
        owner_id INTEGER
    )
    """)
    # Charging sessions table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS charging_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        station_name TEXT,
        units REAL,
        amount REAL,
        tx_hash TEXT,
        status TEXT
    )
    """)


    

    conn.commit()
    conn.close()

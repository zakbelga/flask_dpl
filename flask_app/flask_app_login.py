#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import hashlib
from datetime import datetime

login_app = Flask(__name__)
login_app.secret_key = "your_secret_key"  # Needed for flashing messages

db_name = 'user.db'

# Utility function for database connection
def get_db_connection():
    return sqlite3.connect(db_name)

#### RE-INITIALIZING DATABASE => deleting all records from test database
@login_app.route('/delete/all', methods=['POST', 'DELETE'])
def delete_all():
    db_conn = get_db_connection()
    c = db_conn.cursor()
    c.execute("DELETE FROM USER_HASH;")
    db_conn.commit()
    db_conn.close()
    flash("All test records deleted.", "info")
    return redirect(url_for('index'))

#### SECURE SIGNUP
@login_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Database logic for creating a new account
        db_conn = sqlite3.connect(db_name)
        c = db_conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                      (username, email, password_hash))
            db_conn.commit()
            message = "Account created successfully!"
            # Redirect to login page after successful account creation
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            message = "Username already exists."
        finally:
            db_conn.close()
        
        return render_template('account.html', message=message)

    return render_template('account.html')

#### SECURE LOGIN
@login_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for('login'))

        db_conn = get_db_connection()
        c = db_conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username = ?;", (username,))
        record = c.fetchone()
        db_conn.close()
        
        if record and record[0] == hashlib.sha256(password.encode()).hexdigest():
            flash("Login successful!", "success")
            return redirect(url_for('account'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('login'))
    return render_template("login.html")

#### ROUTES FOR EACH TEMPLATE
@login_app.route('/')
def index():
    return render_template("index.html")

@login_app.route('/account')
def account():
    return render_template("account.html")

@login_app.route('/map')
def map_page():
    return render_template("map.html")

@login_app.route('/time')
def time_page():
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("time.html", datetime_now=datetime_now)

#### MAIN
if __name__ == "__main__":
    login_app.run(host="0.0.0.0", port=5555, debug=True)

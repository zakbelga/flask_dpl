# Add to this file for the Microweb app lab
from flask import Flask
from flask import request
from flask import render_template
import datetime

login_app = Flask(__name__)

@login_app.route("/")
def main():
    return render_template("index.html" , datetime_now = datetime.datetime.now())

@login_app.route("/time")
def time():
    return render_template("time.html")

@login_app.route("/map")
def map():
    return render_template("map.html")

@login_app.route("/login")
def login():
    return render_template("login.html")

@login_app.route("/account")
def account():
    return render_template("account.html")

if __name__ == "__main__":
    login_app.run(host="0.0.0.0", port=8802)
from app import app
from flask import render_template, request, redirect, session

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # check username and password
        session["username"] = username
        return redirect("/")

@app.route("/create_user", methods=["GET"])
def create_user():
    return render_template("create_user.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

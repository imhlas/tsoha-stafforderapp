from app import app
from flask import render_template, request, redirect, make_response, session
import products
import users
import orders

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("create_user.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/login")
        else:
            return render_template("error.html", message="Käyttäjätunnus on jo olemassa")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

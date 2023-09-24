from app import app
from flask import render_template, request, redirect, make_response
import products
import users

@app.route("/")
def index():
    return render_template("index.html", products=products.get_all_products())

@app.route('/show_image/<int:product_number>')
def show_image(product_number):
    data = products.get_image(product_number)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/png")
    return response

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
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/orders")
def orders():
    return render_template("orders.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

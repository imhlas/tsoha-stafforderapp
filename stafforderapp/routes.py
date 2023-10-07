from app import app
from flask import render_template, request, redirect, make_response, session
import products
import users
import orders

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

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form["product_id"]
    price = request.form["price"]
    order_id = orders.get_or_create_order(session["user_id"])

    if not orders.add_product_to_order(order_id, product_id, price):
        return render_template("error.html", message="Tuotteen lisääminen epäonnistui")
    else:
        return redirect("/")

@app.route("/orders")
def view_orders():
    if not session["user_id"]:
        return redirect("/")

    ordered_products = orders.get_current_order_details(session["user_id"])
    if not ordered_products:
        return render_template("orders.html",
                               products_list=[],
                               total_price=0,
                               total_quantity=0,
                               message="You have no active orders.")

    total_price = sum([product.price * product.quantity for product in ordered_products])
    total_quantity = sum([product.quantity for product in ordered_products])

    return render_template("orders.html",
                           products_list=ordered_products,
                           total_price=total_price,
                           total_quantity=total_quantity,
                           message=None)

@app.route("/delete_product", methods=["POST"])
def delete_product_from_order():
    order_detail_id = request.form["order_detail_id"]
    orders.delete_order_detail(order_detail_id)
    return redirect("/orders")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

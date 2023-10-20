from app import app
from flask import render_template, request, redirect, make_response, session
import orders, users

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    product_id = request.form["product_id"]
    price = request.form["price"]
    order_id = orders.get_or_create_order(session["user_id"])

    if not orders.add_product_to_order(order_id, product_id, price):
        return render_template("error.html", message="Tuotteen lisääminen epäonnistui")
    else:
        return redirect("/")

@app.route("/orders")
def view_orders():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")

    ordered_products, total_quantity, total_price = orders.get_current_order_details(user_id)
    if not ordered_products:
        return render_template("orders.html",
                               products_list=[],
                               total_price=0,
                               total_quantity=0,
                               message="You have no active orders.")

    return render_template("orders.html",
                           products_list=ordered_products,
                           total_price=total_price,
                           total_quantity=total_quantity,
                           message=None)

@app.route("/orders_admin")
def show_orders_admin():
    usernames = users.get_users_with_closed_orders()
    user_orders = {}
    total_user_data = {}

    for username in usernames:
        user_data, total_data = orders.get_closed_orders_for_user(username)
        user_orders[username] = user_data
        total_user_data[username] = total_data
    print(total_user_data)
    return render_template("orders_admin.html", user_orders=user_orders, total_user_data=total_user_data)

@app.route("/delete_product", methods=["POST"])
def delete_product_from_order():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    order_detail_id = request.form["order_detail_id"]
    orders.delete_order_detail(order_detail_id)
    return redirect("/orders")

@app.route("/end_order_time")
def end_order_time():
    if not orders.end_order_time():
        return render_template("error.html", message="Virhe tapahtumassa: SULJE TILAUSAIKA")
    else: 
        return redirect("/")

@app.route('/mark_billed', methods=['POST'])
def mark_billed():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    username = request.form.get('username')

    if orders.mark_order_as_billed(username):
        return redirect("/orders_admin")
    else:
        return render_template("error.html", message="Tilauksen merkitseminen laskutetuksi epäonnistui")


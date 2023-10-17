from app import app
from flask import render_template, request, redirect, make_response, session
import products, orders


@app.route("/")
def index():
    user_role = session.get("role")
    if user_role==1:
        active_orders = orders.get_active_orders()
        return render_template("admin.html", active_orders=active_orders)
    else:
        return render_template("index.html", products=products.get_all_products())

@app.route('/show_image/<int:product_number>')
def show_image(product_number):
    data = products.get_image(product_number)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route('/product_portfolio')
def show_products():
    user_role = session.get("role")
    if user_role == 1:
        products_list = products.get_all_products()
        total_quantity =  len(products_list)
        return render_template("admin_products.html",
                                products_list=products_list,
                                total_quantity=total_quantity)
    else:
        return redirect("/")

@app.route('/add_product', methods=["GET", "POST"])
def product_portfolio():
    if request.method == "GET":
        return render_template("admin_add_product.html")
    if request.method == "POST":
        name = request.form["name"]
        product_number = int(request.form["product_number"])
        price = request.form["price"]
        price = float(price.replace(",", "."))

        products.add_product(name, product_number, price)

        picture = request.files["file"]
        picture_name = picture.filename
        if not picture_name.endswith(".png"):
            return "Invalid filename"
        data = picture.read()
        products.add_picture(product_number, data)
    return redirect("/")

@app.route('/modify_or_delete_product/<int:product_number>', methods=['POST'])
def modify_or_delete_product(product_number):
    if request.form['action'] == 'modify':
        product_info = products.get_product_by_product_number(product_number)
        return render_template("modify_product_price.html",
                               product=product_info)
    elif request.form['action'] == 'delete':
        products.delete_product(product_number)
    return redirect("/product_portfolio")

@app.route('/update_price/<int:product_number>', methods=['POST'])
def update_price(product_number):
    price_text = request.form["new_price"]
    price = float(price_text.replace(",", "."))

    products.update_price(product_number, price)

    return redirect("/product_portfolio")

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
        return render_template("index.html", brands=products.get_all_brands())

@app.route('/brand/<int:brand_id>')
def brand_page(brand_id):
    return render_template('brand_page.html', products=products.get_products_for_brand(brand_id))


@app.route('/show_image/<int:product_number>')
def show_image(product_number):
    data = products.get_image(product_number)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route('/show_brand_image/<int:brand_id>')
def show_brand_image(brand_id):
    data = products.get_brand_image(brand_id)
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
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        brand = request.form["brand"]
        name = request.form["name"]
        product_number = int(request.form["product_number"])
        price = request.form["price"]
        price = float(price.replace(",", "."))

        picture = request.files["file"]
        picture_name = picture.filename
        if not picture_name.endswith(".png"):
            return render_template("error.html", message="Tiedoston pääte ei ole .png")
        data = picture.read()
        brand_id = products.get_brand_id(brand)
        if not brand_id >= 0:
            return render_template("error.html", message="Brändiä ei löydy")
        try:
            products.add_product(name, product_number, price)
            products.add_picture(product_number, data)
            return redirect("/")
        except:
            return render_template("error.html", message="Tuotteen lisääminen epäonnistui")

@app.route('/brand_product')
def add_brand_or_product():
    return render_template("brand_product.html")

@app.route('/add_brand', methods=["GET", "POST"])
def add_brand():
    if request.method == "GET":
        return render_template("admin_add_brand.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
    name = request.form["brand"]
    picture = request.files["file"]
    picture_name = picture.filename
    if not picture_name.endswith(".png"):
        return render_template("error.html", message="Tiedoston pääte ei ole .png")
    data = picture.read()
    try:
        products.add_brand(name, data)
        return redirect('/brand_product')
    except:
        return render_template("error.html", message="Brändin lisääminen epäonnistui")



@app.route('/modify_or_delete_product/<int:product_number>', methods=['POST'])
def modify_or_delete_product(product_number):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if request.form['action'] == 'modify':
        product_info = products.get_product_by_product_number(product_number)
        return render_template("modify_product_price.html",
                               product=product_info)
    elif request.form['action'] == 'delete':
        products.delete_product(product_number)
    return redirect("/product_portfolio")

@app.route('/update_price/<int:product_number>', methods=['POST'])
def update_price(product_number):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    price_text = request.form["new_price"]
    price = float(price_text.replace(",", "."))

    products.update_price(product_number, price)

    return redirect("/product_portfolio")

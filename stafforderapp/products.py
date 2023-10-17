from db import db

def get_all_products():
    sql = "SELECT * FROM products"
    return db.session.execute(sql).fetchall()

def get_product_by_product_number(product_number):
    sql = "SELECT * FROM products WHERE product_number=:product_number"
    result = db.session.execute(sql, {"product_number":product_number})
    return result.fetchone()

def get_image(product_number):
    sql = "SELECT data FROM images WHERE product_number=:product_number"
    result = db.session.execute(sql, {"product_number":product_number})
    return result.fetchone()[0]

def add_product(name, product_number, price):
    sql = "INSERT INTO products (name, price, product_number) VALUES (:name,:price,:product_number)"
    db.session.execute(sql, {"name":name, "price":price, "product_number":product_number})
    db.session.commit()

def add_picture(product_number, data):
    sql = "INSERT INTO images (product_number,data) VALUES (:product_number,:data)"
    db.session.execute(sql, {"product_number":product_number, "data":data})
    db.session.commit()

def delete_product(product_number):
    sql = "DELETE FROM products WHERE product_number = :product_number"
    db.session.execute(sql, {"product_number": product_number})
    db.session.commit()

def update_price(product_number, new_price):
    sql = "UPDATE products SET price = :new_price WHERE product_number = :product_number"
    db.session.execute(sql, {"new_price": new_price, "product_number": product_number})
    db.session.commit()

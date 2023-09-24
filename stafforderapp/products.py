from db import db

def get_all_products():
    sql = "SELECT * FROM products"
    return db.session.execute(sql).fetchall()

def get_image(product_number):
    sql = "SELECT data FROM images WHERE product_number=:product_number"
    result = db.session.execute(sql, {"product_number":product_number})
    return result.fetchone()[0]

from flask import session
from db import db

def get_or_create_order(user_id):
    sql = "SELECT id FROM orders WHERE user_id=:user_id AND order_status = 'Pending'"
    order = db.session.execute(sql, {"user_id": user_id}).fetchone()

    if order:
        return order[0]
    else:
        sql = "INSERT INTO orders (user_id, order_status) VALUES (:user_id, 'Pending') RETURNING id" 
        result = db.session.execute(sql, {"user_id": user_id})
        db.session.commit()
        new_order_id = result.fetchone()[0]
        return new_order_id

def add_product_to_order(order_id, product_id, price):
    try:
        sql = "INSERT INTO order_details (order_id, product_id, quantity, price) VALUES (:order_id, :product_id, 1, :price)"
        db.session.execute(sql, {"order_id": order_id, "product_id": product_id, "price": price})
        db.session.commit()
        return True
    except:
        return False

def get_current_order_details(user_id):
    sql = """
    SELECT OD.id, P.name, P.price, OD.quantity
    FROM order_details OD
    JOIN products P ON P.id = OD.product_id
    JOIN orders O ON O.id = OD.order_id
    WHERE O.user_id = :user_id AND O.order_status = 'Pending'
    """
    return db.session.execute(sql, {"user_id": user_id}).fetchall()

def delete_order_detail(order_detail_id):
    sql = """
    DELETE FROM order_details
    WHERE id = :order_detail_id
    """
    db.session.execute(sql, {"order_detail_id": order_detail_id})
    db.session.commit()

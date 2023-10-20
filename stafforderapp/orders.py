from flask import session
from datetime import datetime
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

def update_order_date(order_id):
    current_date = datetime.now().strftime("%d-%m-%Y")
    sql = "UPDATE orders SET order_date = :current_date WHERE id = :order_id"
    db.session.execute(sql, {"current_date": current_date, "order_id": order_id})

def add_product_to_order(order_id, product_id, price):
    try:
        sql = "INSERT INTO order_details (order_id, product_id, quantity, price) VALUES (:order_id, :product_id, 1, :price)"
        db.session.execute(sql, {"order_id": order_id, "product_id": product_id, "price": price})
        db.session.commit()
        update_order_date(order_id)
        return True
    except:
        return False

def get_active_orders():
    sql = "select COUNT(*) FROM orders WHERE order_status ='Pending'"
    result = db.session.execute(sql)
    return result.fetchone()[0]

def get_current_order_details(user_id):
    sql_order_details= """
    SELECT 
    OD.id AS id,
    P.name AS product_name,
    SUM(OD.quantity) AS prod_quantity,
    SUM(P.price * OD.quantity) AS prod_price
    FROM order_details OD
    JOIN products P ON P.id = OD.product_id
    JOIN orders O ON O.id = OD.order_id
    WHERE O.user_id = :user_id AND O.order_status = 'Pending'
    GROUP BY OD.id, P.name
    """

    sql_total = """
    SELECT SUM(OD.quantity) AS total_quantity, SUM(OD.price) AS total_price
    FROM order_details OD
    JOIN products P ON P.id = OD.product_id
    JOIN orders O ON O.id = OD.order_id
    WHERE O.user_id = :user_id AND O.order_status = 'Pending'
    """
    order_details = db.session.execute(sql_order_details, {"user_id": user_id}).fetchall()
    total_result = db.session.execute(sql_total, {"user_id": user_id}).fetchone()
    total_quantity = total_result['total_quantity']
    total_price = total_result['total_price']

    return order_details, total_quantity, total_price

def delete_order_detail(order_detail_id):
    sql = """
    DELETE FROM order_details
    WHERE id = :order_detail_id
    """
    db.session.execute(sql, {"order_detail_id": order_detail_id})
    db.session.commit()

def end_order_time():
    try:
        sql = "UPDATE orders SET order_status= 'Closed' WHERE order_status = 'Pending'"
        db.session.execute(sql)
        db.session.commit()
        return True
    except:
        return False

def get_closed_orders_for_user(username):
    user_query = """
    SELECT 
        P.name AS product_name,
        SUM(OD.quantity) AS total_quantity,
        SUM(OD.price) AS total_price
    FROM users U
    JOIN orders O ON U.id = O.user_id
    JOIN order_details OD ON O.id = OD.order_id
    JOIN products P ON OD.product_id = P.id
    WHERE U.name = :username
      AND O.order_status = 'Closed'
    GROUP BY P.name
    """

    total_user_query = """
    SELECT 
        SUM(OD.quantity) AS total_quantity_user,
        SUM(OD.price) AS total_price_user
    FROM users U
    JOIN orders O ON U.id = O.user_id
    JOIN order_details OD ON O.id = OD.order_id
    WHERE U.name = :username
      AND O.order_status = 'Closed'
    """

    user_data = db.session.execute(user_query, {"username": username}).fetchall()
    total_user_data = db.session.execute(total_user_query, {"username": username}).fetchall()

    return user_data, total_user_data

def mark_order_as_billed(username):
    try:
        sql = """
        UPDATE orders
        SET order_status = 'Billed'
        WHERE user_id IN (SELECT id FROM users WHERE name = :username)
        AND order_status = 'Closed'
        """

        db.session.execute(sql, {"username": username})
        db.session.commit()
        return True
    except:
        return False

from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db

def register(name, password, role=2):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, password, role) VALUES (:name, :password, :role)"
        db.session.execute(sql, {"name":name, "password":hash_value, "role": role})
        db.session.commit()
        return True
    except:
        return False

def login(name, password):
    sql = "SELECT id, password, role FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = name
            session["user_id"] = user.id
            session["role"] = user.role
            return True
        else:
            return False

def logout():
    del session["username"]
    del session["user_id"]
    del session["role"]

def get_users_with_closed_orders():
    sql = """
    SELECT DISTINCT U.name
    FROM users U
    JOIN orders O ON U.id = O.user_id
    WHERE O.order_status = 'Closed'
    """
    result = db.session.execute(sql).fetchall()
    usernames = [row[0] for row in result]

    return usernames

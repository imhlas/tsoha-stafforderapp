from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db

def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, password) VALUES (:name, :password)"
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False

def login(name, password):
    sql = "SELECT password FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = name
            return True
        else:
            return False

def logout():
    del session["username"]

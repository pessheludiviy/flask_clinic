import hashlib
from functools import wraps
from flask import session, redirect

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hash_):
    return hash_password(password) == hash_

def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            from flask import session, redirect
            if session.get("role") != role:
                return redirect("/")
            return func(*args, **kwargs)
        return wrapper
    return decorator

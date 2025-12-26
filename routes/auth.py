from flask import Blueprint, render_template, request, redirect, session
from repositories.user_repo import create_user, get_user_by_email
from services.auth_service import hash_password, check_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        create_user(email, hash_password(password), "user")
        return redirect("/login")
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = get_user_by_email(request.form["email"])

        if user and check_password(request.form["password"], user[2]):
            session["user_id"] = user[0]
            session["role"] = user[3]

            # Редирект по роли
            if session["role"] == "doctor":
                from repositories.doctor_repo import get_doctor_by_user_id
                session["doctor_id"] = get_doctor_by_user_id(user[0])
                return redirect("/doctor/appointments")
            else:
                return redirect("/doctors")  # «Врачи» для обычного пользователя
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

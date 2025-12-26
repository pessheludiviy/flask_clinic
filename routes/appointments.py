from flask import flash
from flask import Blueprint, render_template, request, redirect, session
from services.auth_service import login_required
from services.appointment_service import book
from repositories.appointment_repo import get_by_user
from services.auth_service import role_required
from repositories.appointment_repo import get_by_doctor
from repositories.doctor_repo import get_all_doctors
from repositories.appointment_repo import delete_by_id
from repositories.appointment_repo import is_time_slot_available
from repositories.doctor_repo import get_doctor_by_user_id
from flask import flash
from repositories.appointment_repo import (
    is_time_slot_available,
    find_nearest_available_time,
    create_appointment
)

appointment_bp = Blueprint("appointments", __name__)

@appointment_bp.route("/appointments", methods=["GET"])
@login_required
def my_appointments():
    return render_template(
        "appointments/list.html",
        appointments=get_by_user(session["user_id"])
    )



@appointment_bp.route("/doctor/appointments")
@login_required
@role_required("doctor")
def doctor_appointments():
    doctor_id = get_doctor_by_user_id(session["user_id"])

    if doctor_id is None:
        return "Доктор не найден", 404

    return render_template(
        "appointments/doctor_list.html",
        appointments=get_by_doctor(doctor_id)
    )


@appointment_bp.route("/appointments/create", methods=["POST"])
@login_required
def create():
    doctor_id = request.form["doctor_id"]
    time = request.form["time"]

    if not is_time_slot_available(doctor_id, time):
        nearest = find_nearest_available_time(doctor_id, time)

        if nearest:
            flash(f"Это время занято. Ближайшее доступное: {nearest}")
        else:
            flash("Это время занято. Свободных слотов поблизости нет.")

        return redirect("/doctors")

    create_appointment(
        session["user_id"],
        doctor_id,
        time.replace("T", " ")
    )
    flash("Запись успешно создана")
    return redirect("/appointments")



@appointment_bp.route("/appointments/delete/<int:appointment_id>", methods=["POST"])
@login_required
def delete(appointment_id):
    delete_by_id(appointment_id, session["user_id"])
    return redirect("/appointments")


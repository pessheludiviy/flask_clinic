from flask import Blueprint, render_template
from repositories.doctor_repo import get_all_doctors
from services.auth_service import login_required

doctor_bp = Blueprint("doctors", __name__)

@doctor_bp.route("/doctors")
@login_required
def doctors():
    return render_template(
        "doctors/list.html",
        doctors=get_all_doctors()
    )




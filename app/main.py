from flask import Blueprint, render_template, session, redirect, url_for, flash
from .models import User, Medicine

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("home.html")

@main.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    patient = User.query.get(user_id)

    if not patient or patient.role != "patient":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("auth.login"))

    nurse = patient.assigned_nurse

    medicines = Medicine.query.filter_by(patient_id=patient.id).all()
    total_cost = sum([med.total_value for med in medicines]) if medicines else 0

    return render_template(
        "dashboard.html",
        patient=patient,
        nurse=nurse,
        medicines=medicines,
        total_cost=total_cost
    )

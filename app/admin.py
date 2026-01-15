from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from .models import User, Profile, Medicine, db
from .decorators import login_required, role_required
from datetime import datetime

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/dashboard")
@login_required
@role_required("nurse")
def admin_dashboard():
    nurse = User.query.get(session["user_id"])
    if not nurse:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    patients = User.query.filter_by(role="patient").all()
    num_patients = len(patients)
    total_meds = sum(len(p.assigned_medicines) for p in patients)

    patient_totals = {
        p.id: sum(med.total_value for med in p.assigned_medicines)
        for p in patients
    }

    return render_template(
        "admin/dashboard.html",
        nurse=nurse,
        patients=patients,
        num_patients=num_patients,
        total_meds=total_meds,
        patient_totals=patient_totals
    )

@admin.route("/view_profile/<int:user_id>")
@login_required
@role_required("nurse")
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    profile = user.profile

    if not profile:
        profile = Profile(
            user_id=user.id,
            first_name="N/A",
            last_name="N/A",
            phone=""
        )
        db.session.add(profile)
        db.session.commit()

    return render_template("admin/view_profile.html", profile=profile)

@admin.route("/add_patient_medicine/<int:patient_id>", methods=["POST"])
@login_required
@role_required("nurse")
def add_patient_medicine(patient_id):
    patient = User.query.get_or_404(patient_id)

    med = Medicine(
        name=request.form["name"],
        category=request.form["category"],
        quantity=int(request.form["quantity"]),
        price=float(request.form["price"]),
        patient_id=patient.id,
        issued_at=datetime.now(),
        expires_at=datetime.strptime(request.form["expires_at"], "%Y-%m-%d")
                    if request.form.get("expires_at") else None
    )

    db.session.add(med)
    db.session.commit()

    flash("Medicine added successfully.", "success")
    return redirect(url_for("admin.admin_dashboard"))

@admin.route("/edit_medicine/<int:med_id>", methods=["GET", "POST"])
@login_required
@role_required("nurse")
def edit_medicine(med_id):
    med = Medicine.query.get_or_404(med_id)

    if request.method == "POST":
        med.name = request.form["name"]
        med.category = request.form["category"]
        med.quantity = int(request.form["quantity"])
        med.price = float(request.form["price"])

        if request.form.get("expires_at"):
            med.expires_at = datetime.strptime(request.form["expires_at"], "%Y-%m-%d")

        db.session.commit()
        flash("Medicine updated successfully.", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("admin/edit.html", med=med)

@admin.route("/delete_medicine/<int:med_id>")
@login_required
@role_required("nurse")
def delete_medicine(med_id):
    med = Medicine.query.get_or_404(med_id)
    db.session.delete(med)
    db.session.commit()

    flash("Medicine deleted successfully.", "success")
    return redirect(url_for("admin.admin_dashboard"))

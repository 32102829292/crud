from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from .models import User, Profile, db

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        role = request.form["role"]
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        license_no = request.form.get("license_no")
        patient_no = request.form.get("patient_no")
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        phone = request.form.get("phone")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        if role == "nurse":
            if User.query.filter_by(license_no=license_no).first():
                flash("License number already exists.", "danger")
                return redirect(url_for("auth.register"))
            user = User(email=email, role="nurse", license_no=license_no)
        elif role == "patient":
            if User.query.filter_by(patient_no=patient_no).first():
                flash("Patient number already exists.", "danger")
                return redirect(url_for("auth.register"))
            user = User(email=email, role="patient", patient_no=patient_no)
        else:
            flash("Invalid role.", "danger")
            return redirect(url_for("auth.register"))

        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        profile = Profile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        db.session.add(profile)
        db.session.commit()

        flash("Account created successfully.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]
        email = request.form["email"].strip()
        password = request.form["password"]

        if role == "nurse":
            license_no = request.form["license_no"].strip()
            user = User.query.filter_by(
                email=email,
                license_no=license_no,
                role="nurse"
            ).first()

        elif role == "patient":
            patient_no = request.form["patient_no"].strip()
            user = User.query.filter_by(
                email=email,
                patient_no=patient_no,
                role="patient"
            ).first()
        else:
            flash("Invalid role.", "danger")
            return redirect(url_for("auth.login"))

        if not user or not user.check_password(password):
            flash("Invalid credentials.", "danger")
            return redirect(url_for("auth.login"))

        session["user_id"] = user.id
        session["role"] = user.role

        flash("Logged in successfully.", "success")

        if user.role == "nurse":
            return redirect(url_for("admin.admin_dashboard"))
        else:
            return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html")

@auth.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))

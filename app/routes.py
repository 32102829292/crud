from flask import Blueprint, render_template
from .decorators import login_required, role_required
from .models import Employee

bp = Blueprint("main", __name__)
admin = Blueprint("admin", __name__)

@admin.route("/admin")
@login_required
@role_required("admin")
def admin_dashboard():
    employee= Employee.query.all()
    return render_template("admin/dashboard.html",employees=employee)

@bp.route("/")
def index():
    return render_template("home.html")

@bp.route("/dashboard")
@login_required
def dashboard():
    employee= Employee.query.all()
    return render_template("dashboard.html",employees=employee)




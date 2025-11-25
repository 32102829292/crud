from flask import Blueprint, render_template,  redirect, url_for, flash, request
from .decorators import login_required, role_required
from .models import Employee
from .models import db, Employee

bp = Blueprint("main", __name__)
admin = Blueprint("admin", __name__)

@admin.route("/admin")
@login_required
@role_required("admin")
def admin_dashboard():
    employee= Employee.query.all()
    return render_template("admin/dashboard.html",employees=employee)

@admin.route('/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def add_employee():
    if request.method == 'POST':
        name= request.form['name']
        membership_type=request.form['membership_type']
        rate=request.form['rate']
        hour=request.form['hour']
        salary=float(rate)*int(hour)
        deductions=float(salary)*(0.10)
        takeHome=float(salary)-float(deductions)
        if name==" " and membership_type==" ":
            flash("Name, email and course cannot be empty.")
        elif float(rate)<=0:
            flash("Negative rate!")
        elif int(hour)<=0:
            flash("Negative hour!")  
        else:
            new_employee=Employee(name=name,membership_type=membership_type,hour=hour,deductions=deductions,rate=rate,takeHome=takeHome)
            db.session.add(new_employee)
            db.session.commit()
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/add.html')

@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name= request.form['name']
        employee.membership_type=request.form['membership_type']
        employee.rate=request.form['rate']
        employee.hour=request.form['hour']
        employee.salary=float(employee.rate)*int(employee.hour)
        employee.deductions=float(employee.salary)*(0.10)
        employee.takeHome=float(employee.salary)-float(employee.deductions)
        db.session.commit()
        flash('Employee updated successfully!')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/edit.html', employees=employee)

@admin.route('/delete/<int:id>')
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route("/")
def index():
    return render_template("home.html")

@bp.route("/dashboard")
@login_required
def dashboard():
    employee= Employee.query.all()
    return render_template("dashboard.html",employees=employee)




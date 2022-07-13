from flask import redirect, render_template, request, url_for, Blueprint
from project import db
from project.models import Employee, Department
from project.employees.forms import EmployeeForm, DeleteForm

employees_blueprint = Blueprint(
    'employees',
    __name__,
    template_folder='templates'
)


@employees_blueprint.route('/', methods=["GET", "POST"])
def index():
    delete_form = DeleteForm()
    if request.method == "POST":
        form = EmployeeForm(request.form)
        if form.validate():
            new_employee = Employee(form.name.data, form.years_at_company.data)
            for id in form.departments.data:
                new_employee.departments.append(Department.query.get(id))
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('employees.index'))
        else:
            return redirect(url_for('employees.new'))
    return render_template('employees/index.html', employees=Employee.query.all(), delete_form=delete_form)


@employees_blueprint.route('/new')
def new():
    employee_form = EmployeeForm()
    return render_template('employees/new.html', form=employee_form)


@employees_blueprint.route('/<int:id>/edit')
def edit(id):
    employee = Employee.query.get_or_404(id)
    employee_form = EmployeeForm(obj=employee)
    return render_template('employees/edit.html', form=employee_form, employee=employee)


@employees_blueprint.route('/<int:id>', methods=["GET", "POST"])
def show(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        if request.form['method'] == "PATCH":
            form = EmployeeForm(request.form)
            if form.validate():
                employee.name = form.name.data
                employee.years_at_company = form.years_at_company.data
                employee.departments.clear()
                for id in form.departments.data:
                    employee.departments.append(Department.query.get(id))
                db.session.add(employee)
                db.session.commit()
                return redirect(url_for('employees.index'))
            else:
                return render_template('employees/edit.html', form=form, employee=employee)
        elif request.form['method'] == "DELETE":
            delete_form = DeleteForm(request.form)
            if delete_form.validate():
                db.session.delete(employee)
                db.session.commit()
                return redirect(url_for('employees.index'))
            else:
                return redirect(url_for('employees.index'))
    return render_template('employees/show.html', employee=employee, departments=employee.departments)

from flask import redirect, render_template, request, url_for, Blueprint
from project import db
from project.models import Employee, Department
from project.departments.forms import DepartmentForm, DeleteForm

departments_blueprint = Blueprint(
    'departments',
    __name__,
    template_folder='templates'
)


@departments_blueprint.route('/', methods=["GET", "POST"])
def index():
    delete_form = DeleteForm()
    if request.method == "POST":
        form = DepartmentForm(request.form)
        if form.validate():
            new_department = Department(form.name.data)
            db.session.add(new_department)
            db.session.commit()
            return redirect(url_for('departments.index'))
        else:
            return render_template('departments/new.html', form=form)
    return render_template('departments/index.html', departments=Department.query.all(), delete_form=delete_form)


@departments_blueprint.route('/new')
def new():
    department_form = DepartmentForm()
    return render_template('departments/new.html', form=department_form)


@departments_blueprint.route('/<int:id>/edit')
def edit(id):
    department = Department.query.get(id)
    department_form = DepartmentForm(obj=department)
    return render_template('departments/edit.html', form=department_form, department=department)


@departments_blueprint.route('/<int:id>', methods=["GET", "POST"])
def show(id):
    department = Department.query.get(id)
    if request.method == "POST":
        form = DepartmentForm(request.form)
        if request.form['method'] == "PATCH":
            if form.validate():
                department.name = form.name.data
                db.session.add(department)
                db.session.commit()
                return redirect(url_for('departments.index'))
            else:
                return render_template('departments/edit.html', form=form, department=department)
        elif request.form['method'] == "DELETE":
            delete_form = DeleteForm(request.form)
            if delete_form.validate():
                db.session.delete(department)
                db.session.commit()
            return redirect(url_for('departments.index'))
    return render_template('departments/show.html', department=department, employees=department.employees)


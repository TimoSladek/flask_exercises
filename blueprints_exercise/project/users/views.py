from flask import Blueprint, request, render_template, redirect, url_for, flash
from project.models import User
from project import db
from project.users.forms import UserForm, DeleteForm

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)


@users_blueprint.route('/', methods=["GET", "POST"])
def index():
    delete_form = DeleteForm()
    if request.method == "POST":
        form = UserForm(request.form)
        if form.validate():
            new_user = User(form.first_name.data, form.last_name.data, form.img_url.data)
            db.session.add(new_user)
            db.session.commit()
            flash('User Created!')
            return redirect(url_for('users.index'))
        else:
            return render_template('new.html', form=form)
    return render_template('users/index.html', users=User.query.all(), delete_form=delete_form)


@users_blueprint.route('/new')
def new():
    user_form = UserForm()
    return render_template('users/new.html', form=user_form)


@users_blueprint.route('/<int:id>/edit')
def edit(id):
    found_user = User.query.get_or_404(id)
    user_form = UserForm(obj=found_user)
    return render_template('users/edit.html', user=found_user, form=user_form)


@users_blueprint.route('/<int:id>', methods=["GET", "POST"])
def show(id):
    found_user = User.query.get_or_404(id)
    if request.method == "POST":
        if request.form['method'] == "PATCH":
            form = UserForm(request.form)
            if form.validate():
                found_user.first_name = form.first_name.data
                found_user.last_name = form.last_name.data
                found_user.img_url = request.form['img_url']
                db.session.add(found_user)
                db.session.commit()
                flash('User Updated!')
                return redirect(url_for('users.index'))
            else:
                return render_template('edit.html', user=found_user, form=form)
        elif request.form['method'] == "DELETE":
            delete_form = DeleteForm(request.form)
            if delete_form.validate():
                db.session.delete(found_user)
                db.session.commit()
                flash('User Deleted!')
                return redirect(url_for('users.index'))
            else:
                return redirect(url_for('index'))
    return render_template('users/show.html', user=found_user)

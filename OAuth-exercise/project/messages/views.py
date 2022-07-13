from flask import Blueprint, request, render_template, redirect, url_for, flash
from project.models import Message, User
from project import db
from project.messages.forms import MessageForm, DeleteForm
from project.decorators import ensure_correct_user
from flask_login import login_required

messages_blueprint = Blueprint(
    'messages',
    __name__,
    template_folder='templates'
)

all_messages_blueprint = Blueprint(
    'all_messages',
    __name__,
    template_folder='templates'
)


@all_messages_blueprint.route('/')
def index():
    return render_template('messages/all_messages.html', users=User.query.all())


@messages_blueprint.route('/', methods=["GET", "POST"])
@login_required
def index(user_id):
    delete_form = DeleteForm()
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        form = MessageForm(request.form)
        new_message = Message(form.content.data, user_id)
        db.session.add(new_message)
        db.session.commit()
        flash('Message Created!')
        return redirect(url_for('messages.index', user_id=user_id))
    return render_template('messages/index.html', user=user, delete_form=delete_form)


@messages_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(user_id):
    message_form = MessageForm()
    return render_template('messages/new.html', user=User.query.get_or_404(user_id), form=message_form)


@messages_blueprint.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(user_id, id):
    found_message = Message.query.get_or_404(id)
    message_form = MessageForm(obj=found_message)
    return render_template('messages/edit.html', message=found_message, form=message_form)


@messages_blueprint.route('/<int:id>', methods=["GET", "POST"])
@login_required
@ensure_correct_user
def show(user_id, id):
    found_message = Message.query.get_or_404(id)
    if request.method == "POST":
        if request.form['method'] == "PATCH":
            form = MessageForm(request.form)
            if form.validate():
                found_message.content = form.content.data
                db.session.add(found_message)
                db.session.commit()
                flash('Message Updated!')
                return redirect(url_for('messages.index', user_id=user_id))
            else:
                return render_template('messages/edit.html', message=found_message, form=form)
        elif request.form['method'] == "DELETE":
            delete_form = DeleteForm(request.form)
            if delete_form.validate():
                db.session.delete(found_message)
                db.session.commit()
                flash('Message Deleted!')
                return redirect(url_for('messages.index', user_id=user_id))
            else:
                return redirect(url_for('messages.index'))
    return render_template('messages/show.html', message=found_message)

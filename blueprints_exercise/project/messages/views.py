from flask import Blueprint, request, render_template, redirect, url_for, flash
from project.models import Message, User
from project import db
from project.messages.forms import MessageForm, DeleteForm

messages_blueprint = Blueprint(
    'messages',
    __name__,
    template_folder='templates'
)


@messages_blueprint.route('/', methods=["GET", "POST"])
def index(user_id):
    delete_form = DeleteForm()
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        new_message = Message(request.form['content'], user_id)
        db.session.add(new_message)
        db.session.commit()
        flash('Message Created!')
        return redirect(url_for('messages.index', user_id=user_id))
    return render_template('messages/index.html', user=user, delete_form=delete_form)


@messages_blueprint.route('/new')
def new(user_id):
    message_form = MessageForm()
    return render_template('messages/new.html', user=User.query.get_or_404(user_id), form=message_form)


@messages_blueprint.route('/<int:id>/edit')
def edit(user_id, id):
    found_message = Message.query.get_or_404(id)
    message_form = MessageForm(obj=found_message)
    return render_template('messages/edit.html', message=found_message, form=message_form)


@messages_blueprint.route('/<int:id>', methods=["GET", "POST"])
def show(user_id, id):
    found_message = Message.query.get_or_404(id)
    if request.method == "POST":
        if request.form['method'] == "PATCH":
            form = MessageForm(request.form)
            if form.validate():
                found_message.content = request.form['content']
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
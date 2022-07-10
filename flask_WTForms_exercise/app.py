from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import UserForm, MessageForm, DeleteForm
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users-messages'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    img_url = db.Column(db.Text)
    messages = db.relationship('Message', backref="user", lazy="dynamic", cascade="all,delete")

    def __init__(self, first_name, last_name, img_url):
        self.first_name = first_name
        self.last_name = last_name
        self.img_url = img_url


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id


@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/users', methods=["GET", "POST"])
def index():
    delete_form = DeleteForm()
    if request.method == "POST":
        form = UserForm(request.form)
        if form.validate():
            new_user = User(form.first_name.data, form.last_name.data, form.img_url.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('users/new.html', form=form)
    return render_template('users/index.html', users=User.query.all(), delete_form=delete_form)


@app.route('/users/new')
def new():
    user_form = UserForm()
    return render_template('users/new.html', form=user_form)


@app.route('/users/<int:id>', methods=["GET", "POST"])
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
                return redirect(url_for('index'))
            else:
                return render_template('users/edit.html', user=found_user, form=form)
        elif request.form['method'] == "DELETE":
            delete_form = DeleteForm(request.form)
            if delete_form.validate():
                db.session.delete(found_user)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
    return render_template('users/show.html', user=found_user)


@app.route('/users/<int:id>/edit')
def edit(id):
    found_user = User.query.get_or_404(id)
    user_form = UserForm(obj=found_user)
    return render_template('users/edit.html', user=found_user, form=user_form)


@app.route('/users/<int:user_id>/messages', methods=["GET", "POST"])
def messages_index(user_id):
    delete_form = DeleteForm()
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        new_message = Message(request.form['content'], user_id)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('messages_index', user_id=user_id))
    return render_template('messages/index.html', user=user, delete_form=delete_form)


@app.route('/users/<int:user_id>/new')
def messages_new(user_id):
    message_form = MessageForm()
    return render_template('messages/new.html', user=User.query.get_or_404(user_id), form=message_form)


@app.route('/users/<int:user_id>/messages/<int:id>/edit')
def messages_edit(user_id, id):
    found_message = Message.query.get_or_404(id)
    message_form = MessageForm(obj=found_message)
    return render_template('messages/edit.html', message=found_message, form=message_form)


@app.route('/users/<int:user_id>/messages/<int:id>', methods=["GET", "POST"])
def messages_show(user_id, id):
    found_message = Message.query.get_or_404(id)
    if request.method == "POST":
        if request.form['method'] == "PATCH":
            form = MessageForm(request.form)
            if form.validate():
                found_message.content = request.form['content']
                db.session.add(found_message)
                db.session.commit()
                return redirect(url_for('messages_index', user_id=user_id))
            else:
                return render_template('messages/edit.html', message=found_message, form=form)
        elif request.form['method'] == "DELETE":
            delete_form = DeleteForm(request.form)
            if delete_form.validate():
                db.session.delete(found_message)
                db.session.commit()
                return redirect(url_for('messages_index', user_id=user_id))
            else:
                return redirect(url_for('messages_index'))
    return render_template('messages/show.html', message=found_message)

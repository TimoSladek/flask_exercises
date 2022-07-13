from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, validators


class UserForm(FlaskForm):
    email = EmailField('Email address', [validators.InputRequired()])
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    img_url = StringField('img url')
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class LoginForm(FlaskForm):
    email = EmailField('Email address')
    password = PasswordField('Password', [validators.DataRequired()])


class DeleteForm(FlaskForm):
    pass

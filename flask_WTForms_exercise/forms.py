from flask_wtf import FlaskForm
from wtforms import StringField, validators


class UserForm(FlaskForm):
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    img_url = StringField('img url')


class MessageForm(FlaskForm):
    content = StringField('Message', [validators.DataRequired()])


class DeleteForm(FlaskForm):
    pass

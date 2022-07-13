from flask_wtf import FlaskForm
from wtforms import StringField, validators


class DepartmentForm(FlaskForm):
    name = StringField('Department', [validators.DataRequired()])


class DeleteForm(FlaskForm):
    pass

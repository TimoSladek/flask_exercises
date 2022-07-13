from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, widgets, validators
from project.models import Department


class EmployeeForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    years_at_company = IntegerField('Years At Company', [validators.NumberRange(min=1), validators.DataRequired()])

    departments = SelectMultipleField(
        'Departments',
        coerce=int,
        widget=widgets.ListWidget(prefix_label=True),
        option_widget=widgets.CheckboxInput(),
        choices=[(d.id, d.name) for d in Department.query.all()]
    )


class DeleteForm(FlaskForm):
    pass

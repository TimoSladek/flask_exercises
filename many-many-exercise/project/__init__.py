from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///many-many-example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
Migrate(app, db)

from project.employees.views import employees_blueprint
from project.departments.views import departments_blueprint

app.register_blueprint(employees_blueprint, url_prefix='/employees')
app.register_blueprint(departments_blueprint, url_prefix='/departments')


@app.route('/')
def root():
    return redirect(url_for('employees.index'))

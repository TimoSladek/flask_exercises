from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager
from flask_oauthlib.client import OAuth

app = Flask(__name__)
oauth = OAuth()
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///OAuth-exercise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
Migrate(app, db)

twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key='vraODuzd5YvY2AxLuVfpsy97k',
                           consumer_secret='ATA55iItKlR3j55qdR01q0ROOxMCYkNE9jycB0vFaNcEtd99Bn'
                           )

from project.users.views import users_blueprint
from project.messages.views import messages_blueprint
from project.messages.views import all_messages_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(messages_blueprint, url_prefix='/users/<int:user_id>/messages')
app.register_blueprint(all_messages_blueprint, url_prefix='/messages')

login_manager.login_view = 'users.login'

from project.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def root():
    return redirect(url_for('users.index'))

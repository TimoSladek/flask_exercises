from project import db, bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    img_url = db.Column(db.Text)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    messages = db.relationship('Message', backref="user", lazy="dynamic", cascade="all,delete")

    def __init__(self, *args):
        if len(args) == 1:
            self.username = args[0]
        else:
            self.first_name = args[0]
            self.last_name = args[1]
            self.img_url = args[2]
            self.username = args[3]
            self.password = bcrypt.generate_password_hash(args[4]).decode('UTF-8')
            self.email = args[5]

    @classmethod
    def authenticate(cls, email, password):
        found_user = cls.query.filter_by(email=email).first()
        if found_user:
            is_authenticated = bcrypt.check_password_hash(found_user.password, password)
            if is_authenticated:
                return found_user
        return False


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

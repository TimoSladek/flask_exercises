from project import db


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

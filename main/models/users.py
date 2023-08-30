from datetime import datetime
from main import db, login_manager
from flask_login import UserMixin


from main.models.posts import Posts

@login_manager.user_loader
def load_user(userid):
    return Users.query.get(int(userid))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=True)

    posts = db.relationship('Posts', backref='author', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.img_file})"
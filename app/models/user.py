from datetime import datetime
from ..extensions import db, login_manager
from flask_login import UserMixin
from .post import Post

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship(Post, backref='author')
    status = db.Column(db.String(50), default='user')
    avatar = db.Column(db.String(200))
    name = db.Column(db.String(50))
    login = db.Column(db.String(50))
    password = db.Column(db.String(200))
    date = db.Column(db.DateTime, default = datetime.utcnow)
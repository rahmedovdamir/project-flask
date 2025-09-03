from datetime import datetime
from ..extensions import db

class Post(db.Model):
    id_post = db.Column(db.Integer, primary_key=True)
    postname = db.Column(db.String(50))
    teacher  = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    student  = db.Column(db.Integer)
    date = db.Column(db.DateTime, default = datetime.utcnow)
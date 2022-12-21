import datetime
from blog import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
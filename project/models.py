
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Camera(db.Model):
    __tablename__ = 'camera'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    video_url = db.Column(db.String(100))
    audio_url = db.Column(db.String(100))
    test_url = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

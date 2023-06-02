from datetime import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy import LargeBinary


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    second_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    galleries = db.relationship("Gallery")


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gallery_name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    images = db.relationship("Image")


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255))
    gallery_id = db.Column(db.Integer, db.ForeignKey("gallery.id"))
    data = db.Column(
        LargeBinary
    )  # Change 'filename' to 'data' and the type to LargeBinary
    mime_type = db.Column(db.String(64))

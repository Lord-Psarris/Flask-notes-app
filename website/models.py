from . import db  # importing from the current folders __init__.py the db
from flask_login import UserMixin
from sqlalchemy.sql import func


# db.model sets the standard for all the values that would be entered to conform to
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # func.now gets the current time and date
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # allows referencing of another tables user id
    # uses one to many relationship


class User(db.Model, UserMixin):  # have db.models in it to use sql-alchemy as well as UserMixin for user shit
    id = db.Column(db.Integer, primary_key=True)  # for primary key
    email = db.Column(db.String(150), unique=True)  # unique key makes no other column value like this
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')  # every time a note is created it will be added to the list of users notes

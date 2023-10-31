# Laras code for creating classes for database information

from . import db
from flask_login import UserMixin

# Creating user class with database model

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class imageTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

def init_db():
    db.create_all()
    print('Created Database!')

if __name__ == '__main__':
    init_db()

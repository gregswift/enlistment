#!/usr/bin/python

## Imports
# sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy

## Initialize extensions
db = SQLAlchemy(app)
api_manager = APIManager(app, flask_sqlalchemy_db=db)
login_manager = LoginManager()
login_manager.setup_app(app)

## Setup Database model

# define user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode)
    password = db.Column(db.Unicode)

# define candidate model
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)

# define panel model
class Panel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    candidateid = db.Column(db.Integer)
    results = db.Column(db.Integer)

# define panelists model
class Panelist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    panelid = db.Column(db.Integer)
    userid = db.Column(db.Integer)

# define vote model
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    panelid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    vote = db.Column(db.Integer)

def initialize(app):
    return SQLAlchemy(app)

def create_db(db):
    db.create_all()

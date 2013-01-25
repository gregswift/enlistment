#!/usr/bin/python

## Imports
# system
import os
# base
from flask import Flask, request, render_template, redirect, url_for, flash
#login
from flask.ext.login import current_user, login_user, LoginManager, UserMixin
# restless
from flask.ext.restless import APIManager
# sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy
# wtfroms
from flask.ext.wtf import PasswordField, SubmitField, TextField, Form

## Setup app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['OPENSHIFT_POSTGRESQL_DB_URL'] + os.environ['OPENSHIFT_APP_NAME']

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

# define vote model
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    panelid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    vote = db.Column(db.Integer)

## Initialize database 
db.create_all()

## Initialize admin user
admin = User(username=u'admin', password=u'0qww294e')
db.session.add(admin)
db.session.commit()

## Establish Flask_login - required
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

## Create Login Form
class LoginForm(Form):
    username = TextField('username')
    password = PasswordField('password')
    submit = SubmitField('Login')

## Initialize main page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

## Initialize login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #
        # you would check username and password here...
        #
        username, password = form.username.data, form.password.data
        user = User.query.filter_by(username=username,
                                    password=password).one()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

# Step 8: create the API for User with the authentication guard.
auth_func = lambda: current_user.is_authenticated()
api_manager.create_api(User, authentication_required_for=['GET'],
                       authentication_function=auth_func)
api_manager.create_api(Candidate, authentication_required_for=['GET','POST'],
                       authentication_function=auth_func)
api_manager.create_api(Panel, authentication_required_for=['GET','POST','PATCH'],
                       authentication_function=auth_func)
api_manager.create_api(Vote, authentication_required_for=['GET','POST','PATCH'],
                       authentication_function=auth_func)

if __name__ == "__main__":
    app.run()

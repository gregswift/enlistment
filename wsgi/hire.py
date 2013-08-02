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

## Import backend db
import hire.db as backend

## Enable logentries for external logging
from logentries import LogentriesHandler
import logging

log = logging.getLogger('logentries')
log.addHandler(LogentriesHandler('86d1df26-b7e7-4ed1-9b30-2c1ef0bd0f6b'))

## Setup app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['OPENSHIFT_POSTGRESQL_DB_URL'] + os.environ['OPENSHIFT_APP_NAME']

## Initialize extensions
db = backend.initialize(app)
api_manager = APIManager(app, flask_sqlalchemy_db=db)
login_manager = LoginManager()
login_manager.setup_app(app)

## Initialize database 
backend.create_all(db)

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
api_manager.create_api(Candidate, methods=['GET','POST'])
#api_manager.create_api(Candidate, authentication_required_for=['GET','POST'],
#                       authentication_function=auth_func)
api_manager.create_api(Panel, methods=['GET','POST','PATCH'])
api_manager.create_api(Panelist, methods=['GET','POST','PATCH'])
#api_manager.create_api(Panel, authentication_required_for=['GET','POST','PATCH'],
#                       authentication_function=auth_func)
api_manager.create_api(Vote, methods=['GET','POST','PATCH'])
#api_manager.create_api(Vote, authentication_required_for=['GET','POST','PATCH'],
#                       authentication_function=auth_func)

# Results
@app.route('/results/<panelid>', methods=['GET'])
def return_results(panelid):
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import func
    session = sessionmaker(bind=db)
    #return session.query(func.sum(Vote.vote).label('results')).filter_by(Vote.panelid=panelid).all()

if __name__ == "__main__":
    app.run()

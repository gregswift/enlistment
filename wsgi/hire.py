#!/usr/bin/python2
'''
    Hire App for Rackspace
        - Web Service and API used for Candidate voting of the H.I.R.E. process

    Contributors: Greg Swift, Tony Rogers, Josh Conant
'''

import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user, login_user, LoginManager, UserMixin
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import PasswordField, SubmitField, TextField, Form

READONLY = ['GET']
WRITEABLE = ['GET','POST','PATCH','PUT']

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['OPENSHIFT_POSTGRESQL_DB_URL'] + os.environ['OPENSHIFT_APP_NAME']

db = SQLAlchemy(app)
api_manager = APIManager(app, flask_sqlalchemy_db=db)
login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model, UserMixin):
    """ User Table """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode)
    password = db.Column(db.Unicode)

class Candidate(db.Model):
    """ Candidate Table """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)

class Panel(db.Model):
    """ Panel Table (Owner is the creator, but the owner could be merged with Panellist)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    candidateid = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    results = db.Column(db.Integer)

class Panelist(db.Model):
    """ Panel List Table (i.e. Voters) """
    id = db.Column(db.Integer, primary_key=True)
    panelid = db.Column(db.Integer, db.ForeignKey('panel.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

class Vote(db.Model):
    """ Vote Table (could be merged with Panelist) """
    id = db.Column(db.Integer, primary_key=True)
    panelid = db.Column(db.Integer, db.ForeignKey('panel.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    vote = db.Column(db.Integer)

db.create_all()

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

class LoginForm(Form):
    """ Login Webpage """
    username = TextField('username')
    password = PasswordField('password')
    submit = SubmitField('Login')

class RegistrationForm(Form):
    """ Registration Webpage """
    username = TextField('username')
    password = PasswordField('password')
    confirm_password = PasswordField('confirm_password')
    submit = SubmitField('Register')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login API call """
    form = LoginForm()
    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        user = User.query.filter_by(username=username,
                                    password=password).one()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Registration API Call """
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password, confirm = form.password.data, form.confirm_password.data
        if password != confirm:
            return redirect(url_for('register'))
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

api_manager.create_api(User, methods=READONLY, exclude_columns=['password'])
api_manager.create_api(Candidate, methods=WRITEABLE)
api_manager.create_api(Panel, methods=WRITEABLE)
api_manager.create_api(Panelist, methods=WRITEABLE)
api_manager.create_api(Vote, methods=WRITEABLE, allow_functions=True)

#@app.route('/results/<panelid>', methods=['GET'])
#def return_results(panelid):
#    """ Outputs the results of the Vote """
#    from sqlalchemy.orm import sessionmaker
#    from sqlalchemy import func
#    session = sessionmaker(bind=db)
#    return session.query(func.sum(Vote.vote).label('results')).filter_by(Vote.panelid=panelid).all()

if __name__ == "__main__":
    app.run()

#!/usr/bin/python

from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)


## Login
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active
    
    def is_active(self):
        return self.active


class Anonymous(AnonymousUser):
    name = u"Anonymous"


USERS = {
    1: User(u"greg5320", 1),
    2: User(u"josh.conant", 2),
    3: User(u"jesse.gonzalez", 3),
    4: User(u"jon.q.public", 4, False),
}

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


login_manager.setup_app(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/secret")
@fresh_login_required
def secret():
    return render_template("secret.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")


@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


## API
@app.route("/api")
def api_root():
    return

@app.route("/api/candidates")
def api_candidates():
    return 'List of ' + url_for('api_candidates')

@app.route('/api/candidate/new/<name>')
def api_new_candidate(name):
    return 'candidate {0} added'.format(name)

@app.route('/api/panel/new/<name>')
def api_new_panel(name):
    return 'panel {0} created'.format(name)

@app.route('/api/panel/<panelid>/candidate/<candidateid>/<action>')
def api_new_panel(panelid, candidateid, action):
    return 'canidate {0} {1}ed to panel {2}'.format(candidateid, action, panelid)

@app.route('/api/panel/<panelid>/panelist/<name>/<action>')
def api_add_panelist(panelid, name):
    return 'panelist {0} {1}ed to panel {2}'.format(name, action, panelid)

@app.route('/api/panel/<panelid>/vote/<vote>')
def api_vote_candidate(panelid, vote):
    return 'You voted {0} for panel {1}'.format(vote, panelid)

@app.route('/api/panel/<panelid>/results')
def api_vote_candidate(panelid):
    return 'You ask for the results for the vote on panel {0}'.format(panelid)

if __name__ == "__main__":
    app.run()

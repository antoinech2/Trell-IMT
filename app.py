import bcrypt
from flask import Flask, redirect, url_for
from flask_login import login_manager, LoginManager, login_user, login_required, current_user, logout_user

from src.database.database import db, init_database
from src.database.models import *
import flask

app = flask.Flask(__name__)

title = "Task"
users = ["./static/img/logo.jpg", "./static/img/logo.jpg", "./static/img/logo.jpg"]
description = "descriptionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "TrellIMTAdmin47935"

db.init_app(app)  # (1) flask prend en compte la base de donnee
with app.test_request_context():  # (2) bloc exécuté à l'initialisation de Flask
    init_database()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in_view'

salt = bcrypt.gensalt()


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.filter_by(email=user_id).first()


@app.route('/')
@login_required
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/fail')
def fail_pss():  # put application's code here
    return 'mauvais mdp!'


@app.route('/unknowned')
def fail_email():  # put application's code here
    return 'compte existe pas squalala!'


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in_view():
    form = flask.request.form
    if form:
        user = User.query.filter_by(email=form.get("email")).first()
        if user:
            if bcrypt.checkpw(form.get("password").encode('utf-8'), user.password):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect("/")
            else:
                return redirect("/fail")
        else:
            return redirect("/unknowned")
    return flask.render_template("sign_in.html.jinja2")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect("/sign_in")


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up_view():
    form = flask.request.form
    if form:
        new_user = User(email=form.get("email"), password=bcrypt.hashpw(form.get("password").encode('utf-8'), salt),
                        first_name=form.get("first_name"), last_name=form.get("last_name"), type=form.get("user_type"))
        db.session.add(new_user)
        db.session.commit()

    return flask.render_template("sign_up.html.jinja2")


@app.route('/task')
def task_view():
    return flask.render_template("task.html.jinja2", title=title, description=description, users=users)


if __name__ == '__main__':
    app.run()

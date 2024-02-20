from flask import Flask
from flask_login import login_manager, LoginManager

from src.database.database import db, init_database
from src.database.models import *
import flask

app = flask.Flask(__name__)

title = "Task"
users = ["./static/img/logo.jpg", "./static/img/logo.jpg", "./static/img/logo.jpg"]
description = "descriptionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  # (1) flask prend en compte la base de donnee
with app.test_request_context():  # (2) bloc exécuté à l'initialisation de Flask
    init_database()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/sign_in')
def sign_in_view():
    return flask.render_template("sign_in.html.jinja2")


@app.route('/sign_up')
def sign_up_view():
    return flask.render_template("sign_up.html.jinja2")

@app.route('/task')

def task_view():
    return flask.render_template("task.html.jinja2", title=title, description = description , users = users )


if __name__ == '__main__':
    app.run()

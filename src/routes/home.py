from flask_login import login_required
import flask

from app import app
from src.database.models import *


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

@app.route('/home')
def home_view():
    return flask.render_template("home.html.jinja2", username = "Moa", user_logo = "./static/img/logo_user.jpg")
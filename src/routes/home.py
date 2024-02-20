from flask_login import login_required, current_user
import flask

from app import app
from src.database.models import *
def get_user_profile():
    if current_user.is_authenticated:
        return f"/profile/{current_user.id}"
    else:
        return "/sign_in"

def get_user_project():
    if current_user.is_authenticated:
        return '/project/{current_user.id}'
    else:
        return "/sign_in"

def get_user_new_project():
    if current_user.is_authenticated:
        return '/new_project/{current_user.id}'
    else:
        return "/sign_in"


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
    return flask.render_template("home.html.jinja2",
                                 username = "Moa",
                                 user_logo = "./static/img/logo_user.jpg",
                                 user_profile = get_user_profile(),
                                 user_project = get_user_project(),
                                 user_new_projet = get_user_new_project())

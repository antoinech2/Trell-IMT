from flask_login import login_required, current_user
import flask

from app import app
from src.database.models import *

def get_user_logo():
    if current_user.is_authenticated:
        return "./static/img/logo_user.jpg"
    else :
        return "./static/img/logo_user.jpg"
def get_user_name():
    if current_user.is_authenticated:
        return "actual user"
    else :
        return "not authenticated"

def get_user_profile():
    if current_user.is_authenticated:
        return f"/profile/{current_user.id}"
    else:
        return "/sign_in"

def get_user_project():
    if current_user.is_authenticated:
        return f"/project/{current_user.id}"
    else:
        return "/sign_in"

def get_user_new_project():
    if current_user.is_authenticated:
        return f"/new_project/{current_user.id}"
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
    return flask.render_template("header.html.jinja2",
                                 username = get_user_name(),
                                 user_logo = get_user_logo(),
                                 user_profile = get_user_profile(),
                                 user_project = get_user_project(),
                                 user_new_project = get_user_new_project(),
                                 page_template = "task.html.jinja2")

@app.route('/contact')
def contact_view():
    return flask.render_template("header.html.jinja2",
                                 username = get_user_name(),
                                 user_logo = get_user_logo(),
                                 user_profile = get_user_profile(),
                                 user_project = get_user_project(),
                                 user_new_project = get_user_new_project(),
                                 page_template = "contact.html.jinja2")
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
def hello_world():  # put application's code here
    return 'Page d''accueil'


@app.route('/home')
@login_required
def home_view():
    return flask.render_template("header.html.jinja2",
                                 user = current_user,
                                 user_logo = "./static/img/logo_user.jpg",
                                 page_template = "task.html.jinja2")

@app.route('/contact')
def contact_view():
    return flask.render_template("header.html.jinja2",
                                 user = current_user,
                                 user_logo = "./static/img/logo_user.jpg",
                                 page_template = "contact.html.jinja2")
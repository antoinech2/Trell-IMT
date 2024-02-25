from flask_login import login_required, current_user
import flask

from app import app
from src.database.models import *

@app.route('/')
def hello_world():  # put application's code here
    return 'Page d''accueil'


@app.route('/home')
@login_required
def home_view():
    return flask.render_template("header.html.jinja2",
                                 user=current_user,
                                 user_logo="./static/img/logo_user.jpg",
                                 page_template="home_page.html.jinja2")


@app.route('/contact')
def contact_view():
    return flask.render_template("header.html.jinja2",
                                 user=current_user,
                                 user_logo="./static/img/logo_user.jpg",
                                 page_template="contact.html.jinja2")

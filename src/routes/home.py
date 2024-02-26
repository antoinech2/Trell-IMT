from flask_login import login_required, current_user
import flask

from app import app
from src.database.models import *

@app.route('/')
def hello_world():  # put application's code here
    return flask.render_template("site_page.html.jinja2")

@app.route('/test')
def test():  # put application's code here
    return flask.render_template("components/add_task.html.jinja2", user = current_user)

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

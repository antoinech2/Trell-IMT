from flask_login import login_required, current_user
import flask

from app import app
from src.database.models import *


@app.route('/')
def hello_world():  # put application's code here
    return flask.render_template("site_page.html.jinja2")


@app.route('/home')
@login_required
def home_view():
    return flask.render_template("project_manager/project_manager_page.html.jinja2",
                                 user=current_user, boards = current_user.boards)


@app.route('/contact')
def contact_view():
    return flask.render_template("contact.html.jinja2",
                                 user=current_user)

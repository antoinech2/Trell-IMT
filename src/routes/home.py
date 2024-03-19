import json

from flask_login import login_required, current_user
import flask

from app import app
from src.database.models import *
from src.routes.board_dev import board_developer


@app.route('/')
def hello_world():  # put application's code here
    return flask.render_template("site_page.html.jinja2")


@app.route('/home', methods=['GET'])
@login_required
def home_view():
    if current_user.type == UserType.Developer:
        return flask.redirect("/board_developer")
    else:
        with open('data/new_board_template.json') as json_file:
            categories = json.load(json_file)
        return flask.render_template("project_manager/project_manager_page.html.jinja2",
                                    user=current_user, boards = current_user.boards, categories = categories)


@app.route('/contact')
def contact_view():
    is_manager = True
    if current_user.type == UserType.Developer:
        is_manager = False
    return flask.render_template("contact.html.jinja2",
                                 user=current_user,
                                 is_manager=is_manager)

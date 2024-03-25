import json
from flask_login import login_required, current_user
import flask
from app import app
from src.database.models import *


# Define a route for the root URL ('/') of the application.
@app.route('/')
def hello_world():
    return flask.render_template("site_page.html.jinja2")


@app.route('/home', methods=['GET'])
@login_required
def home_view():
    """Home page"""
    # Check if the currently logged-in user is a developer.
    if current_user.type == UserType.Developer:
        # If the user is a developer, redirect them to a developer-specific page.
        return flask.redirect("/board_developer")
    else:
        # If the user is not a developer, load a JSON file containing board categories.
        with open('data/new_board_template.json') as json_file:
            categories = json.load(json_file)
        # Render a template for project managers, passing in the user, their boards, and the loaded categories.
        return flask.render_template("project_manager/project_manager_page.html.jinja2",
                                     user=current_user, boards=current_user.boards, categories=categories)

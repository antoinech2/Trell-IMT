from flask_login import login_required, current_user
import json
import re
import bcrypt
import flask
from flask import request, redirect, render_template
from app import app, salt
from src.database.models import *

@app.route('/new_project', methods=["GET", "POST"])
@login_required
def new_project_form():
    form = flask.request.form
    valid_form, errors = validate_sign_up_form(form)

    # to handle the template
    board_template = request.args.get('template')
    with open('data/new_board_template.json', 'r') as f:
        data = json.load(f)
    list = data[board_template]

    if valid_form:
        categories = form.get('category_list').split("|")
        new_project = Board(name=form.get('project_name'),description=form.get('description'))
        db.session.add(new_project)
        db.session.commit()
        for category in categories:
            new_category = Category(board_id=new_project.id, name=category)
            db.session.add(new_category)
        current_user.boards.append(new_project)
        db.session.add(current_user)
        db.session.commit()
        return flask.render_template('create_project_success.html.jinja2', board_id=new_project.id)
    else:
        return flask.render_template("project_creator.html.jinja2", user = current_user, form = form, errors = errors, template_list_category = list)


def validate_sign_up_form(form):
    result = True
    errors = []

    # Check for form sending
    if not form:
        result = False
        return result, errors

    # Check that this project does not already exist (unique name)
    if Board.query.filter_by(name=form.get("project_name")).count() > 0:
        result = False
        errors.append("A project with the same name already registered")

    return result, errors
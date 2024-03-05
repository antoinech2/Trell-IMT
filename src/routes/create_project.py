from flask_login import login_required, current_user
import re
import bcrypt
import flask
from app import app, salt
from src.database.models import *

@app.route('/create_project', methods=["GET", "POST"])
@login_required
def create_project():
    form = flask.request.form
    valid_form, errors = validate_sign_up_form(form)
    if valid_form:
        #new_project = Project (name=form.get('project_name'),description=form.get('project_description'),catégories=form.get('catégories'))
        #db.session.add(new_project)
        db.session.commit()
        return flask.render_template('create_project_success.html.jinja2')
    else:
        return flask.render_template("project_creator.html.jinja2",user = current_user,form = form, errors = errors)


def validate_sign_up_form(form):
    result = True
    errors = []

    # Check for form sending
    if not form:
        result = False
        return result, errors

    # Check that this project does not already exist (unique name)
    #if Project.query.filter_by(name=form.get("project_name")).count() > 0:
        #result = False
        #errors.append("A project with the same name already registered")

    return result, errors
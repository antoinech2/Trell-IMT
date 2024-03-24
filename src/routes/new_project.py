from flask_login import login_required, current_user
import json
import flask
from flask import request
from app import app
from src.database.models import *

@app.route('/new_project', methods=["GET", "POST"])
@login_required  # Ensure that the user must be logged in to access this route.
def new_project_form():
    valid_form = False
    form = {}
    errors = []

    # If the request method is POST, it means the user is submitting the form.
    if request.method == "POST":
        # Get the JSON data sent with the request
        form = request.get_json()
        # Validate the form data and store the result (True/False) and any error messages.
        valid_form, errors = validate_sign_up_form(form)

    # If the form is valid, proceed to create a new project.
    if valid_form:
        # Split the categories from the form by "|". If no categories are provided, use an empty list.
        categories = form['category_list'].split("|")
        if len(categories) == 1 and categories[0] == "":
            categories = []

        # Create a new Board (project) object with the name and description from the form.
        new_project = Board(name=form['project_name'], description=form['description'])
        # Assign users to the project by querying the database for users with IDs listed in the form.
        new_project.users = db.session.query(User).filter(User.id.in_(form['collaborators'])).all()
        # Add the new project to the database session and commit to save it.
        db.session.add(new_project)
        db.session.commit()

        # For each category provided, create a new Category object and add it to the session.
        for category in categories:
            new_category = Category(board_id=new_project.id, name=category)
            db.session.add(new_category)

        # Associate the current user with the new project and save changes to the database.
        current_user.boards.append(new_project)
        db.session.add(current_user)
        db.session.commit()

        # Return a success template if the project is created successfully.
        return flask.render_template('project_manager/project_creator_success.html.jinja2', user=current_user,
                                     board_id=new_project.id)
    else:
        # If the form is not valid, potentially use a template for the form based on a request argument.
        board_template = request.args.get('template')
        list = []
        if board_template:
            # Load a template from a file if specified.
            with open('data/new_board_template.json', 'r') as f:
                data = json.load(f)
            list = data[board_template]

        # Return the form template, including any form data and errors that were identified.
        return flask.render_template("project_manager/project_creator.html.jinja2", user=current_user, form=form,
                                     errors=errors, template_list_category=list)


# Define a function to validate the form data.
def validate_sign_up_form(form):
    result = True
    errors = []

    # Ensure that some data was actually sent with the form.
    if not form:
        result = False
        return result, errors

    # Check if a project with the same name already exists in the database.
    if Board.query.filter_by(name=form["project_name"]).count() > 0:
        result = False
        errors.append("A project with the same name already registered")

    return result, errors

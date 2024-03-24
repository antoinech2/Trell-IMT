import bcrypt
import flask
from flask import redirect
from flask_login import login_user

from app import app
from src.database.models import *


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in_view():
    form = flask.request.form
    valid_form, errors = validate_sign_in_form(form)

    if valid_form:
        user = User.query.filter_by(email=form.get("email")).first()
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True if form.get("remember") == "true" else False)
        return redirect("/home")
    return flask.render_template("sign_in.html.jinja2", errors=errors, form=form)


def validate_sign_in_form(form):
    result = True
    errors = []

    # Check for form sending
    if not form:
        result = False
        return result, errors

    user = User.query.filter_by(email=form.get("email")).first()
    # Check that user exist
    if not user:
        result = False
        errors.append("This email is not registered")

    # Check for password
    elif not bcrypt.checkpw(form.get("password").encode('utf-8'), user.password):
        result = False
        errors.append("Wrong password")

    return result, errors

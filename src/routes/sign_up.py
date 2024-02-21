import re

import bcrypt
import flask

from app import app, salt
from src.database.models import *


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up_view():
    form = flask.request.form
    valid_form, errors = validate_sign_up_form(form)
    if valid_form:
        new_user = User(email=form.get("email"), password=bcrypt.hashpw(form.get("password").encode('utf-8'), salt),
                        first_name=form.get("first_name"), last_name=form.get("last_name"), type=form.get("user_type"))
        db.session.add(new_user)
        db.session.commit()
        return flask.render_template("sign_up_success.html.jinja2")
    else:
        return flask.render_template("sign_up.html.jinja2", errors=errors, form=form)


def validate_sign_up_form(form):
    result = True
    errors = []
    if not form:
        result = False
        return result, errors
    if form.get("confirmpassword") != form.get("password"):
        result = False
        errors.append("Password confirmation does not match with original password")
    if len(form.get("password")) < 7:
        result = False
        errors.append("Password must be at least 7 characters long")
    if not any(char.isdigit() for char in form.get("password")):
        result = False
        errors.append("Password must contain at least one number")
    if not any(char.isupper() for char in form.get("password")):
        result = False
        errors.append("Password must contain at least one uppercase letter")

    special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if not special_chars.search(form.get("password")):
        result = False
        errors.append("Password must contain at least one special character")

    return result, errors

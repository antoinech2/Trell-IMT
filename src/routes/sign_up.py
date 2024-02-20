import bcrypt
import flask

from app import app, salt
from src.database.models import *


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up_view():
    form = flask.request.form
    if form:
        new_user = User(email=form.get("email"), password=bcrypt.hashpw(form.get("password").encode('utf-8'), salt),
                        first_name=form.get("first_name"), last_name=form.get("last_name"), type=form.get("user_type"))
        db.session.add(new_user)
        db.session.commit()
        return flask.render_template("sign_up_success.html.jinja2")
    else:
        return flask.render_template("sign_up.html.jinja2")

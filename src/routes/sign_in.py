import bcrypt
import flask
from flask import redirect
from flask_login import login_user

from app import app
from src.database.models import *


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in_view():
    form = flask.request.form
    if form:
        user = User.query.filter_by(email=form.get("email")).first()
        if user:
            if bcrypt.checkpw(form.get("password").encode('utf-8'), user.password):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect("/")
            else:
                return redirect("/fail")
        else:
            return redirect("/unknowned")
    return flask.render_template("sign_in.html.jinja2")

from datetime import datetime

import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Task


@app.route('/new_task', methods=["POST"])
@login_required
def new_task_form():
    form = flask.request.form
    category_id = request.args.get('category_id')
    if form and category_id:
        new_task = Task(category_id=category_id, name=form.get("title"), description=form.get("description"), date_expires = datetime.strptime(form.get('task-end'), "%Y-%m-%dT%H:%M") if form.get('task-end') else None)
        db.session.add(new_task)
        db.session.commit()

    return redirect(request.referrer)

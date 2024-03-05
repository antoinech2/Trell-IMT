from datetime import datetime

import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Task


@app.route('/edit_task', methods=["POST"])
@login_required
def edit_task_form():
    form = flask.request.form
    task_id = request.args.get('task_id')
    if form and task_id:
        task = Task.query.filter_by(id=task_id).first()
        task.name = form.get('title')
        task.description = form.get('description')
        if form.get('task-end'):
            task.date_expires = datetime.strptime(form.get('task-end'), "%Y-%m-%dT%H:%M")
        db.session.add(task)
        db.session.commit()

    return redirect(request.referrer)

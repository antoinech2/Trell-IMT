import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Task


@app.route('/delete_task', methods=["POST"])
@login_required
def remove_task_form():
    form = flask.request.form
    task_id = request.args.get('task_id')
    if form and task_id:
        task = Task.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()

    return redirect(request.referrer)

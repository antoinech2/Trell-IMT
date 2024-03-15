import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Task, Step


@app.route('/delete_task', methods=["POST"])
@login_required
def remove_task_form():
    form = flask.request.form
    task_id = request.args.get('task_id')
    if form and task_id:
        task = Task.query.filter_by(id=task_id).first()
        delete_task(task)

    return redirect(request.referrer)


def delete_task(task):
    task.etiquettes = []
    task.users = []
    db.session.commit()
    db.session.query(Step).filter_by(task_id=task.id).delete()
    db.session.delete(task)
    db.session.commit()

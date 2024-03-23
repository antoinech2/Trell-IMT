import flask
from flask import request, redirect
from flask_login import login_required, current_user

from app import app
from src.database.database import db
from src.database.models import Task, Step, Notification


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

    notifications = [Notification(user_id=user.id, title="Tâche supprimée",
                                  content="La tâche '{}' a été supprimée par {}. Vous ne pouvez plus y accéder.".format(
                                      task.name, current_user.first_name + " " + current_user.last_name))
                     for user in task.users if user.id != current_user.id]

    db.session.add_all(notifications)

    task.users = []
    db.session.commit()
    db.session.query(Step).filter_by(task_id=task.id).delete()
    db.session.delete(task)
    db.session.commit()

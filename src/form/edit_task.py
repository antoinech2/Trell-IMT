from datetime import datetime

import flask
from flask import request, redirect
from flask_login import login_required, current_user

from app import app
from src.database.database import db
from src.database.models import Task, Step, Etiquette, User, Notification


@app.route('/edit_task', methods=["PUT"])
@login_required
def edit_task_form():
    form = request.get_json()
    task_id = request.args.get('task_id')
    if form and task_id:
        task = Task.query.filter_by(id=task_id).first()

        task.name = form['title']

        task.description = form['description']

        if form['task-end']:
            task.date_expires = datetime.strptime(form.get('task-end'), "%Y-%m-%dT%H:%M")

        task.etiquettes = [Etiquette.query.filter_by(id=etiquette_id).first() for etiquette_id in form['etiquette']]

        task.users = [User.query.filter_by(id=user_id).first() for user_id in form['collaborator']]

        notifications = [Notification(user_id=user_id, title="Tâche mise à jour",
                                      content="La tâche '{}' a été mise à jour par {}".format(task.name, current_user.first_name + " " + current_user.last_name))
                         for user_id in form['collaborator'] if user_id != current_user.id]

        db.session.add_all(notifications)
        db.session.add(task)
        db.session.commit()

        db.session.query(Step).filter_by(task_id=task_id).delete()
        db.session.commit()
        for subtask in form['subtask']:
            new_step = Step(task_id=task_id, name=subtask["name"], status=subtask["value"])
            db.session.add(new_step)
        db.session.commit()

        return "", 200
    else:
        return "", 400

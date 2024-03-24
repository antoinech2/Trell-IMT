from datetime import datetime

from flask import request, redirect
from flask_login import login_required, current_user

from app import app
from src.database.database import db
from src.database.models import Task, User, Etiquette, Step, Notification


@app.route('/new_task', methods=["POST"])
@login_required
def new_task_form():
    form = request.get_json()
    category_id = request.args.get('category_id')
    if form and category_id:

        date_expires = datetime.strptime(form.get('task-end'), "%Y-%m-%dT%H:%M") if form.get('task-end') else None

        etiquettes = [Etiquette.query.filter_by(id=etiquette_id).first() for etiquette_id in form['etiquette']]

        users = [User.query.filter_by(id=user_id).first() for user_id in form['collaborator']]

        new_task = Task(category_id=category_id, name=form['title'], description=form['description'], date_expires = date_expires, etiquettes = etiquettes, users = users)

        notifications = [Notification(user_id=user.id, title="New task assigned",
                                      content="{} created the task '{}' and assigned it to you".format(current_user.first_name + " " + current_user.last_name, new_task.name))
                         for user in new_task.users if user.id != current_user.id]

        db.session.add_all(notifications)

        db.session.add(new_task)
        db.session.commit()

        for subtask in form['subtask']:
            new_step = Step(task_id=new_task.id, name=subtask["name"], status=subtask["value"])
            db.session.add(new_step)
        db.session.commit()

    return redirect(request.referrer)

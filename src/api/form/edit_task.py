from datetime import datetime

from flask import request
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
        notifications = []
        task = Task.query.filter_by(id=task_id).first()

        task.name = form['title']

        task.description = form['description']

        new_users = [User.query.filter_by(id=user_id).first() for user_id in form['collaborator']]

        # New collaborators
        notifications.extend([Notification(user_id=user.id, title="New task assigned",
                                           content="{} assigned you to the task '{}'".format(
                                               current_user.first_name + " " + current_user.last_name, task.name))
                              for user in new_users if (user.id != current_user.id and user not in task.users)])
        notifications.extend([Notification(user_id=user_notif.id, title="New collaborator for task",
                                           content="{} added {} as new collaborator for task '{}'".format(
                                               current_user.first_name + " " + current_user.last_name,
                                               user.first_name + " " + user.last_name, task.name))
                              for user in new_users if (user.id != current_user.id and user not in task.users) for
                              user_notif in new_users if user_notif in task.users])

        # Removed collaborators
        notifications.extend([Notification(user_id=user.id, title="Task unassigned",
                                           content="{} removed you from collaborators of task '{}'".format(
                                               current_user.first_name + " " + current_user.last_name, task.name))
                              for user in task.users if (user.id != current_user.id and user not in new_users)])
        notifications.extend([Notification(user_id=user_notif.id, title="Collaborator removed from task",
                                           content="{} removed {} from collaborators of task '{}'".format(
                                               current_user.first_name + " " + current_user.last_name,
                                               user.first_name + " " + user.last_name, task.name))
                              for user in task.users if (user.id != current_user.id and user not in new_users) for
                              user_notif in task.users if user_notif in new_users])

        task.users = new_users

        if form['task-end']:
            new_date = datetime.strptime(form.get('task-end'), "%Y-%m-%dT%H:%M")
            if task.date_expires is None:
                notifications.extend(add_notification(task, "New deadline",
                                                      "{} has added a deadline for task {}. Deadline is {}".format(
                                                          current_user.first_name + " " + current_user.last_name,
                                                          task.name,
                                                          datetime.strptime(form.get('task-end'), "%d/%m/%Y %H:%M"))))
            elif task.date_expires != new_date:
                notifications.extend(add_notification(task, "Deadline changed",
                                                      "Deadline of task '{}' was changed by {}.\
                                                       New deadline is {}".format(
                                                          task.name,
                                                          current_user.first_name + " " + current_user.last_name,
                                                          datetime.strptime(form.get('task-end'), "%d/%m/%Y %H:%M"))))

            task.date_expires = new_date

        elif task.date_expires is not None:
            notifications.extend(
                add_notification(task, "Deadline removed", "Deadline of task '{}' was removed by {}".format(
                    task.name, current_user.first_name + " " + current_user.last_name)))

        new_etiquettes = [Etiquette.query.filter_by(id=etiquette_id).first() for etiquette_id in form['etiquette']]

        for etiquette in new_etiquettes:
            if etiquette not in task.etiquettes:
                notifications.extend(
                    add_notification(task, "New etiquette to task",
                                     "Etiquette '{}' was added to task '{}' by {}".format(
                                         etiquette.label, task.name,
                                         current_user.first_name + " " + current_user.last_name))
                )

        for etiquette in task.etiquettes:
            if etiquette not in new_etiquettes:
                notifications.extend(add_notification(task, "Etiquette removed from task",
                                                      "Etiquette '{}' was removed from task '{}' by {}".format(
                                                          etiquette.label, task.name,
                                                          current_user.first_name + " " + current_user.last_name)))

        task.etiquettes = new_etiquettes

        db.session.add(task)
        db.session.commit()

        db.session.query(Step).filter_by(task_id=task_id).delete()
        db.session.commit()
        for subtask in form['subtask']:
            new_step = Step(task_id=task_id, name=subtask["name"], status=subtask["value"])
            db.session.add(new_step)
        db.session.add_all(notifications)
        db.session.commit()

        return "", 200
    else:
        return "", 400


def add_notification(task, title, content):
    return [Notification(user_id=user.id, title=title,
                         content=content)
            for user in task.users if (user.id != current_user.id)]

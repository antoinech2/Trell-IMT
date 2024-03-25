from datetime import datetime

from flask import request, abort
from flask_login import login_required, current_user

from app import app
from src.database.database import db
from src.database.models import Task, Step, Etiquette, User, Notification


@app.route('/edit_task', methods=["PUT"])
@login_required
def edit_task_form():
    """Update task data after user modification.

    Actualise task's data such as name, description, expiration, collaborators, etiquettes

    Request arguments :
    - int : task_id - The id of the task to update

    Request content :
    JSON object with new data of task
    """
    form = request.get_json()
    task_id = request.args.get('task_id')

    # Check for request content
    if form and task_id:
        notifications = []

        # Get the task to update
        task = Task.query.filter_by(id=task_id).first()

        # General information
        task.name = form['title']
        task.description = form['description']

        # Collaborators

        new_users = [User.query.filter_by(id=user_id).first() for user_id in form['collaborator']]
        # Notify new collaborators
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

        # Notify removed collaborators
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

        # Expiration date

        # If expiration date is defined
        if form['task-end']:
            # Convert datetime in database format
            new_date = datetime.strptime(form.get('task-end'), "%Y-%m-%dT%H:%M")
            if task.date_expires is None:
                notifications.extend(add_notification(task, "New deadline",
                                                      "{} has added a deadline for task {}. Deadline is {}".format(
                                                          current_user.first_name + " " + current_user.last_name,
                                                          task.name,
                                                          new_date.strftime("%d/%m/%Y %H:%M"))))
            elif task.date_expires != new_date:
                notifications.extend(add_notification(task, "Deadline changed",
                                                      "Deadline of task '{}' was changed by {}.\
                                                       New deadline is {}".format(
                                                          task.name,
                                                          current_user.first_name + " " + current_user.last_name,
                                                          new_date.strftime("%d/%m/%Y %H:%M"))))

            task.date_expires = new_date

        elif task.date_expires is not None:
            notifications.extend(
                add_notification(task, "Deadline removed", "Deadline of task '{}' was removed by {}".format(
                    task.name, current_user.first_name + " " + current_user.last_name)))

        # Etiquettes
        # TODO : improve with in_
        new_etiquettes = [Etiquette.query.filter_by(id=etiquette_id).first() for etiquette_id in form['etiquette']]

        # Notify users for new etiquette
        for etiquette in new_etiquettes:
            if etiquette not in task.etiquettes:
                notifications.extend(
                    add_notification(task, "New etiquette to task",
                                     "Etiquette '{}' was added to task '{}' by {}".format(
                                         etiquette.label, task.name,
                                         current_user.first_name + " " + current_user.last_name))
                )

        # Notify users for removed etiquette
        for etiquette in task.etiquettes:
            if etiquette not in new_etiquettes:
                notifications.extend(add_notification(task, "Etiquette removed from task",
                                                      "Etiquette '{}' was removed from task '{}' by {}".format(
                                                          etiquette.label, task.name,
                                                          current_user.first_name + " " + current_user.last_name)))

        task.etiquettes = new_etiquettes

        db.session.add(task)
        db.session.commit()

        # Subtasks

        # Remove old subtasks from database
        db.session.query(Step).filter_by(task_id=task_id).delete()
        db.session.commit()

        # Create new subtasks
        for subtask in form['subtask']:
            new_step = Step(task_id=task_id, name=subtask["name"], status=subtask["value"])
            db.session.add(new_step)
        db.session.add_all(notifications)
        db.session.commit()

        return "ok", 200
    else:
        # Return wrong request
        abort(400)


def add_notification(task, title, content):
    """Return notification for every collaborator of the task

    :param Task task: Task object
    :param srt title: Title of the notification
    :param str content: Content of the notification

    :return Notification[]: list of generated notifications

    """
    return [Notification(user_id=user.id, title=title,
                         content=content)
            for user in task.users if (user.id != current_user.id)]

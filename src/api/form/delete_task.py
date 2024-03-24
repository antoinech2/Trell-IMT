import flask
from flask import request, redirect
from flask_login import login_required, current_user

from app import app
from src.database.database import db
from src.database.models import Task, Step, Notification


@app.route('/delete_task', methods=["POST"])
@login_required
def remove_task_form():
    """Delete task from database.

    Delete any subtask contained in the task.

    Request arguments :
    - int : task_id - The id of the category to delete

    sent from an HTML form
    """
    form = flask.request.form
    task_id = request.args.get('task_id')

    if form and task_id:
        task = Task.query.filter_by(id=task_id).first()
        delete_task(task)

    # Refresh page
    return redirect(request.referrer)


def delete_task(task):
    """Delete task from database

    :param task task: task object to delete

    :return: nothing
    """

    # Clear etiquettes
    task.etiquettes = []

    # Notify deletion to task collaborators
    notifications = [Notification(user_id=user.id, title="Tâche deleted",
                                  content="Task '{}' was deleted by {}. You can't access it anymore.".format(
                                      task.name, current_user.first_name + " " + current_user.last_name))
                     for user in task.users if user.id != current_user.id]
    db.session.add_all(notifications)

    # Clear collaborators
    task.users = []

    db.session.commit()
    db.session.query(Step).filter_by(task_id=task.id).delete()
    db.session.delete(task)
    db.session.commit()

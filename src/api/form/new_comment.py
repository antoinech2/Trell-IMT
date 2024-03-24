from datetime import datetime

import flask
from flask import request
from flask_login import login_required, current_user

from app import app
from src.database.database import db
from src.database.models import Commentary, Notification, Task
from src.helper.date import compare_dates


@app.route('/new_comment', methods=["POST"])
@login_required
def new_comment_form():
    form = flask.request.form
    task_id = request.args.get('task_id')
    comment = {}
    if form and task_id:
        new_comment = Commentary(task_id=task_id, user_id=current_user.id, title=form.get("title"),
                                 content=form.get("content"), date_created=datetime.now())

        task = Task.query.filter_by(id=task_id).first()

        notifications = [Notification(user_id=user.id, title="Comment added",
                                      content="New comment by {} on task '{}' : '{}'".format(
                                          current_user.first_name + " " + current_user.last_name, task.name,
                                          new_comment.content[:100] + "..."))
                         for user in task.users if user.id != current_user.id]

        db.session.add_all(notifications)

        db.session.add(new_comment)
        db.session.commit()
        comment = {"title": new_comment.title,
                   "content": new_comment.content,
                   "author": current_user.first_name + " " + current_user.last_name,
                   "time_message": compare_dates(new_comment.date_created)[1],
                   "time": new_comment.date_created.strftime("%d/%m/%Y %H:%M")}
    return comment, 303

import json

from flask import request

from app import app
from flask_login import login_required

from src.database.database import db
from src.database.models import Task, Step, Commentary, User
from src.helper.date import compare_dates


@app.route('/get_task', methods=['GET'])
@login_required
def get_collaborators():
    task_id = request.args.get('task_id')
    if task_id:
        collaborator = [user.as_dict() for user in Task.query.filter_by(id=task_id).first().users]
        etiquette = [etiquette.as_dict() for etiquette in Task.query.filter_by(id=task_id).first().etiquettes]
        subtask = [step.as_dict() for step in Step.query.filter_by(task_id=task_id).all()]
        comment = [{"title": comment.title,
                    "content": comment.content,
                    "author": user.first_name + " " + user.last_name,
                    "time_message": compare_dates(comment.date_created)[1],
                    "time": comment.date_created.strftime("%d/%m/%Y %H:%M")}
                   for (comment, user) in
                   db.session.query(Commentary, User).join(User, Commentary.user_id == User.id).filter(
                       Commentary.task_id == task_id).all()]
        return json.dumps(
            {"collaborator": collaborator, "etiquette": etiquette, "subtask": subtask, "comment": comment})

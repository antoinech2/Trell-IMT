from flask import request
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Task, User


@app.route('/update_collaborators', methods=["POST"])
@login_required
def update_collaborators():
    task_id = request.args.get('task_id')
    subtask_data = request.get_json()
    if subtask_data is not None:
        if not task_id:
            task_id = Task.query.order_by(Task.id.desc()).first().id

        task = Task.query.filter_by(id=task_id).first()
        task.users = []
        for user_id in subtask_data:
            task.users.append(User.query.filter_by(id=user_id).first())
        db.session.commit()

    return "Success", 200

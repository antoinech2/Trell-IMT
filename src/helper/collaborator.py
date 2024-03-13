import flask
from flask import abort, request

from app import app
from flask_login import login_required, current_user

from src.database.models import Step, Task


@app.route('/get_collaborators', methods=['GET'])
@login_required
def get_collaborators():
    task_id = request.args.get('task_id')
    if task_id:
        return [{"id": user.id, "first_name": user.first_name, "last_name" : user.last_name} for user in Task.query.filter_by(id=task_id).first().users]

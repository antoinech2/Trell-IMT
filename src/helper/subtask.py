from datetime import datetime

import flask
from flask import abort, request

from app import app
from flask_login import login_required, current_user

from src.database.models import Step


@app.route('/get_subtasks', methods=['GET'])
@login_required
def get_subtasks():
    task_id = request.args.get('task_id')
    if task_id:
        steps = {step.name: step.status for step in Step.query.filter_by(task_id=task_id).all()}
        return steps

from datetime import datetime

import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Task, Step


@app.route('/update_subtasks', methods=["POST"])
@login_required
def update_subtasks():
    task_id = request.args.get('task_id')
    subtask_data = request.get_json()
    if subtask_data is not None:
        if not task_id:
            task_id = Task.query.order_by(Task.id.desc()).first().id

        db.session.query(Step).filter_by(task_id=task_id).delete()
        db.session.commit()

        for subtask in subtask_data:
            new_step = Step(task_id=task_id, name=subtask["name"], status=subtask["value"])
            db.session.add(new_step)
        db.session.commit()
    return "Success", 200

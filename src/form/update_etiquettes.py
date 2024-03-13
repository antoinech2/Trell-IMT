import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Task, Step, Etiquette


@app.route('/update_etiquettes', methods=["POST"])
@login_required
def update_etiquettes():
    task_id = request.args.get('task_id')
    subtask_data = request.get_json()
    if subtask_data is not None:
        if not task_id:
            task_id = Task.query.order_by(Task.id.desc()).first().id

        task = Task.query.filter_by(id=task_id).first()
        task.etiquettes = []
        for etiquette_id in subtask_data:
            task.etiquettes.append(Etiquette.query.filter_by(id=etiquette_id).first())
        db.session.commit()

    return "Success", 200

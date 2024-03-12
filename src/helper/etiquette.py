import flask
from flask import abort, request

from app import app
from flask_login import login_required, current_user

from src.database.models import Step, Task


@app.route('/get_etiquettes', methods=['GET'])
@login_required
def get_etiquettes():
    task_id = request.args.get('task_id')
    if task_id:
        return [{"id": etiquette.id, "name" : etiquette.label, "description":etiquette.description, "color": etiquette.color} for etiquette in Task.query.filter_by(id=task_id).first().etiquettes]

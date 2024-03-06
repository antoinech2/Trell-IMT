from datetime import datetime

import flask
from flask import abort

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task, Step


@app.route('/board/<board_id>')
@login_required
def board(board_id):
    global expired
    board = Board.query.filter_by(id=board_id).first()
    if not board in current_user.boards:
        abort(401, description="You don't have access to this board.")

    tasks_data = []
    categories = Category.query.filter_by(board_id=board_id).all()
    for category in categories:
        tasks_data.append(category.__dict__)
        tasks_data[-1]['tasks'] = []
        tasks = Task.query.filter_by(category_id=category.id).all()
        for task in tasks:
            task_dict = task.__dict__

            subtasks_done = Step.query.filter_by(task_id=task_dict["id"], status="1").count()
            subtasks_not_done = Step.query.filter_by(task_id=task_dict["id"], status="0").count()
            if subtasks_done + subtasks_not_done > 0:
                task_dict['progress'] = round(subtasks_done / (subtasks_done + subtasks_not_done) * 100)

            if task_dict["date_expires"]:
                expired = False
                delta_date = task_dict["date_expires"] - datetime.now()
                days, seconds = delta_date.days, delta_date.seconds
                if days < 0:
                    expired = True
                    delta_date = datetime.now() - task_dict["date_expires"]
                    days, seconds = delta_date.days, delta_date.seconds
                hours = (days * 24 + seconds) // 3600
                minutes = (abs(seconds) % 3600) // 60
                if abs(days) > 0:
                    message_data = "{} days".format(abs(days))
                elif abs(hours) > 0:
                    message_data = "{} hours".format(abs(hours))
                else:
                    message_data = "{} minutes".format(abs(minutes))
                if expired:
                    task_dict["expires_message"] = "Expired {} ago".format(message_data)
                    task_dict["has_expired"] = True
                else:
                    task_dict["expires_message"] = "Expires in {}".format(message_data)
                    task_dict["has_expired"] = False
                task_dict["date_expires"] = task_dict["date_expires"].strftime("%Y-%m-%dT%H:%M")
            tasks_data[-1]['tasks'].append(task_dict)
    return flask.render_template("board_developer.html.jinja2", tasks_data=tasks_data, user=current_user, board=board)

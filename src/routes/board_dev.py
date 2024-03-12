import flask

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task

@app.route('/board_developer', methods=["GET", "POST"])
@login_required
def board_developer():
    form = flask.request.form
    project_name = ["project1", "project2", "project3", "project4"]
    task_name = ["task1", "task2", "task3"]
    importance = ["importance1", "importance2"]
    states = ["state1", "state2", "state3"]

    boards = Board.query.all()
    tasks = Task.query.all()

    return flask.render_template("developer/Board_developer.html.jinja2", user=current_user,
                                 form=form,
                                 project_name=project_name,
                                 task_name=task_name,
                                 importance=importance,
                                 states=states,
                                 tasks_data=tasks)
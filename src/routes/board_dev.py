import flask

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task

import sys
sys.path.append("src/helper")
from get_task import*

@app.route('/board_developer', methods=["GET", "POST"])
@login_required
def board_developer():
    form = flask.request.form
    project_name = ["project1", "project2", "project3", "project4"]
    task_name = ["task1", "task2", "task3"]
    importance = ["importance1", "importance2"]
    states = ["state1", "state2", "state3"]

    tasks = get_tasks_from_form(form)


    return flask.render_template("developer/Board_developer.html.jinja2", user=current_user,
                                 form=form,
                                 project_name=project_name,
                                 task_name=task_name,
                                 importance=importance,
                                 states=states,
                                 tasks_data=tasks)

def get_tasks_from_form (form):
    name = form.get("project_name")
    tasks = Task.query.all()
    tasks_data = []
    for task in tasks:
        tasks_data.append(get_task(task))
    if name == "project1":
        return tasks_data[0:2]
    else:
        return tasks_data
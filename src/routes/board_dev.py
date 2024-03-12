import flask

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task

from src.helper.get_task import get_task

@app.route('/board_developer', methods=["GET", "POST"])
@login_required
def board_developer():
    form = flask.request.form
    project_name = ["project1", "project2", "project3", "project4"]
    task_name = ["task1", "task2", "task3"]
    importance = ["none","importance1", "importance2"]
    states = ["none","state1", "state2", "state3"]

    tasks = get_tasks_from_form2(form)


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

def get_tasks_from_form2 (form):
    param = {}
    tasks_data = []
    print (form.get("project_name"))
    if form.get("project_name"):
        param["Board.name"] = form.get("project_name")
    if form.get("task_name"):
        param["Task.name"] = form.get("task_name")
    if form.get("importance") != "none":
        param["Task.priority"] = form.get("importance")
    if form.get("state") != "none" :
        param["states"] = form.get("state")
    if form.get("tasks_date"):
        param["Task.date_expires"] = form.get("tasks_date")
    tasks = Task.query.join(Category, Category.id == Task.category_id, Board, Category.board_id == Board.id).filter_by(param).all()
    for task in tasks:
        tasks_data.append(get_task(task))
    return tasks_data
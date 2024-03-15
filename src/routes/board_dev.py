import flask
from sqlalchemy import and_

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task, db

from src.helper.get_task_display import get_task


@app.route('/board_developer', methods=["GET", "POST"])
@login_required
def board_developer():
    form = flask.request.form
    project_name = ["project1", "project2", "project3", "project4"]
    task_name = ["task1", "task2", "task3"]
    importance = ["none", "importance1", "importance2"]
    states = ["none", "state1", "state2", "state3"]
    tasks = get_tasks_from_form(form)
    return flask.render_template("developer/Board_developer.html.jinja2", user=current_user,
                                 form=form,
                                 project_name=project_name,
                                 task_name=task_name,
                                 importance=importance,
                                 states=states,
                                 tasks_data=tasks)

def get_tasks_from_form(form):
    tasks_data = []

    conditions = []
    if form.get("project_name"):
        conditions.append(Board.name == form.get("project_name"))
    if form.get("task_name"):
        conditions.append(Task.name == form.get("task_name"))
    print (conditions)
    query = db.session.query(Task, Category, Board) \
        .join(Category, Category.id == Task.category_id) \
        .join(Board, Board.id == Category.board_id)

    if conditions:
        query = query.filter(and_(*conditions))

    tasks = query.all()

    for task in tasks:
        tasks_data.append(get_task(task[0]))  # Assuming get_task() is designed to take a Task object
    return tasks_data
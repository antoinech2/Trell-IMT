import flask
from sqlalchemy import and_

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task, db, BoardUsers

from src.helper.get_task_display import get_task


@app.route('/board_developer', methods=["GET", "POST"])
@login_required
def board_developer():
    form = flask.request.form
    project_name = [board.name for board in current_user.boards]
    task_name = [task.name for task in current_user.tasks]
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
    query = db.session.query(Task) \
        .join(Category, Category.id == Task.category_id) \
        .join(Board, Board.id == Category.board_id)

    if conditions:
        query = query.filter(and_(*conditions))

    tasks = query.all()

    for task in tasks:
        if current_user in task.users:
            tasks_data.append(get_task(task))
    return tasks_data
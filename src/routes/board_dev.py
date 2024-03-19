import flask
from sqlalchemy import and_

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task, db, Etiquette, EtiquetteTask, User

from src.helper.get_task_display import get_task


@app.route('/board_developer', methods=["GET", "POST"])
@login_required
def board_developer():
    form = flask.request.form
    if form :
        form.state = int(form.get('state'))
        form.importance = int(form.get('importance'))
    project_name = [board.name for board in current_user.boards]
    task_name = [task.name for task in current_user.tasks]
    importance = Etiquette.query.filter(Etiquette.type == "priority").all()
    states = Etiquette.query.filter(Etiquette.type == "status").all()
    tasks = get_tasks_from_form(form)

    etiquette_data = {}
    for etiquette_type in db.session.query(Etiquette.type).distinct():
        etiquette_data[etiquette_type[0]] = {data.__dict__["id"]: data.__dict__ for data in
                                             Etiquette.query.filter_by(type=etiquette_type[0]).all()}


    return flask.render_template("developer/board_developer.html.jinja2", user=current_user,
                                 form=form,
                                 project_name=project_name,
                                 task_name=task_name,
                                 importance=importance,
                                 states=states,
                                 tasks_data=tasks)

def get_tasks_from_form(form):
    tasks_data = []

    conditions = [current_user.id == User.id]
    if form:
        if form.get("project_name"):
            conditions.append(Board.name == form.get("project_name"))
        if form.get("task_name"):
            conditions.append(Task.name == form.get("task_name"))
        if int(form.get("importance")) > 0:
            conditions.append(Etiquette.id == form.get("importance"))
        if int(form.get("state")) > 0:
            conditions.append(Etiquette.id == form.get("state"))
        if form.get("task_date"):
            conditions.append(Task.date_expires < form.get("task_date"))
    print (conditions)

    query = db.session.query(Task) \
        .join(Category, Category.id == Task.category_id) \
        .join(Board, Board.id == Category.board_id) \
        .outerjoin(Task.etiquettes) \
        .outerjoin(Task.users)


    query = query.filter(and_(*conditions))

    tasks = query.all()

    for task in tasks:
        tasks_data.append(get_task(task))
    return tasks_data
import flask
from flask import abort

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task

@app.route('/create_project')
@login_required
def create_project():
    form = flask.request.form
    return flask.render_template("project_creator.html.jinja2",user = current_user,form = form)


@app.route('/board/<board_id>')
@login_required
def board(board_id):
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
            tasks_data[-1]['tasks'].append(task.__dict__)
    return flask.render_template("board_developer.html.jinja2", tasks_data=tasks_data, user = current_user, board = board)




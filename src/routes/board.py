import flask
from flask import abort

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task

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
            task_dict = task.__dict__
            if task_dict["date_expires"]:
                task_dict["date_expires"] = task_dict["date_expires"].strftime("%Y-%m-%dT%H:%M")
            tasks_data[-1]['tasks'].append(task_dict)
    return flask.render_template("board_developer.html.jinja2", tasks_data=tasks_data, user = current_user, board = board)




from flask import abort

from app import app
from flask_login import login_required, current_user

from src.database.models import Board, Category, Task


@app.route('/board/<board_id>')
@login_required
def board(board_id):
    print(current_user.boards)
    if not Board.query.filter_by(id=board_id).first() in current_user.boards:
        abort(401, description="You don't have access to this board.")

    tasks_data = []
    categories = Category.query.filter_by(board_id=board_id).all()
    for category in categories:
        tasks_data.append(category.__dict__)
        tasks_data[-1]['tasks'] = []
        tasks = Task.query.filter_by(category_id=category.id).all()
        for task in tasks:
            tasks_data[-1]['tasks'].append(task.__dict__)
    print(tasks_data)
    return "ok"




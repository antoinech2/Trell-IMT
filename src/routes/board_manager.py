import flask
from flask import abort

from app import app
from flask_login import login_required, current_user

from src.database.database import db
from src.database.models import Board, Category, Task, Etiquette

from src.helper.get_task_display import get_task


@app.route('/board/<board_id>')
@login_required
def board(board_id):
    """Show main page of board

    Board contains categories and task. It can be shared with collaborators.

    Request arguments :
    - /<board_id> - Id of board to show

    """
    cur_board = Board.query.filter_by(id=board_id).first()

    # Check for acess permission
    if cur_board not in current_user.boards:
        abort(401, description="You don't have access to this board.")

    # Etiquette data
    # to generate etiquette selector component
    etiquette_data = {}
    for etiquette_type in db.session.query(Etiquette.type).distinct():
        etiquette_data[etiquette_type[0]] = {data.__dict__["id"]: data.__dict__ for data in
                                             Etiquette.query.filter_by(type=etiquette_type[0]).all()}

    # Board's task data
    tasks_data = []
    categories = Category.query.filter_by(board_id=board_id).all()

    # Loop for all categories
    for category in categories:
        tasks_data.append(category.__dict__)
        tasks_data[-1]['tasks'] = []
        tasks = Task.query.filter_by(category_id=category.id).all()

        # Add task display for each task in category
        for task in tasks:
            tasks_data[-1]['tasks'].append(get_task(task))

    # Render template
    return flask.render_template("project_manager/board_manager.html.jinja2", tasks_data=tasks_data, user=current_user,
                                 board=cur_board, etiquette_data=etiquette_data)

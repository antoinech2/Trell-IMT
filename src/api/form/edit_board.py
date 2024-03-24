from flask import request, redirect
from flask_login import login_required, current_user

from app import app
from src.database.database import db
from src.database.models import Board, User, Notification


@app.route('/edit_board', methods=["PUT"])
@login_required
def edit_board_form():
    """Update board data.

    Actualise board's name, description and collaborators to database

    Request arguments :
    - int : board_id - The id of the board to update

    Request content :
    JSON object with new data of board
    """
    form = request.get_json()
    board_id = request.args.get('board_id')

    # Check for request content
    if form and board_id:
        # Get board to update
        board = Board.query.filter_by(id=board_id).first()

        board.name = form['title']
        board.description = form['description']

        # Notify new collaborators
        new_users = db.session.query(User).filter(User.id.in_(form['collaborators'])).all()
        notifications = [Notification(user_id=user.id, title="New shared project",
                                      content="{} added you to the project '{}'".format(
                                          current_user.first_name + " " + current_user.last_name, board.name))
                         for user in new_users if (user.id != current_user.id and user not in board.users)]
        # Notify removed collaborators
        notifications.extend([Notification(user_id=user.id, title="Acess to project revoked",
                                           content="{} removed you from collaborators of project '{}'".format(
                                               current_user.first_name + " " + current_user.last_name, board.name))
                              for user in board.users if (user.id != current_user.id and user not in new_users)])

        db.session.add_all(notifications)
        board.users = new_users
        db.session.add(board)
        db.session.commit()

    # Refresh page
    return redirect(request.referrer)

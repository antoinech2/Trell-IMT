import flask
from flask import request, redirect
from flask_login import login_required, current_user

from app import app
from src.database.database import db
from src.database.models import Board, Category, Notification
from src.api.form.delete_category import delete_category


@app.route('/delete_board', methods=["POST"])
@login_required
def delete_board_form():
    """Delete board from database.

    Delete any  category, task and subtask contained in the board.

    Request arguments :
    - int : board_id - The id of the board to delete

    sent from an HTML form to confirm action
    """
    form = flask.request.form
    board_id = request.args.get('board_id')

    # Check for deleting confirmation
    if form and board_id:
        board = Board.query.filter_by(id=board_id).first()

        # Delete all categories of board
        for category in Category.query.filter_by(board_id=board_id).all():
            delete_category(category.id)

        # Notify all board collaborators of deletion
        notifications = [Notification(user_id=user.id, title="Project deleted",
                                      content="Project '{}' was deleted by {}. You can't access t anymore.".format(
                                          board.name, current_user.first_name + " " + current_user.last_name))
                         for user in board.users if user.id != current_user.id]

        # Commit all to database
        db.session.add_all(notifications)

        board.users = []
        db.session.commit()
        db.session.delete(board)
        db.session.commit()

    # Return to home page to access other boards
    return redirect("/home")

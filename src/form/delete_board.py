import flask
from flask import request, redirect
from flask_login import login_required, current_user

from app import app
from src.database.database import db
from src.database.models import Board, Category, Notification
from src.form.delete_category import delete_category


@app.route('/delete_board', methods=["POST"])
@login_required
def delete_board_form():
    form = flask.request.form
    board_id = request.args.get('board_id')
    if form and board_id:
        board = Board.query.filter_by(id=board_id).first()
        for category in Category.query.filter_by(board_id = board_id).all():
            delete_category(category.id)
        notifications = [Notification(user_id=user.id, title="Projet supprimé",
                                      content="Le projet '{}' a été supprimé par {}. Vous ne pouvez plus y accéder.".format(board.name, current_user.first_name + " " + current_user.last_name))
                         for user in board.users if user.id != current_user.id]

        db.session.add_all(notifications)

        board.users = []
        db.session.commit()
        db.session.delete(board)
        db.session.commit()

    return redirect("/home")

import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Board


@app.route('/delete_board', methods=["POST"])
@login_required
def delete_board_form():
    form = flask.request.form
    board_id = request.args.get('board_id')
    if form and board_id:
        board = Board.query.filter_by(id=board_id).first()
        board.users = []
        db.session.commit()
        db.session.delete(board)
        db.session.commit()

    return redirect("/home")

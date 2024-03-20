import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Board, User


@app.route('/edit_board', methods=["PUT"])
@login_required
def edit_board_form():
    form = request.get_json()
    board_id = request.args.get('board_id')
    if form and board_id:
        board = Board.query.filter_by(id=board_id).first()
        board.name = form['title']
        board.description = form['description']
        board.users = db.session.query(User).filter(User.id.in_(form['collaborators'])).all()
        db.session.add(board)
        db.session.commit()

    return redirect(request.referrer)

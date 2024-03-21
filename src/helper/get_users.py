from flask import request

from app import app
from flask_login import login_required

from src.database.models import User, Board


@app.route('/get_users', methods=['GET'])
@login_required
def get_users():
    board_id = request.args.get('board_id')
    if board_id:
        users = Board.query.filter_by(id = board_id).first().users
    else:
        users = User.query.all()
    return [{"id": user.id, "first_name": user.first_name, "last_name" : user.last_name} for user in users]

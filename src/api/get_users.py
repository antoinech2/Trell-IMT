from flask import request

from app import app
from flask_login import login_required

from src.database.models import User, Board
from src.helper.workload import calculate_workload


@app.route('/get_users', methods=['GET'])
@login_required
def get_users():
    board_id = request.args.get('board_id')
    if board_id:
        users = Board.query.filter_by(id=board_id).first().users
    else:
        users = User.query.all()
    return [{**user.as_dict(),
             "workload": calculate_workload(user)} for user in users]

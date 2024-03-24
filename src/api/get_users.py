from flask import request

from app import app
from flask_login import login_required

from src.database.models import User, Board
from src.helper.workload import calculate_workload


@app.route('/get_users', methods=['GET'])
@login_required
def get_users():
    """Retrieve application user list from database

    Get name, id and workload of all users of the application

    Request arguments :
    - [int : board_id] - Board id to filter user search only to the board's collaborators

    Request response :
    JSON object with user information
    """
    board_id = request.args.get('board_id')
    if board_id:
        # If board id passed, filter to only board collaborators
        users = Board.query.filter_by(id=board_id).first().users
    else:
        users = User.query.all()

    # Return user information and workload calculation
    return [{**user.as_dict(),
             "workload": calculate_workload(user)} for user in users]

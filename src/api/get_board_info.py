import json

from flask import request

from app import app
from flask_login import login_required

from src.database.models import Board


@app.route('/get_board', methods=['GET'])
@login_required
def get_board():
    board_id = request.args.get('board_id')
    if board_id:
        collaborator = [user.as_dict() for user in Board.query.filter_by(id=board_id).first().users]
        return json.dumps({"collaborator": collaborator})

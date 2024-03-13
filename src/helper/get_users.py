from flask import request

from app import app
from flask_login import login_required

from src.database.models import Step, Task, User


@app.route('/get_users', methods=['GET'])
@login_required
def get_users():
    return [{"first_name": user.__dict__["first_name"], "last_name" : user.__dict__["last_name"], "id":user.__dict__["id"]} for user in User.query.all()]

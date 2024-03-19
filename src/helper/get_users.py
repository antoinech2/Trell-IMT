from app import app
from flask_login import login_required

from src.database.models import User


@app.route('/get_users', methods=['GET'])
@login_required
def get_users():
    return [{"id": user.id, "first_name": user.first_name, "last_name" : user.last_name} for user in User.query.all()]

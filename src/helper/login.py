from flask_login import LoginManager

from src.database.models import User
from app import app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in_view'


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.filter_by(email=user_id).first()

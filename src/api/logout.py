from flask import redirect
from flask_login import login_required, current_user, logout_user

from app import app
from src.database.models import *


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    # Update user in database
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()

    # Return to application welcome page
    return redirect("/")

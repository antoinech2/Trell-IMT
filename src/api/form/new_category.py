import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Category


@app.route('/new_category', methods=["POST"])
@login_required
def new_category_form():
    """Create new category in board.

    Create blank category.

    Request arguments :
    - int : board_id - The id of the board in which the category is added

    Request content :
    HTML form with data of category
    """
    form = flask.request.form
    board_id = request.args.get('board_id')

    # Check for request content
    if form and board_id:
        new_category = Category(board_id=board_id, name=form.get("title"), description=form.get("description"))
        db.session.add(new_category)
        db.session.commit()

    # Refresh page
    return redirect(request.referrer)

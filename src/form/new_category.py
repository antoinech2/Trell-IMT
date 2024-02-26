import flask
from flask import request, redirect

from app import app
from src.database.database import db
from src.database.models import Category


@app.route('/new_category', methods=["POST"])
def new_category_form():
    form = flask.request.form
    board_id = request.args.get('board_id')
    if form and board_id:
        new_category = Category(board_id=board_id, name=form.get("title"), description=form.get("description"))
        db.session.add(new_category)
        db.session.commit()

    return redirect(request.referrer)

import flask
from flask import request, redirect

from app import app
from src.database.database import db
from src.database.models import Task


@app.route('/new_task', methods=["POST"])
def new_task_form():
    form = flask.request.form
    category_id = request.args.get('category_id')
    if form and category_id:
        new_task = Task(category_id=category_id, name=form.get("title"), description=form.get("description"))
        db.session.add(new_task)
        db.session.commit()

    return redirect(request.referrer)

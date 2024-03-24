import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Category, Task
from src.api.form.delete_task import delete_task


@app.route('/delete_category', methods=["POST"])
@login_required
def delete_category_form():
    """Delete category from database.

    Delete any task and subtask contained in the category.

    Request arguments :
    - int : category_id - The id of the category to delete

    sent from an HTML form to confirm action
    """
    form = flask.request.form
    category_id = request.args.get('category_id')

    # Check for deleting confirmation
    if form and category_id:
        delete_category(category_id)

    # Refresh page
    return redirect(request.referrer)


def delete_category(category_id):
    """Delete category from database

    :param int category_id: category id to delete

    :return: nothing
    """
    cat = Category.query.filter_by(id=category_id).first()
    db.session.delete(cat)

    # Delete all task in category
    for task in Task.query.filter_by(category_id=category_id).all():
        delete_task(task)

import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Category, Task


@app.route('/delete_category', methods=["POST"])
@login_required
def delete_category_form():
    form = flask.request.form
    category_id = request.args.get('category_id')
    if form and category_id:
        delete_category(category_id)
    return redirect(request.referrer)


def delete_category(category_id):
    cat = Category.query.filter_by(id=category_id).first()
    db.session.delete(cat)
    db.session.query(Task).filter_by(category_id=category_id).delete()
    db.session.commit()

import flask
from flask import request, redirect
from flask_login import login_required

from app import app
from src.database.database import db
from src.database.models import Category


@app.route('/edit_category', methods=["POST"])
@login_required
def edit_category_form():
    """Update category data.

    Actualise category's name and description to database

    Request arguments :
    - int : category_id - The id of the board to update

    Request content :
    HTML form with new data of category
    """
    form = flask.request.form
    category_id = request.args.get('category_id')

    # Check for request content
    if form and category_id:
        # Get category to update
        category = Category.query.filter_by(id=category_id).first()
        category.name = form.get('title')
        category.description = form.get('description')
        db.session.add(category)
        db.session.commit()

    # Refresh page
    return redirect(request.referrer)

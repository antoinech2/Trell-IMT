# Define a route for '/contact'.
import flask
from flask_login import current_user

from app import app
from src.database.models import UserType


@app.route('/contact')
def contact_view():
    # Render the contact page template
    return flask.render_template("contact.html.jinja2",
                                 user=current_user)

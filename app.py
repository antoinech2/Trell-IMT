import bcrypt
import flask

# Database import
from src.database.database import init_database
from src.database.models import *

# Application creation and config
app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "TrellIMTAdmin47935"

# Database initialisation
db.init_app(app)  # (1) flask prend en compte la base de donnee
with app.test_request_context():  # (2) bloc exécuté à l'initialisation de Flask
    init_database()

# Encryption salt
salt = bcrypt.gensalt()

# Local imports
import src.helper.login
import src.helper.logout
import src.helper.subtask

# Routes
import src.routes.sign_in
import src.routes.home
import src.routes.sign_up
import src.routes.board
import src.routes.new_project

import src.form.new_task
import src.form.new_category
import src.form.edit_task
import src.form.delete_task
import src.form.delete_category
import src.form.edit_category
import src.form.edit_board
import src.form.delete_board
import src.form.update_subtasks

if __name__ == '__main__':
    app.run()

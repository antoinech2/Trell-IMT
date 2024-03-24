import bcrypt
import flask
from flask_migrate import Migrate
from sqlalchemy import event

from src.database.data_init import insert_initial_values
# Database import
from src.database.database import init_database
from src.database.models import *

# Application creation and config
app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "TrellIMTAdmin47935"

# Database initialisation
db.init_app(app)
migrate = Migrate(app, db)

event.listen(Etiquette.__table__, "after_create", insert_initial_values)

with app.test_request_context():
    init_database()

# Encryption salt
salt = bcrypt.gensalt()

# Login import
import src.helper.login

# Routes
import src.routes.sign_in
import src.routes.home
import src.routes.sign_up
import src.routes.board_manager
import src.routes.new_project
import src.routes.board_dev
import src.routes.contact

## API import
import src.api.logout
import src.api.get_task_info
import src.api.get_users
import src.api.get_etiquettes
import src.api.get_board_info
import src.api.notifications

# Forms control
import src.api.form.new_task
import src.api.form.new_category
import src.api.form.edit_task
import src.api.form.delete_task
import src.api.form.delete_category
import src.api.form.edit_category
import src.api.form.edit_board
import src.api.form.delete_board
import src.api.form.new_comment

if __name__ == '__main__':
    app.run()

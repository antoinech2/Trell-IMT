from flask import Flask
from src.database.database import db, init_database
import flask

app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)  # (1) flask prend en compte la base de donnee
with app.test_request_context():  # (2) bloc exécuté à l'initialisation de Flask
    init_database()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/sign_in')
def sign_in_view():
    return flask.render_template("sign_in.html.jinja2")

@app.route('/sign_up')
def sign_up_view():
    return flask.render_template("sign_up.html.jinja2")


if __name__ == '__main__':
    app.run()
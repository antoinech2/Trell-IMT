import flask
from app import app


title = "Task"
users = ["./static/img/logo_user.jpg", "./static/img/logo.jpg", "./static/img/logo_user.jpg"]
description = "descriptionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"


@app.route('/task')
def task_view():
    return flask.render_template("components/task.html.jinja2", title=title, description=description, users=users)

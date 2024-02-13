import flask

app = flask.Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/register_login')
def static_resources_view():
    return flask.render_template("register_login.html.jinja2")



if __name__ == '__main__':
    app.run()
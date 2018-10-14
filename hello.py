from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/fun')
def the_name_is_arbitrary():
    return 'Hello, Fun!'

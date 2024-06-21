from flask import Flask

app = Flask(__name__)
print(__name__)


@app.route('/')
def index():
    return "<h1>Witaj, Świecie!</h1>"


@app.route('/user/<name>')
def user(name):
    return f"<h1>Witaj, {name}!</h1>"

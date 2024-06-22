from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"


@app.route('/user/<name>')
def user(name):
    return f"<h1>Hello, {name}!</h1>"

@app.route('/browser')
def browser():
    user_agent = request.headers.get('User-Agent')
    request_headers = dict(request.headers)
    headers = "<br>".join(map(': '.join, request_headers.items()))
    return f"<p>Twoją przeglądarką jest <b>{user_agent}</b></p><h2>Header</h2><p>{headers}</p>"

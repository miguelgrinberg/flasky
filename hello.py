from flask import Flask
from flask import request, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, UTC

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/tmp/user/<name>')
def tmp(name):
    comments = ["Aaa...", "Bbb....", "Ccc..."]
    return render_template(
        '/tmp/info.html',
        user=name,
        comments=comments
    )


@app.route('/tmp/index')
def index_user():
    return render_template('/tmp/user.html', user="One Two")


@app.route('/browser')
def browser():
    user_agent = request.headers.get('User-Agent')
    # request_headers = dict(request.headers)
    headers = "<br>".join(map(': '.join, request.headers.items()))
    return f"<p>Twoją przeglądarką jest <b>{user_agent}</b></p><h2>Header</h2><p>{headers}</p>"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/time')
def show_time():
    return render_template('time.html', current_time=datetime.now(UTC))
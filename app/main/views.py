from flask import render_template
from . import main
from ..models import User, Loan_application


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/getuser')
def get_user():
    user = User.query.get(1)
    loan = Loan_application.query.get(1)
    return render_template('index.html')
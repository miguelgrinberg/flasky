from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length


class LoginForm(Form):
    # email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    mobile = StringField('mobile', validators=[Required(), Length(11, 11)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(Form):
    mobile = StringField('mobile', validators=[Required(), Length(11, 11)])
    password = PasswordField('Password', validators=[Required()])
    password_repeat = PasswordField('Password repeat', validators=[Required()])
    mobile_code = StringField('mobile_code', validators=[Required(), Length(1, 6)])
    submit = SubmitField('Register In')
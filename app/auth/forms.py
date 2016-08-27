from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length


class LoginForm(Form):
    # email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    mobile = StringField('手机号', validators=[Required(), Length(11, 11)])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')



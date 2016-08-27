from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Length


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class RegisterForm(Form):
    mobile = StringField('手机号', validators=[Required(), Length(11, 11)])
    password = PasswordField('密码', validators=[Required()])
    password_repeat = PasswordField('重复输入密码', validators=[Required()])
    mobile_code = StringField('手机验证码', validators=[Required(), Length(1, 6)])
    submit = SubmitField('注册')
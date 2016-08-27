from flask import render_template, request
from . import main
from .forms import RegisterForm
from flask_login import login_required


@main.route('/')  # 首页
def index():
    return render_template('index.html')


@main.route('/register')  # 注册
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(mobile=form.mobile.data).first()
        # if user is not None and user.verify_password(form.password.data):
        # login_user(user, form.remember_me.data)
        # return redirect(request.args.get('next') or url_for('main.index'))
        flash('手机号或密码无效')
    return render_template('register.html', form=form)


@main.route('/verify_mobile')  # 验证手机号
def verify_mobile():
    mobile = request.get("mobile")
    print(mobile)
    return None


@main.route('/userInfo')  # 用户信息
@login_required
def userInfo():
    return None


@main.route('/userInfo/edit')  # 用户信息修改
@login_required
def userInfo_edit():
    return None


@main.route('/find/password')  # 用户密码找回
@login_required
def find_password():
    return None


@main.route('/find/withdraw_password')  # 用户提现密码找回
@login_required
def find_withdraw_password():
    return None



@main.route('/loan_apply/info')  # 申请资料查看
@login_required
def loan_apply_info():
    return None


@main.route('/loan_apply/upload')  # 申请资料上传
@login_required
def loan_apply_upload():
    return None


@main.route('/loan_apply/amount')  # 申请状态额度
@login_required
def loan_apply_amount():
    return None


# @main.route('/getuser')
# def get_user():
#     user = User.query.get(1)
#     loan = Loan_application.query.get(1)
#     return render_template('index.html')
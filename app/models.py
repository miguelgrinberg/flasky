from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


# user model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(64), unique=True, index=True)  # 用户名
    password_hash = db.Column(db.String(128))  # 密码
    withdraw_password = db.Column(db.String(128))  # 提现密码
    # bank_account = db.Column(db.String(128)) #银行账号
    mobile = db.Column(db.String(20))  # 手机号
    address = db.Column(db.String(128))  # 居住地地址

    loan_applicaitons = db.relationship('Loan_application', backref='user', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# loan applicaiton
class Loan_application(db.Model):
    __tablename__ = 'loan_application'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 外键关联 用户id
    apply_name = db.Column(db.String(64))  # 申请人
    gender = db.Column(db.SmallInteger)  # 性别 0：先生 1：女士
    marriage_status = db.Column(db.SmallInteger)  # 婚姻状况 0：未婚 1：已婚 2：离异
    apply_identi = db.Column(db.String(20))  # 身份证号
    bank_name = db.Column(db.String(128))  # 银行名称
    bank_account = db.Column(db.String(30))  # 银行账号
    company_address = db.Column(db.String(20))  # 单位地址
    company_mobile = db.Column(db.String(20))  # 单位电话
    urgent_contacter1 = db.Column(db.String(128))  # 紧急联系人1
    urgent_contacter2 = db.Column(db.String(128))  # 紧急联系人2
    image1 = db.Column(db.String(128))  # 本人手持证件照
    image2 = db.Column(db.String(128))  # 身份证正面照
    image3 = db.Column(db.String(128))  # 身份证正面照
    image4 = db.Column(db.String(128))  # 证明材料
    apply_status = db.Column(db.SmallInteger)  # 审核状态 0：待审核 1：未通过 2：通过
    loan_amount = db.Column(db.Integer)
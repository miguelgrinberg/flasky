#-*-coding:utf-8-*-
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
###########显示个中文真难啊。。。

import os
from werkzeug import secure_filename
from flask import render_template, redirect, url_for, abort, flash, request, current_app, send_from_directory,jsonify
from flask_login import login_required, current_user, login_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, LoginForm, SelectClassForm, isSelectClassForm
from .. import db
from ..models import Role, User, Class, registrations
from ..decorators import admin_required
from ..checkname import allowed_file



@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效的用户名或密码.')
    return render_template('index.html', form=form)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit-profile/<nickname>', methods=['GET', 'POST'])
@login_required
def edit_profile(nickname):
    user = User.query.filter_by(username=nickname).first_or_404()
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('你的个人信息已更新.')
        return redirect(url_for('.user', username=nickname))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('个人信息已更新.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

#######test##########################################
html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>photeo up</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=up>
    </form>
    '''
#######test##########################################


@main.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
        app = current_app._get_current_object()
        if request.method == 'POST':
            file = request.files['file']
            fname = file.filename
            if file and allowed_file(fname):
                filename = secure_filename(fname)
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
                #file.filename = '{}_{}'.format(current_user.username, file.filename)   
                file.save('/{}/{}_{}'.format(UPLOAD_FOLDER, current_user.username, fname))
                current_user.avatar = '../static/avatar/{}_{}'.format(current_user.username, file.filename)
                db.session.add(current_user)
                flash('头像已更新')
                return redirect(url_for('.user', username=current_user.username))
        return render_template('upload_file.html')


@main.route('/selectclass', methods=['GET','POST'])
def selectclass():
    username=current_user.username
    user = User.query.filter_by(username=username).first()
    form = SelectClassForm()
    form1 = isSelectClassForm()
    classes = Class.query.all()
    classesed = user.classes.all()
    if request.method == 'POST':

        ids=request.form.get('a', 0)
        print ids
        classesing = Class.query.filter_by(id=ids).first_or_404()
        user.classes.append(classesing)
        db.session.add(user)
        flash('您已选课成功！')

        return redirect(url_for('.selectclass'))
    return render_template('selectclass.html', classes=classes, form=form, form1=form1, classesed=classesed)


@main.route('/selectedclass/<username>', methods=['GET','POST'])
def selectedclass(username):
    user = User.query.filter_by(username=username).first_or_404()
    classesed = user.classes.all()
    return render_template('selected_class.html', classesed=classesed)


@main.route('/guoziliangpage')
def guopage():
    return render_template('guoziliang.html')

@main.route('/calculator')
def calculator():
    return render_template('calculator.html')










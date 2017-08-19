#coding=utf-8
from flask import Blueprint, render_template, redirect, flash,url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField

from config import app

moment = Moment(app)
bootstrap = Bootstrap(app)
api_blueprint = Blueprint('api', __name__)

class NameForm(FlaskForm):
    # WTF表单，填写用户名和密码
    name = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('Submit')

@api_blueprint.route('/login',methods=['GET','POST'])
def login():
    # 登陆页面
    form = NameForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        if username == u'admin' and password == u'admin':
            # 正确用户名和密码跳转至/manage/main
            return redirect(url_for('manage.manage',username=username))
        else:
            flash('Wrong password or Wrong username')
    return render_template('index.html', form=form)

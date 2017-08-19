# coding=utf-8
import datetime
from flask import Blueprint, request,redirect,url_for,session,render_template
from config import db
from models import LoginTrack

manage_blueprint = Blueprint('manage', __name__)


@manage_blueprint.route('/main',methods=['GET','POST'])
def manage():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    username = request.args.get('username')
    args = {
                "ip" : ip,
                "ua" : ua,
                "time" : datetime.datetime.now(),
                "status" : 1,
                "username":username
            }
    # 先查询是否有相同UA，IP的设备在线，如果有，则此次登陆更新为最新在线状态，其他登陆下线
    history = db.session.query(LoginTrack).filter(LoginTrack.user_name == username,LoginTrack.ip == ip,
                                                  LoginTrack.user_agent == ua)
    for each in history:
        each.status = 0
    login_his = LoginTrack(**args)
    db.session.add(login_his)
    session['username'] = username
    return redirect(url_for('manage.dashboard',username=request.args.get('username')))


@manage_blueprint.route('/dashboard',methods=['GET','POST'])
def dashboard():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    username = session.get('username')
    # 查询该设备是否处于在线状态
    check = db.session.query(LoginTrack).filter(LoginTrack.user_name == username, LoginTrack.ip == ip,
                                                LoginTrack.user_agent == ua,LoginTrack.status == 1).all()
    # 所有在线设备数据
    data = db.session.query(LoginTrack).filter(LoginTrack.user_name == username, LoginTrack.ip == ip,
                                                  LoginTrack.status==1).all()
    # 所有登陆历史数据
    login_history = db.session.query(LoginTrack).filter(LoginTrack.user_name == username, LoginTrack.ip == ip,
                                                        LoginTrack.status == 0).all()
    if check:
        return render_template('dashborad.html',history=login_history,online=data)
    return redirect(url_for('api.login')),302

@manage_blueprint.route('/offline/<id>',methods=['GET'])
def offline(id):
    # 注销操作，然后跳转到dashboard
    data = LoginTrack.query.get(id)
    data.status = 0
    return redirect(url_for("manage.dashboard"))
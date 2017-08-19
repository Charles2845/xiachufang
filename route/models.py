# coding=utf-8
from config import db

class LoginTrack(db.Model):
    __tablename__ = 'login_track'
    id = db.Column(db.Integer,primary_key=True)
    ip = db.Column(db.String(100))
    user_name = db.Column(db.String(100))
    user_agent = db.Column(db.Text)
    time = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    def __init__(self,**kwargs):
        self.ip = kwargs.get('ip')
        self.user_name = kwargs.get('username')
        self.user_agent = kwargs.get('ua')
        self.time = kwargs.get('time')
        self.status = kwargs.get('status')          # 0为下线，1为在线

    def toJson(self):
        return dict((c.name,
                     getattr(self, c.name))
                     for c in self.__table__.columns)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/xiachufang'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'hard to guess string'
db = SQLAlchemy(app)

from route.login import api_blueprint
from route.manage import manage_blueprint
app.register_blueprint(api_blueprint,url_prefix='/api')
app.register_blueprint(manage_blueprint,url_prefix='/manage')




# _*_ coding:utf-8 _*_
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# init flask app
app = Flask(__name__)
app.config.from_object('config')

# init db
db = SQLAlchemy(app)

# init flask-Login
lm = LoginManager()
lm.setup_app(app)

from app import views, models

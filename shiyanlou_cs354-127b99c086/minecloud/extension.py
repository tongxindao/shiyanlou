#!/usr/bin/env python
# encoding: utf-8

# from .app import app
from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)
db = SQLAlchemy()

from flask_cache import Cache
cache = Cache()

from flask_login import LoginManager
login_manager = LoginManager()

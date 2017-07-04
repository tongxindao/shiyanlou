#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from .config import FlaskConfig
from .extension import db, cache, login_manager
from .host import host
from .image import image
from .template import template
from .user import User, user
from .frontend import frontend
from .virtualmachine import virtualmachine

app = Flask(__name__)
app.config.from_object(FlaskConfig)

# register blueprints
DEFAULT_BLUEPRINTS = (
    host,
    user,
    frontend,
    image,
    template,
    virtualmachine
)

for blueprint in DEFAULT_BLUEPRINTS:
    app.register_blueprint(blueprint)

# Config SQLAlchemy object
# flask-sqlalchemy
db.init_app(app)

# Update Flask-login config
login_manager.login_view = 'frontend.login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

login_manager.setup_app(app)

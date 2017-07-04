#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column
from ..extension import db
from .constants import HOST_OK

class Host(db.Model):
    __tablename__ = 'hosts'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(128), nullable=False, unique=True)
    username = Column(db.String(32), default='shiyanlou')
    password = Column(db.String(32), default='shiyanlou')
    vms = db.relationship('VirtualMachine', backref='host', lazy='dynamic')
    ip = Column(db.String(32), default='127.0.0.1')
    status_code = Column(db.SmallInteger, default=HOST_OK)

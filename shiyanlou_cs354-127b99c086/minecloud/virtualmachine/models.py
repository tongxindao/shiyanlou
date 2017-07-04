# _*_ coding: utf-8 _*_

from sqlalchemy import Column, ForeignKey
from ..extension import db
from datetime import datetime
from .constants import VM_SHUTDOWN

class VirtualMachine(db.Model):
    __tablename__ = 'virtualmachines'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(128), nullable=False, unique=True)
    template_id = Column(db.Integer, db.ForeignKey('templates.id'))
    owner_id = Column(db.Integer, db.ForeignKey('users.id'))
    host_id = Column(db.Integer, db.ForeignKey('hosts.id'))
    owner = Column(db.String(16), db.ForeignKey('users.name'))
    create_time = Column(db.DateTime)
    status_code = Column(db.SmallInteger, default=VM_SHUTDOWN)

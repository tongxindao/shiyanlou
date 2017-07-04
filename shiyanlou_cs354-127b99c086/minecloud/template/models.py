# _*_ coding: utf-8 _*_

from sqlalchemy import Column, ForeignKey
from ..extension import db

class Template(db.Model):
    __tablename__ = 'templates'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(128), nullable=False, unique=True)
    cpu_number = Column(db.SmallInteger)
    mem_size = Column(db.Integer) 
    image_id = Column(db.Integer, db.ForeignKey('images.id')) 
    user_id = Column(db.Integer, db.ForeignKey('users.id')) 

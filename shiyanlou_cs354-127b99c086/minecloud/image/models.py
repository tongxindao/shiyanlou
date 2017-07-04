# _*_ coding: utf-8 _*_

from sqlalchemy import Column, ForeignKey
from ..extension import db

class Image(db.Model):
    __tablename__ = 'images'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), nullable=False, unique=True)
    path = Column(db.String(128), nullable=False) 
    user_id = Column(db.Integer, db.ForeignKey('users.id')) 

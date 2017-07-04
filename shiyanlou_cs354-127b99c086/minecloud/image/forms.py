#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import FlaskForm
from wtforms import (TextField, SubmitField, IntegerField)

class AddImageForm(FlaskForm):
    name = TextField(u'镜像名')
    path = TextField(u'镜像路径')

    submit = SubmitField(u'添加')

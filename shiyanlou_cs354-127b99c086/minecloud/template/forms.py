#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import FlaskForm
from wtforms import (TextField, SubmitField, IntegerField)

class AddTemplateForm(FlaskForm):
    name = TextField(u'模板名')
    image_id = TextField(u'镜像ID')
    cpu_number = TextField(u'CPU数量')
    mem_size = TextField(u'内存大小')

    submit = SubmitField(u'添加')

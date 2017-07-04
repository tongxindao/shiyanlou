#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import FlaskForm
from wtforms import (TextField, SubmitField, IntegerField)

class AddHostForm(FlaskForm):
    name = TextField(u'服务器名')
    username = TextField(u'用户名')

    password = TextField(u'密码')
    # status_code = IntegerField(u'状态码')

    submit = SubmitField(u'添加')

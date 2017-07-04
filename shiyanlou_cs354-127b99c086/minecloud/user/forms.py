#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import FlaskForm
from wtforms import (TextField, SubmitField, IntegerField)

class AddUserForm(FlaskForm):
    name = TextField(u'用户名')
    password = TextField(u'密码')
    type_code = IntegerField(u'类型')

    submit = SubmitField(u'添加')

#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import FlaskForm
from wtforms import (TextField, SubmitField, IntegerField)

class AddVirtualMachineForm(FlaskForm):
    name = TextField(u'虚拟机名')
    template_id = TextField(u'模板ID')
    owner = TextField(u'所有者')
    # status_code = IntegerField(u'虚拟机状态')

    submit = SubmitField(u'添加')

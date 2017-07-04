#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import FlaskForm
from wtforms import (TextField, SubmitField, HiddenField, PasswordField)
from wtforms.validators import Required, Length

class LoginForm(FlaskForm):
    next = HiddenField()
    login = TextField(u'用户名', [Required()])
    password = PasswordField('密码', [Required(), Length(6,18)])
    submit = SubmitField('登录')

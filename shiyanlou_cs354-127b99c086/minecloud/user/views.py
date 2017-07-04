#! /usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as APP
from flask_login import login_required
from .forms import AddUserForm
from .models import User
from ..decorators import admin_required
from ..extension import db

import sys
reload(sys)
sys.setdefaultencoding('utf8')

user = Blueprint('user', __name__, url_prefix='/users')

@user.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template(('user/index.html'))

@user.route('/admin', methods=['GET'])
@login_required
@admin_required
def admin():
    form = AddUserForm()
    users = User.query.filter().all()
    return render_template("user/admin.html", users=users, form=form)
    
@user.route('/<int:user_id>/delete', methods=['GET'])
@login_required
@admin_required
def delete_user(user_id):
    user_instance = User.query.filter(User.id==user_id).first()
    if user_instance:
        db.session.delete(user_instance)
        db.session.commit()
    return redirect(url_for('user.admin'))

@user.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'GET':
        form = AddUserForm()
        user_list = User.query.filter().all()
        return render_template("user/admin.html", form=form, user_list=user_list)
    else:
        form = AddUserForm(request.form)
        if form.validate_on_submit():
            user_instance = User()
            form.populate_obj(user_instance)
            db.session.add(user_instance)
            db.session.commit()
        return redirect(url_for('user.admin'))

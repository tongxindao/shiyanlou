#! /usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as APP
from .forms import AddTemplateForm
from .models import Template
from ..extension import db

import sys
reload(sys)
sys.setdefaultencoding('utf8')

template = Blueprint('template', __name__, url_prefix='/templates')

@template.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        form = AddTemplateForm()
        template_list = Template.query.filter().all()
        return render_template("template/index.html", form=form, template_list=template_list)
    else:
        form = AddTemplateForm(request.form)
        if form.validate_on_submit():
            template_instance = Template()
            form.populate_obj(template_instance)
            db.session.add(template_instance)
            db.session.commit()
        return redirect(url_for('template.index'))

@template.route('/<int:template_id>/delete', methods=['GET'])
def delete_template(template_id):
    template_instance = Template.query.filter(Template.id==template_id).first()
    if template_instance:
        db.session.delete(template_instance)
        db.session.commit()
    return redirect(url_for('template.index'))

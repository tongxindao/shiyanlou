#! /usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as APP
from .forms import AddImageForm
from .models import Image
from ..extension import db

import sys
reload(sys)
sys.setdefaultencoding('utf8')

image = Blueprint('image', __name__, url_prefix='/images')

@image.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        form = AddImageForm()
        image_list = Image.query.filter().all()
        return render_template("image/index.html", form=form, image_list=image_list)
    else:
        form = AddImageForm(request.form)
        if form.validate_on_submit():
            image_instance = Image()
            form.populate_obj(image_instance)
            db.session.add(image_instance)
            db.session.commit()
        return redirect(url_for('image.index'))

@image.route('/<int:image_id>/delete', methods=['GET'])
def delete_image(image_id):
    image_instance = Image.query.filter(Image.id==image_id).first()
    if image_instance:
        db.session.delete(image_instance)
        db.session.commit()
    return redirect(url_for('image.index'))

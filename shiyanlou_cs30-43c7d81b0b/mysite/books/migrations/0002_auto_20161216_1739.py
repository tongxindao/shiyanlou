# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publisher',
            options={'ordering': ['name']},
        ),
    ]

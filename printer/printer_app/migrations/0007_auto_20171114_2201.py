# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-14 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer_app', '0006_auto_20171114_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='uploaded',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

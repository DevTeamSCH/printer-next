# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer_app', '0004_auto_20161024_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
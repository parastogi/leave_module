# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_auto_20170828_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default='True'),
        ),
    ]
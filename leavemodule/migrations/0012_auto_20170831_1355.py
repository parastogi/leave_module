# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leavemodule', '0011_auto_20170830_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='pf_in',
            field=models.IntegerField(),
        ),
    ]

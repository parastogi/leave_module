# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_auto_20170828_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=50)),
                ('hod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.User')),
            ],
        ),
    ]
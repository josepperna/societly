# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-05 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20190304_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='year',
            field=models.CharField(choices=[('1', 'Freshman'), ('2', 'Sophomore'), ('3', 'Junior'), ('4', 'Senior'), ('5', 'Postgraduate')], default='1', max_length=1),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0021_auto_20170813_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='debateteam',
            name='flags',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

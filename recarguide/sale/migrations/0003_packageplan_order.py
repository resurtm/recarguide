# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sale', '0002_auto_20171013_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='packageplan',
            name='order',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
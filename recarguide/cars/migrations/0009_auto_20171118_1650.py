# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-18 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cars', '0008_trim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trim',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='trim',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
    ]
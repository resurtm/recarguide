# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-18 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cars', '0006_auto_20171104_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='make',
            name='facebook',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='make',
            name='in_since',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='make',
            name='instagram',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='make',
            name='out_since',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='make',
            name='twitter',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='make',
            name='website',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='make',
            name='youtube',
            field=models.CharField(default='', max_length=250),
        ),
    ]

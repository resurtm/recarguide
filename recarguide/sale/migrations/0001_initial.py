# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 08:43
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0002_auto_20171013_0843'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackagePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('slug', models.SlugField(default='')),
                ('price', models.PositiveIntegerField(default=0)),
                ('max_listings', models.PositiveSmallIntegerField(default=0)),
                ('max_photos', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SellProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(default=None, null=True,
                                          on_delete=django.db.models.deletion.PROTECT,
                                          to='cars.Car')),
                ('user', models.ForeignKey(default=None,
                                           on_delete=django.db.models.deletion.PROTECT,
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
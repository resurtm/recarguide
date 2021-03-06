# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-10 08:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=250)),
                ('slug', models.SlugField(default='', max_length=250)),
                ('trim_name', models.CharField(default='', max_length=100)),
                ('price', models.PositiveIntegerField(default=0)),
                ('year', models.PositiveSmallIntegerField(default=0)),
                ('mileage', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(default='', max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('slug', models.SlugField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('slug', models.SlugField(default='')),
                ('website', models.CharField(default='', max_length=250)),
                ('facebook', models.CharField(default='', max_length=250)),
                ('twitter', models.CharField(default='', max_length=250)),
                ('youtube', models.CharField(default='', max_length=250)),
                ('instagram', models.CharField(default='', max_length=250)),
                ('in_since', models.PositiveIntegerField(default=0)),
                ('out_since', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('slug', models.SlugField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ready', models.BooleanField(default=False)),
                ('uid', models.CharField(max_length=16)),
                ('filename', models.CharField(max_length=250)),
                ('filedata', models.TextField(default=None, null=True)),
                ('car', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='photos', to='cars.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Trim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('make', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cars.Make')),
                ('model', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cars.Model')),
            ],
        ),
    ]

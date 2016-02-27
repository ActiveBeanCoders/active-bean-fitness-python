# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160222235923 on 2016-02-23 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('userId', models.BigIntegerField()),
                ('activity', models.CharField(max_length=256)),
                ('date', models.DateTimeField()),
                ('unit', models.CharField(max_length=32)),
                ('distance', models.DecimalField(decimal_places=4, max_digits=10)),
                ('comment', models.CharField(max_length=4000)),
                ('distHour', models.IntegerField(default=0)),
                ('distMin', models.IntegerField(default=0)),
                ('distSec', models.IntegerField(default=0)),
            ],
        ),
    ]

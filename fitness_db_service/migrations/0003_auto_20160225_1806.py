# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160222235923 on 2016-02-26 01:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_db_service', '0002_auto_20160223_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainUser',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('comma_separated_roles', models.TextField()),
                ('nickname', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'domain_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DomainUserCredentials',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('password_hash', models.CharField(blank=True, max_length=255, null=True)),
                ('salt', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'domain_user_credentials',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='activity',
            options={'managed': False},
        ),
    ]

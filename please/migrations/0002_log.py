# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-24 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('please', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logtext', models.TextField(default='')),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-16 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='title',
        ),
        migrations.AddField(
            model_name='answer',
            name='person',
            field=models.CharField(default=b'Tanjil', max_length=50),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(max_length=200),
        ),
    ]

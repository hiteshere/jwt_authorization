# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-23 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180823_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='resume',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]

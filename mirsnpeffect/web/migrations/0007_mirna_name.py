# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-23 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20180122_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='mirna',
            name='name',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-18 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20171205_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='genome',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.GenomeVersion'),
        ),
    ]
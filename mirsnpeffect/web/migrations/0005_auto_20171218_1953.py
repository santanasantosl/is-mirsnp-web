# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-18 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_gene_genome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gene',
            name='band',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

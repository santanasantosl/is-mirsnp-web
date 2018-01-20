# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-05 03:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DbSNP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hugo', models.CharField(max_length=50)),
                ('chr', models.CharField(max_length=5)),
                ('start_pos', models.PositiveIntegerField()),
                ('end_pos', models.PositiveIntegerField()),
                ('strand', models.CharField(max_length=1, null=True)),
                ('band', models.CharField(max_length=10, null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneSynonym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('synonym', models.CharField(max_length=100)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='GeneTranscript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript_id', models.CharField(max_length=30, null=True)),
                ('transcript_version', models.PositiveIntegerField(blank=True, null=True)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='GenomeVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('fasta', models.FileField(null=True, upload_to=b'')),
                ('gtf', models.FileField(null=True, upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Mirbase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=10)),
                ('fasta', models.FileField(null=True, upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='MiRNA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chr', models.CharField(max_length=5)),
                ('start_pos', models.PositiveIntegerField()),
                ('end_pos', models.PositiveIntegerField()),
                ('strand', models.CharField(max_length=1, null=True)),
                ('mirbase_acc', models.CharField(max_length=30, null=True)),
                ('mirbase_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Mirbase')),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_mfe', models.FloatField()),
                ('ref_mfe_pval', models.FloatField()),
                ('alt_mfe', models.FloatField()),
                ('alt_mfe_pval', models.FloatField()),
                ('pval_log_ratio', models.FloatField()),
                ('log_ratio_pval', models.FloatField()),
                ('type', models.CharField(blank=True, choices=[('FULL_MIRNA', 'FULL_MIRNA'), ('SEED_7MER', '7MER_SEED'), ('SEED_8MER', '8MER_SEED')], max_length=10, null=True)),
                ('is_significant', models.BooleanField()),
                ('mirna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.MiRNA')),
            ],
        ),
        migrations.CreateModel(
            name='TranscriptAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=20)),
                ('chr', models.CharField(max_length=5)),
                ('start_pos', models.PositiveIntegerField()),
                ('end_pos', models.PositiveIntegerField()),
                ('strand', models.CharField(max_length=1, null=True)),
                ('transcript', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.GeneTranscript')),
            ],
        ),
        migrations.CreateModel(
            name='TranscriptDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('version', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chr', models.CharField(max_length=5)),
                ('start_pos', models.PositiveIntegerField()),
                ('end_pos', models.PositiveIntegerField()),
                ('ref', models.CharField(max_length=30)),
                ('alt', models.CharField(max_length=30)),
                ('strand', models.CharField(max_length=1, null=True)),
                ('rsid', models.CharField(max_length=30, null=True)),
                ('dbsnp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.DbSNP')),
                ('genome_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.GenomeVersion')),
            ],
        ),
        migrations.CreateModel(
            name='VariantAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript_annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.TranscriptAnnotation')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Variant')),
            ],
        ),
        migrations.AddField(
            model_name='prediction',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Variant'),
        ),
        migrations.AddField(
            model_name='genetranscript',
            name='transcript_db',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.TranscriptDB'),
        ),
        migrations.AddField(
            model_name='dbsnp',
            name='genome_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.GenomeVersion'),
        ),
    ]
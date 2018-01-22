# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage


class GenomeVersion(models.Model):
    name = models.CharField(max_length=10)
    fasta = models.FileField(null=True)
    gtf = models.FileField(null=True)


# Create your models here.
class Gene(models.Model):

    hugo = models.CharField(max_length=50)
    chr = models.CharField(max_length=5)
    start_pos = models.PositiveIntegerField()
    end_pos = models.PositiveIntegerField()
    ## Strand
    strand = models.CharField(max_length=1, null=True)
    ## Band
    band = models.CharField(max_length=20, null=True)
    ## description
    description = models.TextField(null=True)
    ## genome version
    genome = models.ForeignKey(GenomeVersion, null=True)


class GeneSynonym(models.Model):
    gene = models.ForeignKey(Gene)
    synonym = models.CharField(max_length=100)


class TranscriptDB(models.Model):
    name = models.CharField(max_length=30)
    version = models.CharField(max_length=10)


class GeneTranscript(models.Model):
    gene = models.ForeignKey(Gene)
    transcript_id = models.CharField(max_length=30, null=True)
    transcript_version = models.PositiveIntegerField(null=True, blank=True)
    transcript_db = models.ForeignKey(TranscriptDB)


class TranscriptAnnotation(models.Model):
    region = models.CharField(max_length=20)
    chr = models.CharField(max_length=5)
    start_pos = models.PositiveIntegerField()
    end_pos = models.PositiveIntegerField()
    ## Strand
    strand = models.CharField(max_length=1, null=True)
    transcript = models.ForeignKey(GeneTranscript)


class Mirbase(models.Model):
    version = models.CharField(max_length=10)
    fasta = models.FileField(null=True)


class MiRNA(models.Model):
    chr = models.CharField(max_length=5)
    start_pos = models.PositiveIntegerField()
    end_pos = models.PositiveIntegerField()
    ## Strand
    strand = models.CharField(max_length=1, null=True)
    mirbase_acc = models.CharField(max_length=30, null=True)
    mirbase_version = models.ForeignKey(Mirbase)


class DbSNP(models.Model):
    version = models.CharField(max_length=10)
    genome_version = models.ForeignKey(GenomeVersion)


class Variant(models.Model):
    chr = models.CharField(max_length=5)
    start_pos = models.PositiveIntegerField()
    end_pos = models.PositiveIntegerField()
    ref = models.CharField(max_length=30)
    alt = models.CharField(max_length=30)
    gene = models.ForeignKey(Gene, null=True)
    annotation = models.ForeignKey(TranscriptAnnotation, null=True)
    ## Strand
    strand = models.CharField(max_length=1, null=True)
    rsid = models.CharField(max_length=30, null=True)
    genome_version = models.ForeignKey(GenomeVersion)
    dbsnp = models.ForeignKey(DbSNP, null=True)


class VariantAnnotation(models.Model):
    variant = models.ForeignKey(Variant)
    transcript_annotation = models.ForeignKey(TranscriptAnnotation)


class Prediction(models.Model):

    FULL = 'FULL_MIRNA'
    SEED7 = 'SEED_7MER'
    SEED8 = 'SEED_8MER'

    TYPE_CHOICES = (
        (FULL, 'FULL_MIRNA'),
        (SEED7, '7MER_SEED'),
        (SEED8, '8MER_SEED'),
    )

    variant = models.ForeignKey(Variant)
    mirna = models.ForeignKey(MiRNA)
    ref_mfe = models.FloatField()
    ref_mfe_pval = models.FloatField()
    alt_mfe = models.FloatField()
    alt_mfe_pval = models.FloatField()
    pval_log_ratio = models.FloatField()
    log_ratio_pval = models.FloatField()
    type = models.CharField(max_length=10, null=True, blank=True, choices=TYPE_CHOICES)
    is_significant = models.BooleanField()


class Job(models.Model):

    models.DateTimeField(auto_now_add=True)
    total_number_variants = models.PositiveIntegerField()
    number_3utr_variants = models.PositiveIntegerField()


class JobPrediction(models.Model):

    prediction = models.ForeignKey(Prediction)
    job = models.ForeignKey(Job)
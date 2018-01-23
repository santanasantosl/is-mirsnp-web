import os
import re
import django
django.setup()
from django.conf import settings
from web.models import DbSNP, Gene, GeneSynonym, GeneTranscript, GenomeVersion, Job, JobPrediction, MiRNA, Mirbase, Prediction, TranscriptAnnotation, TranscriptDB, Variant, VariantAnnotation


def load_snps(dbsnp_bed, genome, dbsnp_version):
    try:
        genome = GenomeVersion.objects.get(name=genome)
    except:
        genome = GenomeVersion(name=genome)
        genome.save()

    try:
        dbsnp = DbSNP.objects.get(version=dbsnp_version, genome_version=genome)
    except:
        dbsnp = DbSNP(version=dbsnp_version, genome_version=genome)
        dbsnp.save()

    dbsnp_fh = open(dbsnp_bed, 'r')
    for line in dbsnp_fh:
        line = line.strip()
        if not re.search('^track', line):
            fields = line.split('\t')
            chrom = fields[0]
            start_pos = int(fields[1])
            end_pos = int(fields[2])
            rsid = fields[3]
            strand = fields[4]
            print chrom + '\t' + str(start_pos) + '\t' + str(end_pos)

            try:
                gene = Gene.objects.get(chr=chrom,
                                        start_pos__gte=start_pos,
                                        end_pos__lte=end_pos,
                                        strand=strand)
                print rsid + '\t' + gene
            except:
                pass


def load_snps_from_vcf(dbsnp_vcf, genome, dbsnp_version):

    try:
        genome = GenomeVersion.objects.get(name=genome)
    except:
        genome = GenomeVersion(name=genome)
        genome.save()

    try:
        dbsnp = DbSNP.objects.get(version=dbsnp_version, genome_version=genome)
    except:
        dbsnp = DbSNP(version=dbsnp_version, genome_version=genome)
        dbsnp.save()

    dbsnp_fh = open(dbsnp_vcf, 'r')
    for line in dbsnp_fh:
        line = line.strip()
        if not re.search('^#', line):
            fields = line.split('\t')
            chrom = fields[0]
            start_pos = int(fields[1])
            rsid = fields[2]
            ref = fields[3]
            alt = fields[4].split(',')[0]
            end_pos = start_pos + len(alt) - 1

            strand = fields[7].split('|')[2].split('=')[0]
            #print chrom + '\t' + str(start_pos) + '\t' + str(end_pos) + '\t' + strand

            try:
                ta = TranscriptAnnotation.objects.filter(chr=chrom,
                                                         start_pos__lte=start_pos,
                                                         end_pos__gte=end_pos,
                                                         region='3UTR')
                print rsid + '\t' + str(ta.count())
            except:
                pass


def load_validation_data(validation_data, genome, dbsnp_version):

    try:
        genome = GenomeVersion.objects.get(name=genome)
    except:
        genome = GenomeVersion(name=genome)
        genome.save()

    try:
        dbsnp = DbSNP.objects.get(version=dbsnp_version, genome_version=genome)
    except:
        dbsnp = DbSNP(version=dbsnp_version, genome_version=genome)
        dbsnp.save()

    validation_data_fh = open(validation_data)
    for line in validation_data_fh:
        line = line.strip()
        if not re.search('^SNP_ID', line):
            fields = line.split('\t')
            mirna = fields[5]

            try:
                mirna_obj = MiRNA.objects.get(name=mirna)
            except:
                mirna_obj = None

            try:
                variant = Variant.objects.get(chr=fields[1], start_pos=int(fields[2]), ref=fields[3], alt=fields[4])
            except:
                variant = Variant(chr=fields[1], start_pos=fields[2], end_pos=int(fields[2])+len(fields[3])-1,
                                  ref=fields[3], alt=fields[4], rsid=fields[0], dbsnp=dbsnp, genome_version=genome)
                variant.save()

            if mirna_obj and variant:
                try:
                    prediction = Prediction.objects.get(variant=variant, mirna=mirna_obj)
                except:
                    prediction_type = fields[12]

                    if prediction_type == 'full_miRNA':
                        prediction_type = 'FULL'
                    elif prediction_type == '7mer_seed':
                        prediction_type = 'SEED7'
                    elif prediction_type == '8mer_seed':
                        prediction_type = 'SEED8'

                    significant = False

                    if fields[13] == 'YES':
                        significant = True

                    prediction = Prediction(variant=variant, mirna=mirna_obj, ref_mfe=fields[6],
                                            ref_mfe_pval=fields[7], alt_mfe=fields[8], alt_mfe_pval=fields[9],
                                            pval_log_ratio=fields[10], log_ratio_pval=fields[11],
                                            type=prediction_type, is_significant=significant)
                    prediction.save()


if __name__ == "__main__":

    vcf_file = os.path.join(settings.MEDIA_ROOT, 'dbsnp_147.3utr.hg19.annotated.vcf')
    #load_snps_from_vcf(vcf_file, 'hg19', '147')
    validation_data = os.path.join(settings.MEDIA_ROOT, 'validation_results.txt')
    load_validation_data(validation_data, 'hg19', '147')
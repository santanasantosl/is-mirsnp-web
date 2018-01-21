import os
import re
import django
django.setup()
from django.conf import settings
from web.models import DbSNP, Gene, GeneSynonym, GeneTranscript, GenomeVersion, Job, JobPrediction, MiRNA, Mirbase, Prediction, TranscriptAnnotation, TranscriptDB, Variant, VariantAnnotation


def load_genomic_data(fixture_directory, genome):

    load_genes(fixture_directory, genome)


def load_genes(dir, genome):

    compiled_refseq_gene = compile_refseq_gene(dir)


    ## Create genome version
    try:
        genome_version = GenomeVersion.objects.get(name=genome)
    except:
        genome_version = GenomeVersion(name=genome)
        genome_version.save()

    ## Create TranscriptDB
    try:
        transcript_db = TranscriptDB.objects.get(name='refseq', version=1)
    except:
        transcript_db = TranscriptDB(name='refseq', version=1)
        transcript_db.save()

    refseq_gene_dict = dict()
    refseq_gene = os.path.join(dir, 'refseq_gene_hg19.txt')
    refseq_gene_fh = open(refseq_gene)

    for line in refseq_gene_fh:
        line = line.strip()
        if not re.search('^#', line):
            fields = line.split('\t')
            refseq_gene_dict[fields[0]] = fields[1]

    refseq_gene_fh.close()

    hgnc_dict = dict()
    hgnc_fn = os.path.join(dir, 'hgnc_complete_set.txt')
    hgnc_fh = open(hgnc_fn)

    counter = 1
    for line in hgnc_fh:
        line = line.strip()
        if counter > 1:
            fields = line.split('\t')
            gene_symbol = fields[1]
            description = fields[2]
            location = fields[6]
            status = fields[5]

            if status == 'Approved':
                hgnc_dict[gene_symbol] = description + '\t' + location

        counter += 1

    hgnc_fh.close()

    for gene in compiled_refseq_gene:
        data = compiled_refseq_gene[gene]
        fields = data.split('\t')
        chrom = fields[0]
        start_pos = int(fields[1])
        end_pos = int(fields[2])
        strand = fields[3]
        refseqs = fields[5].split(',')

        if hgnc_dict.has_key(gene):
            description = hgnc_dict[gene].split('\t')[0]
            band = hgnc_dict[gene].split('\t')[1]

            try:
                gene_obj = Gene.objects.get(chr=chrom, start_pos=start_pos,
                                            end_pos=end_pos, strand=strand,
                                            hugo=gene, band=band, description=description,
                                            genome=genome_version)
                for refseq in refseqs:
                    try:
                        gene_transcript = GeneTranscript.objects.get(gene=gene_obj, transcript_db=transcript_db,
                                                                     transcript_id=refseq)
                    except:
                        gene_transcript = GeneTranscript(gene=gene_obj, transcript_db=transcript_db,
                                                         transcript_id=refseq)
                        gene_transcript.save()

            except:
                try:
                    if len(band.split(' ')) > 1:
                        band = band.split(' ')[0]
                    gene_obj = Gene(chr=chrom, start_pos=start_pos, end_pos=end_pos, strand=strand, hugo=gene, band=band,
                                    description=description, genome=genome_version)
                    gene_obj.save()

                    for refseq in refseqs:
                        try:
                            gene_transcript = GeneTranscript.objects.get(gene=gene_obj, transcript_db=transcript_db,
                                                                         transcript_id=refseq)
                        except:
                            gene_transcript = GeneTranscript(gene=gene_obj, transcript_db=transcript_db,
                                                             transcript_id=refseq)
                            gene_transcript.save()

                except:
                    pass
                    #print band + '\t' + description + '\t' + data


def load_3utr_data(dir):

    utr3_fn = os.path.join(dir, 'refseq_hg19_3utr.bed')
    utr3_fh = open(utr3_fn)

    for line in utr3_fh:
        line = line.strip()
        fields = line.split('\t')
        chrom = fields[0]
        start_pos = fields[1]
        end_pos = fields[2]
        refseq_id = fields[3].split('_')[0] + '_' + fields[3].split('_')[1]
        strand = fields[4]
        #print refseq_id
        try:
            refseq_obj = GeneTranscript.objects.get(transcript_id=refseq_id)
            transcript_annotation = TranscriptAnnotation.objects.get(region='3UTR', chr=chrom,
                                                                     start_pos=start_pos, end_pos=end_pos,
                                                                     strand=strand, transcript=refseq_obj)
        except:
            try:
                refseq_obj = GeneTranscript.objects.get(transcript_id=refseq_id)
                transcript_annotation = TranscriptAnnotation(region='3UTR', chr=chrom,
                                                             start_pos=start_pos, end_pos=end_pos,
                                                             strand=strand, transcript=refseq_obj)
                print refseq_obj.id
                transcript_annotation.save()
            except:
                pass
            pass


def compile_refseq_gene(dir):

    refseq_gene_dict = dict()
    refseq_gene = os.path.join(dir, 'refseq_gene_hg19.txt')
    refseq_gene_fh = open(refseq_gene)

    for line in refseq_gene_fh:
        line = line.strip()
        if not re.search('^#', line):
            fields = line.split('\t')
            if not re.search('^NR', fields[0]):
                if refseq_gene_dict.has_key(fields[1]):
                    refseq_gene_dict[fields[1]].append(fields[0])

                else:
                    refseq_gene_dict[fields[1]] = list()
                    refseq_gene_dict[fields[1]].append(fields[0])

    refseq_hg19_genes_fn = os.path.join(dir, 'refseq_hg19_genes.bed')
    refseq_hg19_genes_fh = open(refseq_hg19_genes_fn)
    refseq_hg19_genes_dict = dict()

    for line in refseq_hg19_genes_fh:
        line = line.strip()
        fields = line.split('\t')
        chrom = fields[0]
        start_pos = fields[1]
        end_pos = fields[2]
        refseq = fields[3]
        strand = fields[5]

        if len(chrom.split('_')) == 1:

            refseq_hg19_genes_dict[refseq] = chrom + '\t' + start_pos + '\t' + end_pos + '\t' + strand
    refseq_hg19_genes_fh.close()

    gene_refseq = dict()

    for key in refseq_gene_dict.keys():
        refseqs = refseq_gene_dict[key]

        final_chrom = ''
        final_start_pos = 0
        final_end_pos = 0
        final_strand = ''

        if len(refseqs) > 1:
            for refseq in refseqs:
                if refseq_hg19_genes_dict.has_key(refseq):
                    refseq_data = refseq_hg19_genes_dict[refseq]
                    fields = refseq_data.split('\t')
                    chrom = fields[0]
                    start_pos = int(fields[1])
                    end_pos = int(fields[2])
                    strand = fields[3]
                    if final_start_pos == 0 and final_end_pos == 0:
                        final_chrom = chrom
                        final_start_pos = start_pos
                        final_end_pos = end_pos
                        final_strand = strand
                    else:
                        if start_pos < final_start_pos:
                            final_start_pos = start_pos
                        if end_pos > final_end_pos:
                            final_end_pos = end_pos

        else:
            if refseq_hg19_genes_dict.has_key(refseq):
                refseq_data = refseq_hg19_genes_dict[refseq]
                fields = refseq_data.split('\t')
                chrom = fields[0]
                start_pos = int(fields[1])
                end_pos = int(fields[2])
                strand = fields[3]

                final_chrom = chrom
                final_start_pos = start_pos
                final_end_pos = end_pos
                final_strand = strand
        gene_refseq[key] = final_chrom + '\t' + str(final_start_pos) + '\t' + str(final_end_pos) + '\t' + final_strand + '\t' + key + '\t' + ','.join(refseqs)

    return gene_refseq


if __name__ == "__main__":

    load_genomic_data(settings.MEDIA_ROOT, 'hg19')
    load_3utr_data(settings.MEDIA_ROOT)
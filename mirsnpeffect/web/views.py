# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tempfile
import os

from django.shortcuts import render
from web.models import Variant, Prediction
from mirsnpeffect.settings import MEDIA_ROOT, MEDIA_URL

# Create your views here.


def home(request):
    context = locals()
    template = 'home.html'
    return render(request, template, context)


def download(request):
    context = locals()
    template = 'download.html'
    return render(request, template, context)


def search(request):

    template = 'job.html'
    snps_not_in_database = []
    snps_outside_utr3 = []
    significant_predictions = []
    non_significant_predictions = []
    snps_without_predictions = []
    error_data =False
    results_link = ''

    if request.method == 'POST':
        form_data = request.POST.get('searchbox')
        split_data = form_data.split('\n')
        for rsid in split_data:
            rsid = rsid.strip()
            variant = Variant.objects.filter(rsid=rsid)
            if variant.count() == 0:
                snps_not_in_database.append(rsid)
            else:
                predictions = Prediction.objects.filter(variant=variant).order_by('variant__rsid')
                if len(predictions) > 0:
                    for prediction in predictions:
                        if prediction.is_significant:
                            significant_predictions.append(prediction)
                        else:
                            non_significant_predictions.append(prediction)
                else:
                    snps_without_predictions.append(variant)

        # Generate file with all predictions
        fd, outfile = tempfile.mkstemp('.txt', os.path.join(MEDIA_ROOT, 'results/'))
        outfile_handle = open(outfile, 'w')
        results_link = os.path.join('/', MEDIA_URL, 'results/' + outfile.split('/')[-1])

        # Print file header
        outfile_handle.write('SNPID\tCHROM\tPOS\tREF\tALT\tMIRNA\tREF_MFE\tREF_MFE_PVALUE\tALT_MFE\tALT_MFE_PVALUE\tPVAL_LOG_RATIO\tPVAL_OF_LOG_RATIO\tTYPE\tSIGNIFICANT\n')
        for pred in significant_predictions:
            outfile_handle.write(
                pred.variant.rsid + '\t' + pred.variant.chr + '\t' + str(pred.variant.start_pos) +
                '\t' + pred.variant.ref + '\t' + pred.variant.alt + '\t' + pred.mirna.name + '\t'
                + str(pred.ref_mfe) + '\t' + str(pred.ref_mfe_pval) + '\t' + str(pred.alt_mfe) + '\t'
                + str(pred.alt_mfe_pval) + '\t' + str(pred.pval_log_ratio) + '\t' + str(pred.log_ratio_pval) + '\t'
                + pred.type + '\t' + str(pred.is_significant) + '\n'
            )
        for pred in non_significant_predictions:
            outfile_handle.write(
                pred.variant.rsid + '\t' + pred.variant.chr + '\t' + str(pred.variant.start_pos) +
                '\t' + pred.variant.ref + '\t' + pred.variant.alt + '\t' + pred.mirna.name + '\t'
                + str(pred.ref_mfe) + '\t' + str(pred.ref_mfe_pval) + '\t' + str(pred.alt_mfe) + '\t'
                + str(pred.alt_mfe_pval) + '\t' + str(pred.pval_log_ratio) + '\t' + str(pred.log_ratio_pval) + '\t'
                + pred.type + '\t' + str(pred.is_significant) + '\n'
            )


        outfile_handle.close()

    else:
        error_data = True

    context = {'snps_not_in_database': snps_not_in_database,
               'snps_outside_utr3': snps_outside_utr3,
               'snps_without_predictions': snps_without_predictions,
               'significant_predictions': significant_predictions,
               'non_significant_predictions': non_significant_predictions,
               'error_data': error_data,
               'results_link': results_link}
    return render(request, template, context)
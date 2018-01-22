# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from web.models import Variant, Prediction

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

    if request.method == 'POST':
        form_data = request.POST.get('searchbox')
        split_data = form_data.split('\n')
        for rsid in split_data:
            variant = Variant.objects.filter(rsid=rsid)
            if variant.count() == 0:
                snps_not_in_database.append(rsid)
            else:
                variant = Variant.objects.filter(rsid=rsid, annotation__region='UTR3')
                if len(variant) == 0:
                    snps_outside_utr3.append(variant)

                else:
                    predictions = Prediction.objects.filter(variant=variant, is_signficant=True)
                    if len(predictions) > 0:
                        for prediction in predictions:
                            if prediction.is_significant:
                                significant_predictions.append(prediction)
                            else:
                                non_significant_predictions.append(prediction)
                    else:
                        snps_without_predictions.append(variant)

    else:
        form_data = 'No prediction were found for the submitted list of SNPs. Please, check your input'

    context = {'snps_not_in_database': snps_not_in_database,
               'snps_outside_utr3': snps_outside_utr3,
               'snps_without_predictions': snps_without_predictions,
               'significant_predictions': significant_predictions,
               'non_significant_predictions': non_significant_predictions}
    return render(request, template, context)
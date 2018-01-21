# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.

def home(request):
    context = locals()
    template = 'home.html'
    return render(request, template, context)


def job(request):
    context = locals()
    template = 'job.html'
    return render(request, template, context)


def download(request):
    context = locals()
    template = 'download.html'
    return render(request, template, context)
from django.http import Http404
from django.shortcuts import render

from recarguide.cars.models import Car


def step1(request):
    return render(request, 'sale/step1.html')

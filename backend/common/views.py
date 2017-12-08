from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from cars.models import Make


def home(request):
    print(settings.STRIPE)
    return HttpResponse('test')
    popular_makes = Make.objects.find_popular_makes()
    return render(request, 'common/home.html', {
        'popular_makes': popular_makes,
    })

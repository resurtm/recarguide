from django.shortcuts import render

from cars.models import Make


def home(request):
    popular_makes = Make.objects.find_popular_makes()
    return render(request, 'common/home.html', {
        'popular_makes': popular_makes,
    })

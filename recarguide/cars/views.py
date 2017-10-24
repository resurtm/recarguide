from django.http import Http404
from django.shortcuts import render

from recarguide.cars.models import Car


def view(request, slug, id):
    try:
        car = Car.objects.get(id=id)
        if car.slug != slug:
            raise Car.DoesNotExist()
    except Car.DoesNotExist:
        raise Http404('Requested car does not exist')
    return render(request, 'cars/view.html', {'car': car})


def search(request):
    return render(request, 'cars/search.html')

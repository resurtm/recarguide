from django.http import Http404
from django.shortcuts import render

import recarguide.cars.elasticsearch as es
from recarguide.cars.facetedsearch import FacetedSearch
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
    search = FacetedSearch(request.GET)

    body = {
        'query': {
            'term': {
                '_all': 'land',
            },
        },
    }

    es.ensure_es()
    result = es.es.search(index='recarguide_car',
                          doc_type='recarguide_car_type',
                          body=body)

    print(result)

    return render(request, 'cars/search.html')

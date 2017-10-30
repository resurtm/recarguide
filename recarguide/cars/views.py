from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from recarguide.cars.models import Car
from recarguide.cars.search.faceted import FacetedSearch, PAGE_SIZE
from recarguide.cars.search.source import CarSource


def view(request, slug, id):
    try:
        car = Car.objects.get(id=id)
        if car.slug != slug:
            raise Car.DoesNotExist()
    except Car.DoesNotExist:
        raise Http404('Requested car does not exist')
    return render(request, 'cars/view.html', {'car': car})


def search(request):
    fsearch = FacetedSearch(request.GET)
    source = CarSource(fsearch)

    paginator = Paginator(source, PAGE_SIZE)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    if page <= 0 or page > paginator.num_pages:
        raise Http404
    cars = paginator.page(page)
    source.page = page

    return render(request, 'cars/search.html', {'cars': cars,
                                                'fsearch': fsearch,
                                                'source': source,
                                                'paginator': paginator})

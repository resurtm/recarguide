from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from recarguide.cars.models import Car
from recarguide.cars.search import QueryBuilder, CarSource, PAGE_SIZE


def view(request, slug, id):
    try:
        car = Car.objects.get(id=id)
        if car.slug != slug:
            raise Car.DoesNotExist()
    except Car.DoesNotExist:
        raise Http404('Requested car does not exist')
    return render(request, 'cars/view.html', {'car': car})


def search(request):
    source = CarSource(QueryBuilder(request.GET))
    pager = Paginator(source, PAGE_SIZE)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    if page <= 0 or page > pager.num_pages:
        raise Http404
    cars = pager.page(page)
    return render(request, 'cars/search.html', {'source': source,
                                                'pager': pager,
                                                'cars': cars})

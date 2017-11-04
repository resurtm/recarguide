from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from recarguide.cars.models import Car
from recarguide.cars.search import QueryBuilder, CarSource, PAGE_SIZE, \
    build_hidden_fields


def view(request, slug, id):
    try:
        car = Car.objects.find_by_id_and_slug(id, slug)
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
    return render(request, 'cars/search.html',
                  {'source': source, 'cars': pager.page(page),
                   'fields': build_hidden_fields(source)})

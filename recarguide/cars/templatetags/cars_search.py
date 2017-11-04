from django import template

from recarguide.cars.search import RANGED_PARAMS, UrlBuilder, \
    build_hidden_fields, name_by_id, key_by_id, SHORT_FACET_SIZE, \
    LONG_FACET_SIZE

register = template.Library()


@register.inclusion_tag('cars/search_bar.html')
def search_bar(source):
    return {'fields': build_hidden_fields(source, True, False),
            'keyword': source.params['keyword']}


@register.inclusion_tag('cars/current_filters.html')
def current_filters(source):
    params = []
    url = UrlBuilder(source.params)
    for id, v in source.params.items():
        if not v:
            continue
        if id in RANGED_PARAMS:
            if v == source.facet_ranges[id]:
                continue
            v = '{}—{}'.format(v[0], v[1])
        params.append((name_by_id(id), url.build(**{id: '-'}), v))
    return {'params': params}


@register.inclusion_tag('cars/facet_group.html')
def facet_group(id, source):
    if id == 'make' and source.params['make']:
        return {}
    if id == 'model' and \
            (not source.params['make'] or source.params['model']):
        return {}

    if id == 'category' and source.params['category']:
        return {}
    if id == 'subcategory' and \
            (not source.params['category'] or source.params['subcategory']):
        return {}

    url = UrlBuilder(source.params)
    if id in source.facet_counts:
        items = [(value, count, url.build(**{id: value}))
                 for value, count in source.facet_counts[id]]
    else:
        items = []
    return {'title': name_by_id(id),
            'main_items': items[:SHORT_FACET_SIZE],
            'more_items': items[LONG_FACET_SIZE:]}


@register.inclusion_tag('cars/ranged_facet_group.html')
def ranged_facet_group(id, source):
    min_max = source.facet_ranges[id] if source.facet_ranges[id] else (-1, -1)
    return {'title': name_by_id(id), 'min': min_max[0], 'max': min_max[1],
            'key': key_by_id(id)}


@register.inclusion_tag('cars/search_pagination.html')
def search_pagination(source, cars):
    if not cars.has_other_pages():
        return {}
    url = UrlBuilder(source.params)
    pages = [
        (i, url.build(page=i))
        for i in range(1, cars.paginator.num_pages + 1)
    ]
    prev = url.build(page=cars.number - 1) if cars.has_previous() else None
    next = url.build(page=cars.number + 1) if cars.has_next() else None
    return {'pages': pages, 'prev': prev, 'next': next}

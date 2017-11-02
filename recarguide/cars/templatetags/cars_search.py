from django import template

from recarguide.cars.search import RANGED_PARAMS, UrlBuilder, \
    key_by_id, name_by_id, SHORT_FACET_SIZE, LONG_FACET_SIZE

register = template.Library()


@register.inclusion_tag('cars/search_bar.html')
def search_bar(source):
    tpl = '<input type="hidden" hidden name="{}" value="{}">'
    fields = ''
    for id, value in source.params.items():
        if value and id != 'keyword':
            fields += tpl.format(key_by_id(id), value)
    return {'fields': fields, 'keyword': source.params['keyword']}


@register.inclusion_tag('cars/current_filters.html')
def current_filters(source):
    params = []
    url = UrlBuilder(source.params)
    for id, v in source.params.items():
        if not v:
            continue
        params.append((
            name_by_id(id),
            url.build(**{id: '-'}),
            '{}—{}'.format(v[0], v[1]) if id in RANGED_PARAMS else v
        ))
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
    items = [(value, count, url.build(**{id: value}))
             for value, count in source.facet_counts[id]]
    return {'title': name_by_id(id),
            'main_items': items[:SHORT_FACET_SIZE],
            'more_items': items[LONG_FACET_SIZE:]}

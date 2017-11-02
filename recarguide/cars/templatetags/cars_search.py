from django import template

from recarguide.cars.search import PARAMS, RANGED_PARAMS, UrlBuilder, \
    key_by_id, name_by_id

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
    builder = UrlBuilder(source.params)
    for id, v in source.params.items():
        if not v:
            continue
        params.append((
            name_by_id(id),
            builder.build(**{id: '-'}),
            '{}—{}'.format(v[0], v[1]) if id in RANGED_PARAMS else v
        ))
    return {'params': params}

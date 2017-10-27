from django import template

from recarguide.cars.search.faceted import PARAMS

register = template.Library()


@register.inclusion_tag('cars/current_search.html')
def current_search(fs):
    params = []
    for title, id, key, __ in PARAMS:
        value = getattr(fs, id)
        if value:
            params.append((title, fs.build_url(**{id: '-'}), value))
    return {'params': params}

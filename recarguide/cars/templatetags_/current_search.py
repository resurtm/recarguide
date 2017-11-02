from django import template

from recarguide.cars.search.faceted import PARAMS, RANGED_PARAMS

register = template.Library()


@register.inclusion_tag('cars/current_search.html')
def current_search(fs):
    params = []
    for title, id, key, __ in PARAMS:
        v = getattr(fs, id)
        if v:
            params.append((
                title,
                fs.build_url(**{id: '-'}),
                '{}—{}'.format(v[0], v[1]) if id in RANGED_PARAMS else v,
            ))
    return {'params': params}

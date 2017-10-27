from django import template

from recarguide.cars.search.faceted import (MAX_SHORT_FACET_SIZE, PARAMS)

register = template.Library()


@register.inclusion_tag('cars/facet_group.html')
def facet_group(k, fs, source):
    if k == 'make' and fs.make is not None:
        return {'show': False}
    if k == 'model' and (fs.make is None or fs.model):
        return {'show': False}

    if k == 'category' and fs.category is not None:
        return {'show': False}
    if k == 'subcategory' and (fs.category is None or fs.subcategory):
        return {'show': False}

    return _handle_facet_group(k, fs, source)


def _get_title(to_find):
    for title, id, key, __ in PARAMS:
        if id == to_find:
            return title
    return ''


def _handle_facet_group(k, fs, source):
    items = [
        (i['key'], i['doc_count'], fs.build_url(**{k: i['key']}))
        for i in source.aggregations[k]['buckets']
    ]
    main_items = items[:MAX_SHORT_FACET_SIZE]
    more_items = items[MAX_SHORT_FACET_SIZE:]

    return {'show': True,
            'title': _get_title(k),
            'main_items': main_items,
            'more_items': more_items}

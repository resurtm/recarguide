from django import template

register = template.Library()


@register.inclusion_tag('cars/header_search_bar.html')
def header_search_bar(fsearch):
    hidden = ''
    tpl = '<input type="hidden" hidden name="{}" value="{}">'
    for key, value in fsearch.params_with_key.items():
        if value:
            hidden += tpl.format(key, value)
    return {'fsearch': fsearch, 'hidden': hidden}

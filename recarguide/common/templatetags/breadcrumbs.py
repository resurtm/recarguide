from django import template

register = template.Library()

CONTEXT_KEY = 'breadcrumbs_items'


@register.simple_tag(takes_context=True)
def breadcrumb(context, title, url_name=False):
    context[CONTEXT_KEY] = context.get(CONTEXT_KEY, []) + [(title, url_name)]
    return ''


@register.inclusion_tag('common/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    return {'items': context[CONTEXT_KEY]}

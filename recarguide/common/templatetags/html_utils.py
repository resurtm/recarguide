from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(bound_field, class_):
    field = bound_field.field
    attrs = field.widget.attrs
    if 'class' in attrs:
        attrs['class'] = '{} {}'.format(attrs['class'], class_)
    else:
        attrs['class'] = class_
    field.widget.attrs = attrs
    return bound_field

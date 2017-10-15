from django import template

register = template.Library()


@register.filter
def add_class(bound_field, class_):
    attrs = bound_field.field.widget.attrs
    if 'class' in attrs:
        attrs['class'] = '{} {}'.format(attrs['class'], class_)
    else:
        attrs['class'] = class_
    bound_field.field.widget.attrs = attrs
    return bound_field

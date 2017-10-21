from fnmatch import fnmatch

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


CURR_VIEW_TAG_NAME = 'cv'


@register.tag(name=CURR_VIEW_TAG_NAME)
def curr_view(parser, token):
    try:
        tag_name, view_name, state = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '{} tag requires view name argument'.format(CURR_VIEW_TAG_NAME)
        )
    if not (view_name[0] == view_name[-1] and view_name[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "{} tag's first argument must be enclosed in quotes"
                .format(CURR_VIEW_TAG_NAME)
        )
    if state != 'is_active' and state != 'is_inactive':
        raise template.TemplateSyntaxError(
            "{} tag's second argument must have is_active or is_inactive value"
                .format(CURR_VIEW_TAG_NAME)
        )
    assert tag_name == CURR_VIEW_TAG_NAME

    node_list = parser.parse(('endcv',))
    parser.delete_first_token()

    return CurrentViewNode(view_name[1:-1], state, node_list)


class CurrentViewNode(template.Node):
    def __init__(self, view_name, state, node_list):
        self.view_name = view_name
        self.state = state
        self.node_list = node_list

    def render(self, context):
        vname = context.request.resolver_match.view_name
        if fnmatch(vname, self.view_name) and self.state == 'is_active':
            return self.node_list.render(context)
        if not fnmatch(vname, self.view_name) and self.state == 'is_inactive':
            return self.node_list.render(context)
        return ''

from django import template

register = template.Library()


@register.inclusion_tag('sale/progress_bar.html')
def progress_bar(step):
    bar_percent = 95 if step == 5 else step * 20
    return {'step': step, 'bar_percent': bar_percent}

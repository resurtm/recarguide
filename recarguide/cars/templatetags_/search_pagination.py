from django import template

register = template.Library()


@register.inclusion_tag('cars/search_pagination.html')
def search_pagination(fsearch, source, cars, paginator):
    if not cars.has_other_pages():
        return {}
    pages = []
    if paginator.num_pages <= 5:
        for i in range(1, paginator.num_pages + 1):
            pages.append((
                i,
                fsearch.build_url(page=i)
            ))

    # print('total pages' + str(cars.count))
    #
    # print(cars.has_other_pages)
    # pages = [123]
    # print(dir(cars))
    # print(cars.number)

    return {'pages': pages}

import datetime

from elasticsearch import Elasticsearch

from recarguide.cars.models import Car

es = None
index_prefix = 'recarguide_'


def indices_list():
    indices = ['car']
    return ['{}{}'.format(index_prefix, index) for index in indices]


def mappings_list():
    mappings = {
        'car': {
            'properties': {
                'make': {
                    'type': 'string',
                    'index': 'not_analyzed',
                },
                'model': {
                    'type': 'string',
                    'index': 'not_analyzed',
                },
            },
        },
    }
    res = {}
    for k, v in mappings.items():
        res['{}{}'.format(index_prefix, k)] = v
    return res


def ensure_es():
    """
    :return:
    :rtype: Elasticsearch
    """
    global es
    if es is None:
        es = Elasticsearch()
    print(es)
    return es


def ensure_indices():
    ensure_es()
    mappings = mappings_list()
    for index in indices_list():
        if not es.indices.exists(index=index):
            body = {'mappings': {
                '{}_type'.format(index): mappings[index]
            }}
            es.indices.create(index=index, body=body)


def delete_indices():
    ensure_es()
    for index in indices_list():
        if es.indices.exists(index=index):
            es.indices.delete(index=index)


def reindex_car(car):
    """
    :param car:
    :type car: Car

    :return:
    """
    ensure_es()

    if car.category.parent_id is None:
        category = car.category.name
        subcategory = None
    else:
        category = car.category.parent.name
        subcategory = car.category.name

    body = {'timestamp': datetime.datetime.now(),
            'name': car.name,
            'slug': car.slug,
            'make': car.make.name,
            'model': car.model.name,
            'category': category,
            'subcategory': subcategory,
            'price': car.price,
            'year': car.year,
            'car': car.mileage,
            'description': car.description}

    es.index(index='{}car'.format(index_prefix),
             doc_type='{}car_type'.format(index_prefix),
             id=car.id,
             body=body)


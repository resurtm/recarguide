import datetime

from elasticsearch import Elasticsearch

from recarguide.cars.models import Car

instance = None
index_prefix = 'recarguide_'


def indices_list():
    indices = ['car']
    return ['{}{}'.format(index_prefix, index) for index in indices]


def mappings_list():
    mappings = {
        'car': {
            'properties': {
                'make': {'type': 'string', 'index': 'not_analyzed'},
                'model': {'type': 'string', 'index': 'not_analyzed'},
                'category': {'type': 'string', 'index': 'not_analyzed'},
                'subcategory': {'type': 'string', 'index': 'not_analyzed'},
            },
        },
    }
    res = {}
    for k, v in mappings.items():
        res['{}{}'.format(index_prefix, k)] = v
    return res


def ensure_instance():
    """
    :return:
    :rtype: Elasticsearch
    """
    global instance
    if instance is None:
        instance = Elasticsearch()
    return instance


def ensure_indices():
    ensure_instance()
    mappings = mappings_list()
    for index in indices_list():
        if not instance.indices.exists(index=index):
            body = {'mappings': {
                '{}_type'.format(index): mappings[index]
            }}
            instance.indices.create(index=index, body=body)


def delete_indices():
    ensure_instance()
    for index in indices_list():
        if instance.indices.exists(index=index):
            instance.indices.delete(index=index)


def serialize_car(car):
    if car.category.parent_id is None:
        category = car.category.name
        subcategory = None
    else:
        category = car.category.parent.name
        subcategory = car.category.name
    return {'name': car.name,
            'slug': car.slug,
            'make': car.make.name,
            'model': car.model.name,
            'category': category,
            'subcategory': subcategory,
            'price': car.price,
            'year': car.year,
            'car': car.mileage,
            'description': car.description}


def reindex_car(car):
    """
    :param car:
    :type car: Car

    :return:
    """
    ensure_instance()
    body = serialize_car(car)
    body['timestamp'] = datetime.datetime.now()
    instance.index(index='{}car'.format(index_prefix),
                   doc_type='{}car_type'.format(index_prefix),
                   id=car.id,
                   body=body)


def search_cars(query_body):
    ensure_instance()
    return instance.search(index='recarguide_car',
                           doc_type='recarguide_car_type',
                           body=query_body)

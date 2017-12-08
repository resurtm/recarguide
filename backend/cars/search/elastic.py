import datetime

from elasticsearch import Elasticsearch

instance = None
index_prefix = 'recarguide_'


def indices():
    items = ['car']
    return ['{}{}'.format(index_prefix, index) for index in items]


def mappings():
    items = {
        'car': {
            'properties': {
                'make': {'type': 'string', 'index': 'not_analyzed'},
                'model': {'type': 'string', 'index': 'not_analyzed'},
                'category': {'type': 'string', 'index': 'not_analyzed'},
                'subcategory': {'type': 'string', 'index': 'not_analyzed'},
            },
        },
    }
    return {'{}{}'.format(index_prefix, k): v for k, v in items.items()}


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
    maps = mappings()
    for index in indices():
        if instance.indices.exists(index=index):
            continue
        body = {'mappings': {'{}_type'.format(index): maps[index]}}
        instance.indices.create(index=index, body=body)


def delete_indices():
    ensure_instance()
    for index in indices():
        if instance.indices.exists(index=index):
            instance.indices.delete(index=index)


def encode_car(car):
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
            'trim': car.trim_name,
            'category': category,
            'subcategory': subcategory,
            'price': car.price,
            'year': car.year,
            'car': car.mileage,
            'description': car.description}


def reindex_car(car):
    ensure_instance()
    body = encode_car(car)
    body['timestamp'] = datetime.datetime.now()
    instance.index(index='{}car'.format(index_prefix),
                   doc_type='{}car_type'.format(index_prefix),
                   id=car.id,
                   body=body)


def search_cars(query_body, query='search'):
    ensure_instance()
    return getattr(instance, query)(index='{}car'.format(index_prefix),
                                    doc_type='{}car_type'.format(index_prefix),
                                    body=query_body)

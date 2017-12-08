from cars.search.elastic import search_cars


def find_popular_makes(count=28):
    query = {
        'from': 0,
        'size': 0,
        'query': {
            'match_all': {}
        },
        'aggregations': {
            'makes': {
                'terms': {
                    'field': 'make',
                    'size': count
                }
            }
        }
    }
    return [
        v['key']
        for v in search_cars(query)['aggregations']['makes']['buckets']
    ]

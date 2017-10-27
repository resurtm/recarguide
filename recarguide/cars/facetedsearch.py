def _range_facet_converter(v):
    if '-' not in v:
        return None
    vs = [x.strip() for x in v.split('-')]
    for x in vs:
        if not x.isdigit():
            return None
    return tuple(map(int, vs))


def _bool_facet_converter(v):
    pass


PARAMS = (
    ('Keyword', 'keyword', 'q', str),
    ('Make', 'make', 'm', str),
    ('Model', 'model', 'n', str),
    ('Category', 'category', 'c', str),
    ('Year', 'year', 'y', _range_facet_converter),
    ('Price', 'price', 'p', _range_facet_converter),
    ('Has Picture', 'has_picture', 'hp', _bool_facet_converter),
    ('Sold Listings', 'sold_listings', 'sl', _bool_facet_converter),
)

PAGE_SIZE = 10
MAX_SHORT_FACET_SIZE = 7
MAX_LONG_FACET_SIZE = 21


class FacetedSearch(object):
    def __init__(self, get_params=None):
        if get_params is None:
            get_params = {}
        self._parse_params(get_params)

    def build_es_query(self, offset=0, limit=PAGE_SIZE):
        q = {
            'from': offset,
            'size': limit,
            'query': {},
        }

    @property
    def params(self):
        res = {}
        for __, id, __, __ in PARAMS:
            res[id] = getattr(self, id)
        return res

    def _parse_params(self, params):
        for name, id, key, conv in PARAMS:
            val = str(params.get(key, '')).strip()
            val = conv(val) if len(val) > 0 else None
            setattr(self, id, val)

    def _build_aggregations(self):
        result = {
            'aggregations': {
                'makes': {
                    'terms': {
                        'field': 'make',
                        'size': MAX_LONG_FACET_SIZE
                    }
                },
                'models': {
                    'terms': {
                        'field': 'model',
                        'size': MAX_LONG_FACET_SIZE
                    }
                }
            }
        }

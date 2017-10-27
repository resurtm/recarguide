from urllib.parse import urlencode

from django.urls import reverse


def _range_facet_converter(v):
    if '-' not in v:
        return None
    vs = [x.strip() for x in v.split('-')]
    for x in vs:
        if not x.isdigit():
            return None
    return tuple(map(int, vs))


def _bool_facet_converter(v):
    if isinstance(v, bool):
        return v
    if v == '0' or v == '':
        return False
    if v == '1':
        return True
    return None


PARAMS = (
    ('Keyword', 'keyword', 'q', str),
    ('Make', 'make', 'm', str),
    ('Model', 'model', 'n', str),
    ('Category', 'category', 'c', str),
    ('Sub-Category', 'subcategory', 's', str),
    ('Year', 'year', 'y', _range_facet_converter),
    ('Price', 'price', 'p', _range_facet_converter),
    ('Has Picture', 'has_picture', 'hp', _bool_facet_converter),
    ('Sold Listings', 'sold_listings', 'sl', _bool_facet_converter),
)

AGGREGATABLE_PARAMS = ('make', 'model', 'category', 'subcategory')
RANGED_PARAMS = ('year', 'price')

PAGE_SIZE = 7
MAX_SHORT_FACET_SIZE = 5
MAX_LONG_FACET_SIZE = 10


class FacetedSearch(object):
    def __init__(self, get_params=None):
        if get_params is None:
            get_params = {}
        self._parse_params(get_params)

    def build_query(self, offset=0, limit=PAGE_SIZE, type='query'):
        assert type == 'query' or type == 'filter'
        return {**{'from': offset, 'size': limit},
                **self._build_condition(type),
                **self._build_aggregations()}

    def build_url(self, **kwargs):
        params = []
        for __, id, key, __ in PARAMS:
            if self._check_special_url_cases(id, kwargs):
                continue
            if id in kwargs:
                if kwargs[id] == '-':
                    continue
                else:
                    params.append((key, kwargs[id]))
            elif getattr(self, id):
                params.append((key, getattr(self, id)))
        self._handle_ranges(params)
        url = reverse('cars:search')
        return url + ('?' + urlencode(params) if len(params) > 0 else '')

    def _check_special_url_cases(self, id, kw):
        if id == 'subcategory' and 'category' in kw and kw['category'] == '-':
            return True
        if id == 'model' and 'make' in kw and kw['make'] == '-':
            return True
        return False

    def _handle_ranges(self, params):
        for k, v in enumerate(params):
            if isinstance(v[1], tuple):
                params[k] = v[0], '{}-{}'.format(v[1][0], v[1][1])

    @property
    def params(self):
        res = {}
        for __, id, __, __ in PARAMS:
            res[id] = getattr(self, id)
        return res

    def _parse_params(self, params):
        for name, id, key, converter in PARAMS:
            val = str(params.get(key, '')).strip()
            val = converter(val) if len(val) > 0 else None
            setattr(self, id, val)

    def _build_condition(self, type='query'):
        assert type == 'query' or type == 'filter'
        result = {type: {}}
        must = self._build_must()
        if must:
            result[type] = {'bool': {'must': must}}
        if len(result[type]) == 0:
            result[type] = {'match_all': {}}
        return result

    def _build_must(self):
        must = []
        if self.keyword is not None:
            must.append({'match_phrase': {'_all': self.keyword}})
        for param in AGGREGATABLE_PARAMS:
            value = getattr(self, param)
            if value:
                must.append({'term': {param: value}})
        for param in RANGED_PARAMS:
            value = getattr(self, param)
            if value:
                must.append({
                    'range': {
                        param: {'gte': value[0], 'lte': value[1]},
                    },
                })
        # todo: has picture, sold lisings
        # todo: make this code better
        return must

    def _build_aggregations(self):
        result = {'aggregations': {}}
        for param in AGGREGATABLE_PARAMS:
            result['aggregations'][param] = {
                'terms': {
                    'field': param,
                    'size': MAX_LONG_FACET_SIZE
                }
            }
        return result if len(result['aggregations']) > 0 else {}
from urllib.parse import urlencode

from django.urls import reverse

PAGE_SIZE = 7
SHORT_FACET_SIZE = 5
LONG_FACET_SIZE = 10

QUERY_TYPE_SELECT = 'query'
QUERY_TYPE_FILTER = 'filter'
QUERY_TYPE_COUNT = 'count'


def query_types():
    return [QUERY_TYPE_SELECT, QUERY_TYPE_FILTER, QUERY_TYPE_COUNT]


def _range_converter(v):
    if '-' not in v:
        return None
    vs = [x.strip() for x in v.split('-')]
    for x in vs:
        if not x.isdigit():
            return None
    return int(vs[0]), int(vs[1])


def _bool_converter(v):
    if isinstance(v, bool):
        return v
    if v == '1':
        return True
    return False


PARAMS = (
    # name, id, key, type converter
    ('Keyword', 'keyword', 'q', str),
    ('Make', 'make', 'm', str),
    ('Model', 'model', 'n', str),
    ('Category', 'category', 'c', str),
    ('Sub-Category', 'subcategory', 's', str),
    ('Year', 'year', 'y', _range_converter),
    ('Price', 'price', 'p', _range_converter),
    ('Has Picture Only', 'has_picture', 'hp', _bool_converter),
    ('Include Sold Listings', 'sold_listings', 'sl', _bool_converter),
)
FACET_COUNT_PARAMS = ('make', 'model', 'category', 'subcategory')
RANGED_PARAMS = ('year', 'price')


def key_by_id(find):
    for __, id, key, __ in PARAMS:
        if id == find:
            return key


def name_by_id(find):
    for name, id, __, __ in PARAMS:
        if id == find:
            return name


class UrlBuilder(object):
    def __init__(self, params=None):
        self._params = params if params else {}

    def build(self, **kwargs):
        res = []
        kw = {k: v.strip() for k, v in kwargs.items()}
        for __, id, key, __ in PARAMS:
            if self._skip_param(id, kw):
                continue
            if id in kw and kw[id]:
                res.append((key, kw[id]))
            elif id in self._params and self._params[id]:
                res.append((key, self._params[id]))
        self._handle_ranges(res)
        if 'page' in kw and kw['page']:
            res.append(('page', kw['page']))
        return reverse('cars:search') + ('?' + urlencode(res) if res else '')

    def _skip_param(self, id, kw):
        if id in kw and kw[id] == '-':
            return True
        if id == 'subcategory' and 'category' in kw and kw['category'] == '-':
            return True
        if id == 'model' and 'make' in kw and kw['make'] == '-':
            return True
        return False

    def _handle_ranges(self, params):
        for k, v in enumerate(params):
            if isinstance(v[1], tuple) and len(v[1]) == 2:
                params[k] = v[0], '{}-{}'.format(v[1][0], v[1][1])


class QueryBuilder(object):
    def __init__(self, params=None):
        if params is None:
            params = {}
        self.params = {}
        for __, id, key, conv in PARAMS:
            val = str(params.get(key, '')).strip()
            self.params[id] = conv(val) if val else None

    def build(self, offset=0, limit=PAGE_SIZE, type='query'):
        assert type in query_types()
        return {**self._build_offset_limit(offset, limit),
                **self._build_condition(type),
                **self._build_aggregations(type)}

    def _build_offset_limit(self, offset, limit):
        res = {}
        if offset is not None:
            res['from'] = offset
        if limit is not None:
            res['size'] = limit
        return res

    def _build_condition(self, type=QUERY_TYPE_SELECT):
        must = self._build_must()
        res = {'bool': {'must': must}} if must else {'match_all': {}}
        return {QUERY_TYPE_FILTER if type == QUERY_TYPE_COUNT else type: res}

    def _build_must(self):
        must = []
        if self.params['keyword']:
            must.append({'match_phrase': {'_all': self.params['keyword']}})
        for id in FACET_COUNT_PARAMS:
            if id in self.params and self.params[id]:
                must.append({'term': {id: self.params[id]}})
        for id in RANGED_PARAMS:
            if id in self.params and self.params[id]:
                v = self.params[id]
                must.append({
                    'range': {
                        id: {'gte': v[0], 'lte': v[1]},
                    },
                })
        # todo: has picture only, include sold listings
        return must

    def _build_aggregations(self, type=QUERY_TYPE_SELECT):
        if type == QUERY_TYPE_COUNT:
            return {}
        result = {
            id: {'terms': {'field': id, 'size': LONG_FACET_SIZE}}
            for id in FACET_COUNT_PARAMS
        }
        return {'aggregations': result} if result else {}

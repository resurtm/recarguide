from recarguide.cars.models import Car
from recarguide.cars.search.builders import QUERY_TYPE_COUNT, \
    QUERY_TYPE_SELECT, FACET_COUNT_PARAMS, PARAMS
from recarguide.cars.search.elastic import search_cars


class CarSource:
    def __init__(self, query_builder):
        self._qb = query_builder
        self._count = None

        self.facet_counts = {}
        self.params = self._qb.params

    def __len__(self):
        return self._calc_count()

    def __getitem__(self, sl):
        query = self._qb.build(sl.start, sl.stop - sl.start, QUERY_TYPE_SELECT)
        res = search_cars(query)
        aggrs = res['aggregations']

        for id in FACET_COUNT_PARAMS:
            if id not in aggrs or not aggrs[id]['buckets']:
                continue
            self.facet_counts[id] = []
            for b in aggrs[id]['buckets']:
                self.facet_counts[id].append((b['key'], b['doc_count']))

        ids = [int(car['_id']) for car in res['hits']['hits']]
        return Car.objects.filter(pk__in=ids)

    def _calc_count(self):
        if self._count is None:
            result = search_cars(self._qb.build(None, None, QUERY_TYPE_COUNT),
                                 'count')
            self._count = int(result['count'])
        return self._count

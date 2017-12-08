from cars.models import Car
from cars.search.builders import QUERY_TYPE_COUNT, QUERY_TYPE_SELECT, \
    FACET_COUNT_PARAMS, RANGED_PARAMS
from cars.search.elastic import search_cars


class CarSource:
    def __init__(self, query_builder):
        self._qb = query_builder
        self._count = None

        self.facet_counts = {}
        self.facet_ranges = {}
        self.params = self._qb.params

    def __len__(self):
        return self._calc_count()

    def __getitem__(self, sl):
        res1 = search_cars(
            self._qb.build(sl.start, sl.stop - sl.start, QUERY_TYPE_SELECT)
        )
        aggrs = res1['aggregations']
        for id in FACET_COUNT_PARAMS:
            if id not in aggrs or not aggrs[id]['buckets']:
                continue
            self.facet_counts[id] = []
            for b in aggrs[id]['buckets']:
                self.facet_counts[id].append((b['key'], b['doc_count']))

        res2 = search_cars(
            self._qb.build(0, 0, QUERY_TYPE_SELECT, True)
        )
        aggrs = res2['aggregations']
        for id in RANGED_PARAMS:
            if 'min_' + id not in aggrs or 'max_' + id not in aggrs:
                continue
            a = aggrs['min_' + id]['value']
            b = aggrs['max_' + id]['value']
            self.facet_ranges[id] = (int(a), int(b)) if a and b else None

        ids = [int(car['_id']) for car in res1['hits']['hits']]
        return Car.objects.filter(pk__in=ids)

    def _calc_count(self):
        if self._count is None:
            result = search_cars(self._qb.build(None, None, QUERY_TYPE_COUNT),
                                 'count')
            self._count = int(result['count'])
        return self._count

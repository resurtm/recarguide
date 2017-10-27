from recarguide.cars.models import Car
from recarguide.cars.search.elastic import search_cars


class CarSource:
    def __init__(self, fsearch):
        self.aggregations = {}
        self.page = None
        self._fsearch = fsearch
        self._count = None

    def __len__(self):
        return self._calc_count()

    def __getitem__(self, sl):
        query = self._fsearch.build_query(sl.start,
                                          sl.stop - sl.start,
                                          'query')
        result = search_cars(query)
        self.aggregations = result['aggregations']
        ids = [int(car['_id']) for car in result['hits']['hits']]
        return Car.objects.filter(pk__in=ids)

    def _calc_count(self):
        if self._count is None:
            query = self._fsearch.build_query(0, 0, 'filter')
            result = search_cars(query)
            self._count = int(result['hits']['total'])
        return self._count

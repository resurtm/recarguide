from django.test import TestCase

from recarguide.cars.facetedsearch import FacetedSearch as FS


class FacetedSearchParamsTestCase(TestCase):
    def test_case1(self):
        params = {'keyword': None, 'make': None, 'model': None,
                  'category': None, 'year': None, 'price': None,
                  'has_picture': None, 'sold_listings': None}

        fs = FS()
        self.assertEqual(fs.params, params)

        fs = FS({})
        self.assertEqual(fs.params, params)

    def test_case2(self):
        fs = FS({'q': 'test1', 'm': 'test2', 'n': 'test3',
                 'c': 'test4', 'y': '2500-7500', 'p': '5550-8650',
                 'hp': '1', 'sl': '1'})
        params = {'keyword': 'test1', 'make': 'test2', 'model': 'test3',
                  'category': 'test4', 'year': (2500, 7500),
                  'price': (5550, 8650), 'has_picture': True,
                  'sold_listings': True}
        self.assertEqual(fs.params, params)

from django.test import TestCase

from recarguide.cars.facetedsearch import _range_facet_converter as rfc


class RangeFacetConverterTestCase(TestCase):
    def test_case1(self):
        self.assertIsNone(rfc('-'))
        self.assertIsNone(rfc(' -  '))

    def test_case2(self):
        self.assertIsNone(rfc('-5000'))
        self.assertIsNone(rfc(' -5000  '))
        self.assertIsNone(rfc(' - 5000  '))
        self.assertIsNone(rfc('1000-'))
        self.assertIsNone(rfc(' 1000-  '))
        self.assertIsNone(rfc(' 1000 -  '))

    def test_case3(self):
        self.assertEqual(rfc('1000-5000'), (1000, 5000))
        self.assertEqual(rfc(' 1001-5001  '), (1001, 5001))
        self.assertEqual(rfc(' 1002 - 5002  '), (1002, 5002))

    def test_case4(self):
        self.assertIsNone(rfc('1000.1-5000.1'))
        self.assertIsNone(rfc(' 1000.1-5000.1  '))
        self.assertIsNone(rfc(' 1000.1 - 5000.1  '))

    def test_case5(self):
        self.assertIsNone(rfc('abc'))
        self.assertIsNone(rfc(' abc  '))

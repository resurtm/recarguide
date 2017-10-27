from django.test import TestCase

from recarguide.cars.facetedsearch import _bool_facet_converter as bfc


class BoolFacetConverterTestCase(TestCase):
    def test_case1(self):
        self.assertTrue(bfc('1'))
        self.assertTrue(bfc(True))

        self.assertFalse(bfc('0'))
        self.assertFalse(bfc(''))
        self.assertFalse(bfc(False))

    def test_case2(self):
        self.assertIsNone(bfc('2'))
        self.assertIsNone(bfc(2))

        self.assertIsNone(bfc({}))
        self.assertIsNone(bfc([]))
        self.assertIsNone(bfc((1,)))

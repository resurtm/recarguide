import datetime

from django.test import TestCase

from recarguide.sale.tools import years_choices


class YearsChoicesTestCase(TestCase):
    def test_case1(self):
        current_year = datetime.datetime.now().year
        choices = [(i, str(i)) for i in range(current_year, 1900 - 1, -1)]
        choices.insert(0, (None, ''))
        self.assertEqual(choices, years_choices())

    def test_case2(self):
        choices = [
            (1930, '1930'),
            (1929, '1929'),
            (1928, '1928'),
            (1927, '1927'),
            (1926, '1926'),
            (1925, '1925'),
        ]
        self.assertEqual(choices, years_choices(False, 1925, 1930))

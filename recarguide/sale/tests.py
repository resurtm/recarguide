from django.test import TestCase

from recarguide.sale.models import PackagePlan


class TestPackagePlanModel(TestCase):
    def test_stripe_price(self):
        package_plan = PackagePlan(price=123)
        self.assertEqual(12300, package_plan.stripe_price)

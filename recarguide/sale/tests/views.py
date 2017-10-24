import re

from django.contrib.auth.models import User
from django.http.response import HttpResponseBadRequest
from django.test import TestCase
from django.urls import reverse


class _SaleTestCase(TestCase):
    def _login_new_user(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.assertTrue(self.client.login(username='testuser',
                                          password='12345'))

    def _login_user(self):
        self.assertTrue(self.client.login(username='resurtm',
                                          password='abc123abc123'))


class SaleIndexTestCase(_SaleTestCase):
    def test_guest(self):
        resp = self.client.get(reverse('sale:index'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('location' in resp)
        self.assertEqual(resp['location'], '/login/?next=/sale/')

    def test_user(self):
        self._login_new_user()
        resp = self.client.get(reverse('sale:index'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('location' in resp)
        self.assertEqual(resp['location'], '/sale/step1/')


class SaleStep1TestCase(_SaleTestCase):
    fixtures = ['packageplans']

    def test_guest(self):
        resp = self.client.get(reverse('sale:step1'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('location' in resp)
        self.assertEqual(resp['location'], '/login/?next=/sale/step1/')

    def test_user_get(self):
        self._login_new_user()
        resp = self.client.get(reverse('sale:step1'))
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode('utf-8', 'strict')
        self.assertIsNotNone(re.search('<h4[^>]*>Step #1</h4>', content))
        self.assertIsNotNone(re.search('<button[^>]*>\s*Select\s*</button>',
                                       content))

    def test_user_post_fail(self):
        self._login_new_user()
        resp = self.client.post(reverse('sale:step1'))
        self.assertEqual(resp.status_code, 400)
        self.assertTrue(isinstance(resp, HttpResponseBadRequest))

    def test_user_post_success(self):
        self._login_new_user()
        resp = self.client.post(reverse('sale:step1'), {'package_plan_id': 1})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('location' in resp)
        self.assertEqual(resp['location'], '/sale/step2/')


class SaleStep2TestCase(_SaleTestCase):
    fixtures = ['users', 'packageplans', 'sellprocesses', 'makes', 'models',
                'categories']

    def test_guest(self):
        resp = self.client.get(reverse('sale:step2'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('location' in resp)
        self.assertEqual(resp['location'], '/login/?next=/sale/step2/')

    def test_user_get(self):
        self._login_user()
        resp = self.client.get(reverse('sale:step2'))
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode('utf-8', 'strict')
        self.assertIsNotNone(re.search('<h4[^>]*>Step #2</h4>', content))
        self.assertIsNotNone(re.search('<button[^>]*>\s*Next\s*</button>',
                                       content))

    def test_user_post_fail(self):
        self._login_user()
        resp = self.client.post(reverse('sale:step2'))
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode('utf-8', 'strict')
        self.assertIsNotNone(re.search('<h4[^>]*>Step #2</h4>', content))
        self.assertIsNotNone(re.search('<button[^>]*>\s*Next\s*</button>',
                                       content))

    def test_user_post_success(self):
        self._login_user()
        resp = self.client.post(reverse('sale:step2'), {
            'mileage': [125600],
            'price': 35000,
            'year': 2011,
            'make': 1,
            'model': 2,
            'category': 4,
            'subcategory': 5,
            'description': 'testing car',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('location' in resp)
        self.assertEqual(resp['location'], '/sale/step3/')

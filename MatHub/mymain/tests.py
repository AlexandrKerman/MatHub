from django.test import TestCase
from django.contrib.auth import authenticate, login
# Create your tests here.

class Test_redirect (TestCase):
    def test_index (self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)
    def test_materials (self):
        response = self.client.get('/material/')
        self.assertEqual(response.status_code, 302)
    def test_orders (self):
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, 302)
    def test_storages (self):
        response = self.client.get('/storage/')
        self.assertEqual(response.status_code, 302)


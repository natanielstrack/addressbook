import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client

from maps.models import Address


class HomeAccess(TestCase):

    def test_accessing_home(self):
        client = Client()

        response = client.get('/')
        self.assertEqual(response.status_code, 200)


class ListAddressApiTestCase(TestCase):

    def setUp(self):
        Address.objects.create(latitude=43.100, longitude=123, address="some street")
        Address.objects.create(latitude=-43.100, longitude=-100.14312, address="other street")

    def test_listing_address(self):
        client = Client()

        response = client.post('/list')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content['results']), 2)

class AddAddressApiTestCase(TestCase):

    @patch('maps.views.AddAddress._get_address')
    def test_adding_address(self, get_address):
        get_address.return_value = 'some street'
        client = Client()

        response = client.post(
            '/add',
            {'lat':43.100, 'lng':123, 'address':'some street'}
        )
        self.assertEqual(response.status_code, 200)

        addresses = Address.objects.filter(address='some street')
        self.assertEqual(addresses.count(), 1)

class DeleteApiTestCase(TestCase):

    def setUp(self):
        Address.objects.create(latitude=43.100, longitude=123, address="some street")
        Address.objects.create(latitude=-43.100, longitude=-100.14312, address="other street")

    def test_deleting_address(self):
        client = Client()

        response = client.post('/delete')
        self.assertEqual(response.status_code, 200)

        addresses = Address.objects.all()
        self.assertEqual(addresses.count(), 0)

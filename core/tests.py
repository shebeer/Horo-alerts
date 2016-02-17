from django.test import TestCase

# Create your tests here.
import unittest
from django.test import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        assert(len(response.context['predictions'])== 12 or len(response.context['predictions'])== 1)

    def test_subscribe(self):

        response = self.client.post('/subscribe/', {'email': 'shabeersha33@gmail.com', 'name': 'secret','dob':'24/02/2016'})
        self.assertEqual(response.status_code, 200)
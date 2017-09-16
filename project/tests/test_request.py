from __future__ import absolute_import, unicode_literals
import unittest
import requests

from project.event import EventFactory
from eventlib import random_event_dict, STATIC_EVENT

BASE_URL = "http://localhost:5000/"

class RequestTest(unittest.TestCase):

    def test_single_request_static(self):
        response = requests.post(BASE_URL+'receiver', data=STATIC_EVENT)
        self.assertEqual(response.status_code, 200)
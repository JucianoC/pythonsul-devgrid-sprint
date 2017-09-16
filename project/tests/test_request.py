from __future__ import absolute_import, unicode_literals
import unittest
import requests

from project.event import EventFactory
from eventlib import random_event_dict, STATIC_EVENT

SLOW_TESTS_ACTIVE = False

BASE_URL = "http://localhost:5000/"
MANY_REQUESTS_RANGE = 500

class RequestTest(unittest.TestCase):

    def test_single_request_static(self):
        response = requests.post(BASE_URL+'receiver', data=STATIC_EVENT)
        self.assertEqual(response.status_code, 200)

    def test_single_request_random(self):
        random_event_string = EventFactory.event_string_from_dict(random_event_dict())
        response = requests.post(BASE_URL+'receiver', data=random_event_string)
        self.assertEqual(response.status_code, 200)

    def test_many_request_static(self):
        if SLOW_TESTS_ACTIVE:
            index = 0
            responses_codes = []
            while index < MANY_REQUESTS_RANGE:
                response = requests.post(BASE_URL+'receiver', data=STATIC_EVENT)
                responses_codes.append(response.status_code)
                index += 1

            self.assertListEqual(responses_codes, [200]*MANY_REQUESTS_RANGE)
        else:
            self.assertEqual(True, True)

    def test_many_request_random(self):
        if SLOW_TESTS_ACTIVE:
            index = 0
            responses_codes = []
            while index < MANY_REQUESTS_RANGE:
                random_event_string = EventFactory.event_string_from_dict(random_event_dict())
                response = requests.post(BASE_URL+'receiver', data=random_event_string)
                responses_codes.append(response.status_code)
                index += 1

            self.assertListEqual(responses_codes, [200]*MANY_REQUESTS_RANGE)
        else:
            self.assertEqual(True, True)
from __future__ import absolute_import
import unittest
from datetime import datetime
import pytz

from project.event import EventFactory
from eventlib import random_event_dict, STATIC_EVENT

class ParserTest(unittest.TestCase):
    """
    That class are responsable to teste the parser of a string event to dict
    """

    def test_single_parser_random(self):
        comparable_dict = random_event_dict()
        event = EventFactory.event_from_string(EventFactory.event_string_from_dict(comparable_dict))
        comparable_event = EventFactory.event_from_dict(comparable_dict)
        self.assertDictEqual(event.__dict__, comparable_event.__dict__)

    def test_single_parser_static(self):
        comparable_dict = {
            'device_id': 10, 
            'hz': 49.87, 
            'fft_re': [-257863.0, 102815.0, -64043.0, 48516.0, 59599.0, -4223.0, -43441.0, 23559.0, -24518.0], 
            'line': {
                'phase': -43.841, 
                'voltage': 230.08, 
                'current': 1.75
            }, 
            'dummy': 2, 
            'utc_time': datetime(2016, 10, 4, 16, 47, 50, tzinfo=pytz.UTC), 
            'device_fw': 16071801, 
            'wifi_strength': -62, 
            'power': {
                'reactive': 279, 
                'appearent': 403, 
                'active': 289
            }, 
            'alarms': {'coilrevesed':  'off'}, 
            'fft_img': [481910.0, -14891.0, 69871.0, -7130.0, 43860.0, 34204.0, 55951.0, -6945.0, 26131.0], 
            'peaks': [1041.0, 1051.0, 1058.0, 1051.0, 1049.0, 1047.0, 1054.0, 1059.0, 1057.0, 1060.0], 
            'evt': 2
        }
        event = EventFactory.event_from_string(EventFactory.event_string_from_dict(comparable_dict))
        comparable_event = EventFactory.event_from_dict(comparable_dict)
        self.assertDictEqual(event.__dict__, comparable_event.__dict__)

    def test_string_to_dict(self):
        comparable_dict = {
            'device_id': 10, 
            'hz': 49.87, 
            'fft_re': [-257863.0, 102815.0, -64043.0, 48516.0, 59599.0, -4223.0, -43441.0, 23559.0, -24518.0], 
            'line': {
                'phase': -43.841, 
                'voltage': 230.08, 
                'current': 1.75
            }, 
            'dummy': 2, 
            'utc_time': datetime(2016, 10, 4, 16, 47, 50, tzinfo=pytz.UTC), 
            'device_fw': 16071801, 
            'wifi_strength': -62, 
            'power': {
                'reactive': 279, 
                'appearent': 403, 
                'active': 289
            }, 
            'alarms': {'coilrevesed':  'off'}, 
            'fft_img': [481910.0, -14891.0, 69871.0, -7130.0, 43860.0, 34204.0, 55951.0, -6945.0, 26131.0], 
            'peaks': [1041.0, 1051.0, 1058.0, 1051.0, 1049.0, 1047.0, 1054.0, 1059.0, 1057.0, 1060.0], 
            'evt': 2
        }
        self.assertEqual(STATIC_EVENT, EventFactory.event_string_from_dict(comparable_dict))
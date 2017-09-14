import re
from datetime import datetime

class Event(object):
    def __init__(self):
        self.device_id = None
        self.device_fw = None
        self.evt = None
        self.alarms = dict()
        self.power = dict(
            active = None,
            reactive = None,
            appearent = None
        )
        self.line = dict(
            current = None,
            voltage = None,
            phase = None
        )
        self.peaks = []
        self.fft_re = []
        self.fft_img = []
        self.utc_time = None
        self.hz = None
        self.wifi_strength = None
        self.dummy = None

class EventFactory(object):

    REGEX_GROUP = r"([a-z]|[A-Z])+( |[a-z]|[A-Z])*\:( |\w|\=|\;|\.|\-|\,|(\d+\:\d+\:\d+))*(?!( |[a-z]|[A-Z])*\:)"
    REGEX_SUBGROUP = r'^(?P<head>\w+|\w+ \w+)\: (?P<tail>.*)'

    @classmethod
    def get_event(cls, event_string):
        event = Event()

        info_groups = [value.group() for value in re.finditer(EventFactory.REGEX_GROUP, event_string)]
        info_groups = map(lambda value: value.lower(), info_groups)

        try:
            for group in info_groups:
                re_result = re.match(EventFactory.REGEX_SUBGROUP, group)
                head = re_result.group('head')
                tail = re_result.group('tail')
                print("head -> ", head)
                print("tail -> ", tail)

                if head == "device":
                    EventFactory.decode_device(event, tail)
                elif head == "alarms":
                    EventFactory.decode_alarms(event, tail)
                elif head == "power":
                    EventFactory.decode_power(event, tail)
                
        except:
            raise
            return None
        
        return event

    @classmethod
    def decode_device(cls, event, tail_info):
        data = [value.split('=') for value in tail_info.split('; ')]
        data = [(key, int(value)) for key, value in data]
        for key, value in data:
            if key == 'id': 
                event.device_id = value
            elif key == 'fw': 
                event.device_fw = value
            elif key == 'evt': 
                event.evt = value

    @classmethod
    def decode_alarms(cls, event, tail_info):
        alarm_dict = dict()
        data = [value.split('=') for value in tail_info.split('; ')]
        for key, value in data:
            alarm_dict[key] = value
        event.alarms.update(alarm_dict)

    @classmethod
    def decode_power(cls, event, tail_info):
        power_dict = dict()
        data = [value.split('=') for value in tail_info.split('; ')]
        for key, value in data:
            info = float(re.match(r'(\d|\.)*', value).group(0))
            power_dict[key] = info
        event.power.update(power_dict)
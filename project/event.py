import re
from datetime import datetime
import pytz

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

                if head == "device":
                    EventFactory.decode_device(event, tail)
                elif head == "alarms":
                    EventFactory.decode_alarms(event, tail)
                elif head == "power":
                    EventFactory.decode_power(event, tail)
                elif head == "line":
                    EventFactory.decode_line(event, tail)
                elif head == "peaks":
                    EventFactory.decode_float_values_in_list(
                        event.peaks, tail
                    )
                elif head == "fft re":
                    EventFactory.decode_float_values_in_list(
                        event.fft_re, tail
                    )
                elif head == "fft img":
                    EventFactory.decode_float_values_in_list(
                        event.fft_img, tail
                    )
                elif head == "utc time":
                    event.utc_time = datetime.strptime(tail, "%Y-%m-%d %H:%M:%S")
                    event.utc_time.replace(tzinfo=pytz.UTC)
                elif head == "hz":
                    event.hz = float(tail)
                elif head == "wifi strength":
                    event.wifi_strength = int(tail)
                elif head == "dummy":
                    event.dummy = int(tail)
                
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
        data = [value.split('=') for value in tail_info.split('; ')]
        for key, value in data:
            event.alarms[key] = value

    @classmethod
    def decode_power(cls, event, tail_info):
        data = [value.split('=') for value in tail_info.split('; ')]
        for key, value in data:
            info = int(re.match(r'\d+', value).group(0))
            event.power[key] = info

    @classmethod
    def decode_line(cls, event, tail_info):
        data = [value.split('=') for value in tail_info.split('; ')]
        for key, value in data:
            info = float(re.match(r'(\-|\d|\.|\,)*', value).group(0).replace(',','.'))
            event.line[key] = info

    @classmethod
    def decode_float_values_in_list(cls, list_instance, tail_info):
        for value in tail_info.split('; '):
            info = float(re.match(r'(\-|\d|\.)*', value).group(0))
            list_instance.append(info)
from __future__ import absolute_import, unicode_literals
import json
import re
from datetime import datetime
import pytz

from project.models import SensorEvent, SensorEventPeaks, SensorEventFFTRE, SensorEventFFTIMG

class Event(object):
    """
    This class map a event string to this object
    """
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

    def to_json(self):
        """
        Return a json representation of the object
        """
        instance_dict = self.__dict__.copy()
        instance_dict['utc_time'] = instance_dict['utc_time'].isoformat()
        return json.dumps(instance_dict, separators=(',', ':'))

    def save(self, db):
        """
        Save in the database the event
        """
        sensor_event = SensorEvent(
            device_id=self.device_id,
            device_fw=self.device_fw,
            device_evt=self.evt,
            alarms=json.dumps(self.alarms),
            power_active=self.power['active'],
            power_reactive=self.power['reactive'],
            power_appearent=self.power['appearent'],
            line_current=self.line['current'],
            line_voltage=self.line['voltage'],
            line_phase=self.line['phase'],
            utc_time=self.utc_time,
            hz=self.hz,
            wifi_strength=self.wifi_strength,
            dummy=self.dummy,
            clustered=True
        )

        db.session.add(sensor_event)
        
        try:
            db.session.commit()
        except:
            raise #debug
            db.session.rollback()
            return None

        peaks = [
            SensorEventPeaks(value=value, sensor_event_id=sensor_event.id)
            for value in self.peaks
        ]

        fft_re = [
            SensorEventFFTRE(value=value, sensor_event_id=sensor_event.id)
            for value in self.fft_re
        ]

        fft_img = [
            SensorEventFFTIMG(value=value, sensor_event_id=sensor_event.id)
            for value in self.fft_img
        ]

        db.session.add_all(peaks)
        db.session.add_all(fft_re)
        db.session.add_all(fft_img)
        sensor_event.clustered = False
        
        try:
            db.session.commit()
        except:
            raise #debug
            db.session.rollback()
            return None

        return sensor_event

class EventFactory(object):
    """
    This class is a Event factory
    """

    REGEX_GROUP = r"([a-z]|[A-Z])+( |[a-z]|[A-Z])*\:( |\w|\=|\;|\.|\-|\,|(\d+\:\d+\:\d+))*(?!( |[a-z]|[A-Z])*\:)"
    REGEX_SUBGROUP = r'^(?P<head>\w+|\w+ \w+)\: (?P<tail>.*)'
    EVENT_STRING = "Device: ID={device_id}; Fw={device_fw}; Evt={evt}; Alarms: CoilRevesed=OFF; Power: Active={active}W; Reactive={reactive}var; Appearent={appearent}VA; Line: Current={current}A; Voltage={voltage}V; Phase={phase}rad; Peaks: {peaks}; FFT Re: {fft_re}; FFT Img: {fft_img}; UTC Time: {utc_time}; hz: {hz}; WiFi Strength: {wifi_strength}; Dummy: {dummy}"

    @classmethod
    def event_from_string(cls, event_string):
        """
        Return a Event object from an event string
        """
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
                    event.utc_time = event.utc_time.replace(tzinfo=pytz.UTC)
                elif head == "hz":
                    event.hz = float(tail)
                elif head == "wifi strength":
                    event.wifi_strength = int(tail)
                elif head == "dummy":
                    event.dummy = int(tail)
                
        except:
            return None
        
        return event

    @classmethod
    def decode_device(cls, event, tail_info):
        """
        Decode the device information
        """
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
        """
        Decode the alarms information
        """
        data = [value.split('=') for value in tail_info.split('; ')]
        for key, value in data:
            event.alarms[key] = value

    @classmethod
    def decode_power(cls, event, tail_info):
        """
        Decode the power information
        """
        data = [value.split('=') for value in tail_info.split('; ')]
        for key, value in data:
            info = int(re.match(r'\d+', value).group(0))
            event.power[key] = info

    @classmethod
    def decode_line(cls, event, tail_info):
        """
        Decode the line information
        """
        data = [value.split('=') for value in tail_info.split('; ')]
        for key, value in data:
            info = float(re.match(r'(\-|\d|\.|\,)*', value).group(0).replace(',','.'))
            event.line[key] = info

    @classmethod
    def decode_float_values_in_list(cls, list_instance, tail_info):
        """
        Decode the tail info to a list of floats
        """
        for value in tail_info.split('; '):
            info = float(re.match(r'(\-|\d|\.)*', value).group(0))
            list_instance.append(info)

    @classmethod
    def event_string_from_dict(cls, event_dict):
        """
        Return a event string from a Event
        """
        kwargs = event_dict.copy()
        kwargs['fft_re'] = '; '.join(map("{:.2f}".format, kwargs['fft_re']))
        kwargs.update(kwargs.pop('line'))
        kwargs['phase'] = (str(kwargs['phase'])).replace('.', ',')
        kwargs.pop('alarms')
        kwargs['fft_img'] = '; '.join(map("{:.2f}".format, kwargs['fft_img']))
        kwargs.update(kwargs.pop('power'))
        kwargs['peaks'] = '; '.join(map("{:.3f}".format, kwargs['peaks']))
        kwargs['utc_time'] = kwargs['utc_time'].strftime("%Y-%m-%-d %H:%M:%S")
        
        return EventFactory.EVENT_STRING.format(**kwargs)

    @classmethod
    def event_from_dict(cls, event_dict):
        """
        Return a Event from a event dict
        """
        return EventFactory.event_from_string(EventFactory.event_string_from_dict(event_dict))
from datetime import datetime
from random import randint, uniform

STATIC_EVENT = "Device: ID=10; Fw=16071801; Evt=2; Alarms: CoilRevesed=OFF; Power: Active=289W; Reactive=279var; Appearent=403VA; Line: Current=1.75A; Voltage=230.08V; Phase=-43,841rad; Peaks: 1041.000; 1051.000; 1058.000; 1051.000; 1049.000; 1047.000; 1054.000; 1059.000; 1057.000; 1060.000; FFT Re: -257863.00; 102815.00; -64043.00; 48516.00; 59599.00; -4223.00; -43441.00; 23559.00; -24518.00; FFT Img: 481910.00; -14891.00; 69871.00; -7130.00; 43860.00; 34204.00; 55951.00; -6945.00; 26131.00; UTC Time: 2016-10-4 16:47:50; hz: 49.87; WiFi Strength: -62; Dummy: 2"
EVENT_STRING = "Device: ID={device_id}; Fw={device_fw}; Evt={evt}; Alarms: CoilRevesed=OFF; Power: Active={active}W; Reactive={reactive}var; Appearent={appearent}VA; Line: Current={current}A; Voltage={voltage}V; Phase={phase}rad; Peaks: {peaks}; FFT Re: {fft_re}; FFT Img: {fft_img}; UTC Time: {utc_time}; hz: {hz}; WiFi Strength: {wifi_strength}; Dummy: {dummy}"

def random_event_dict():
    return {
        'device_fw': randint(10000000, 20000000), 
        'fft_re': [round(uniform(-200000.0, 500000.0), 1) for i in range(9)], 
        'hz': round(uniform(40.0, 50.0), 2), 
        'line': {'phase': round(uniform(-50.0, -40.0), 3), 'current': round(uniform(1.0, 2.0), 2), 'voltage': round(uniform(200.0, 250.0), 2)}, 
        'alarms': {'coilrevesed': 'off'}, 
        'dummy': 2, 
        'fft_img': [round(uniform(-20000.0, 500000.0), 1) for i in range(9)], 
        'power': {'active': randint(200,300), 'appearent': randint(400,500), 'reactive': randint(200,300)}, 
        'peaks': [round(uniform(1000.0, 1100.0), 1) for i in range(10)], 
        'utc_time': datetime(randint(2000,2100), randint(1,12), randint(1,28), randint(0,24), randint(0,59), randint(0,59)), 
        'evt': 2, 
        'wifi_strength': randint(-100, 0), 
        'device_id': randint(10, 90)
    }

def event_string_from_dict(event_dict):
    kwargs = event_dict.copy()
    kwargs['fft_re'] = '; '.join(map(str, kwargs['fft_re']))
    kwargs.update(kwargs.pop('line'))
    kwargs['voltage'] = (str(kwargs['voltage'])).replace('.', ',')
    kwargs.pop('alarms')
    kwargs['fft_img'] = '; '.join(map(str, kwargs['fft_img']))
    kwargs.update(kwargs.pop('power'))
    kwargs['peaks'] = '; '.join(map(str, kwargs['peaks']))
    kwargs['utc_time'] = kwargs['utc_time'].strftime("%Y-%m-%d %H:%M:%S")
    
    return EVENT_STRING.format(**kwargs)
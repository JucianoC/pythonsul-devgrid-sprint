from __future__ import absolute_import, unicode_literals
from project.app import db

class Cluster(db.Model):
    """
    Map the cluster table in database
    """
    __tablename__ = 'cluster'
    id = db.Column(db.Integer, primary_key=True)
    event = db.relationship('SensorEvent', lazy='select')

class SensorEvent(db.Model):
    """
    Map the sensor_event table in database
    """
    __tablename__ = 'sensor_event'
    id = db.Column(db.Integer, primary_key=True)
    clustered = db.Column(db.Boolean, default=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), default=None)
    cluster_label = db.Column(db.Integer, default=None)
    device_id = db.Column(db.Integer())
    device_fw = db.Column(db.Integer())
    device_evt = db.Column(db.Integer())
    alarms = db.Column(db.String(256))
    power_active = db.Column(db.Float)
    power_reactive = db.Column(db.Float)
    power_appearent = db.Column(db.Float)
    line_current = db.Column(db.Float)
    line_voltage = db.Column(db.Float)
    line_phase = db.Column(db.Float)
    peaks = db.relationship('SensorEventPeaks', lazy='select')
    fft_re = db.relationship('SensorEventFFTRE', lazy='select')
    fft_img = db.relationship('SensorEventFFTIMG', lazy='select')
    utc_time = db.Column(db.DateTime(timezone=True))
    hz = db.Column(db.Float)
    wifi_strength = db.Column(db.Integer)
    dummy = db.Column(db.Integer)

class SensorEventPeaks(db.Model):
    """
    Map the sensor_event_peaks table in database
    """
    __tablename__ = 'sensor_event_peaks'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    sensor_event_id = db.Column(db.Integer, db.ForeignKey('sensor_event.id'))

class SensorEventFFTRE(db.Model):
    """
    Map the sensor_event_fft_re table in database
    """
    __tablename__ = 'sensor_event_fft_re'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    sensor_event_id = db.Column(db.Integer, db.ForeignKey('sensor_event.id'))

class SensorEventFFTIMG(db.Model):
    """
    Map the sensor_event_fft_img table in database
    """
    __tablename__ = 'sensor_event_fft_img'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    sensor_event_id = db.Column(db.Integer, db.ForeignKey('sensor_event.id'))
from project.models import SensorEvent, SensorEventPeaks, SensorEventFFTRE, SensorEventFFTIMG, Cluster
import time
from sqlalchemy import func
from sklearn.cluster import MeanShift, estimate_bandwidth

class Cluster(object):

    def __init__(self, db, data_limit=1000, sleep_time=2):
        self.db = db
        self.data_limit = data_limit
        self.sleep_time = sleep_time

    def number_to_cluster(self):
        data = self.db.session.query(
            func.count(SensorEvent.id)
        ).filter(
            SensorEvent.clustered == False
        ).first()
        return data[0]

    def has_data_enougth(self):
        return self.number_to_cluster() >= self.data_limit

    def iteration(self):
        if not self.has_data_enougth():
            time.sleep(self.sleep_time)
            return False

    def run(self):
        pass
        # while True:
            
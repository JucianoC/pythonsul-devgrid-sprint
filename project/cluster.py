from project.models import SensorEvent, Cluster
import time
from sqlalchemy import func
from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy

class ClusterFactory(object):
    """
    That class do the collection of database events no already clustered,
    aply the algorithm and save the results.
    """

    def __init__(self, db, data_limit=1000, sleep_time=2):
        self.db = db
        self.data_limit = data_limit
        self.sleep_time = sleep_time

    def number_to_cluster(self):
        """
        Return the number of events that aren't non clustered.
        """
        data = self.db.session.query(
            func.count(SensorEvent.id)
        ).filter(
            SensorEvent.clustered == False
        ).first()
        return data[0]

    def has_data_enougth(self):
        """
        This method return True if the number of non clustered events are greater than the limit.
        """
        to_cluster = self.number_to_cluster()
        return  to_cluster >= self.data_limit

    def get_database_data(self):
        """
        Return the sensor_event info from database.
        """
        return self.db.session.query(SensorEvent).filter(
            SensorEvent.clustered == False
        ).limit(self.data_limit).all()

    def database_to_cluster(self, sensor_event):
        """
        Return a list of informations to be applied to the cluster algorithm, for a sensor_event
        """
        peaks = sensor_event.peaks[:3]
        transients = [peak.value for peak in peaks]
        data = [
            sensor_event.power_active,
            sensor_event.power_reactive,
            sensor_event.power_appearent,
            sensor_event.line_current,
            sensor_event.line_voltage
        ]

        data += transients
        data = [numpy.float32(val) for val in data]
        return data

    def get_cluster_data(self, database_data):
        """
        Return a list of lists to be applied to cluster algorith, for a list of sensor_event
        """
        return [self.database_to_cluster(value) for value in database_data]

    def do_cluster(self, data):
        """
        Run the cluster algorithm
        """
        cluster_info = data
        brandwidth = estimate_bandwidth(cluster_info, quantile=0.2, n_samples=200)
        brandwidth = brandwidth if brandwidth > 0 else None
        mean_shift = MeanShift(bandwidth=brandwidth, cluster_all=False, bin_seeding=True)
        labels = mean_shift.fit_predict(cluster_info)
        return labels

    def save_cluster(self, database_data, labels):
        """
        Save the data result of cluster algorithm
        """
        cluster = Cluster()
        self.db.session.add(cluster)
        self.db.session.commit()

        for i in range(self.data_limit):
            database_data[i].clustered = True
            database_data[i].cluster_id = cluster.id
            database_data[i].cluster_label = int(labels[i])

        self.db.session.commit()
        return cluster

    def ignore_wrong(self, database_data):
        """
        Mark as clustered the list database_data
        """
        for val in database_data:
            val.clustered = True
        self.db.session.commit()

    def iteration(self):
        """
        Perform a iteration of the cluster service
        """
        if not self.has_data_enougth():
            time.sleep(self.sleep_time)
            self.db.session.commit()
            return None
        
        database_data = self.get_database_data()
        cluster_data_list = self.get_cluster_data(database_data)
        try:
            labels = self.do_cluster(cluster_data_list)
        except ValueError:
            self.ignore_wrong(database_data)
            return None

        cluster_db = self.save_cluster(database_data, labels)
        return cluster_db

    def run(self):
        """
        Run a infinite loop, that periodically run the cluster algorithm
        """
        while True:
            result = self.iteration()          
            if not result is None:
                print("New cluster -> ", result.id)
            else:
                print("No enougth data")
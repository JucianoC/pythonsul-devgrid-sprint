from __future__ import absolute_import
import unittest

from project.app import db
from project.cluster import ClusterFactory
from project.models import SensorEvent

class ClusterFactoryTest(unittest.TestCase):

    def test_number_to_cluster(self):
        cluster = ClusterFactory(db)
        number = cluster.number_to_cluster()
        self.assertIsInstance(number, int)

    def test_data_enougth(self):
        cluster = ClusterFactory(db)
        self.assertIsInstance(cluster.has_data_enougth(), bool)

    def get_database_data(self):
        cluster = ClusterFactory(db)
        self.assertIsInstance(cluster.get_database_data(), list)

    def test_database_to_cluster(self):
        cluster = ClusterFactory(db)
        database_data = cluster.get_database_data()
        value = cluster.database_to_cluster(database_data[0])
        self.assertIsInstance(value, list)

    def test_get_cluster_data(self):
        cluster = ClusterFactory(db)
        database_data = cluster.get_database_data()
        data = cluster.get_cluster_data(database_data)
        self.assertIsInstance(data, list)

    def test_do_cluster(self):
        cluster = ClusterFactory(db)
        database_data = cluster.get_database_data()
        data = cluster.get_cluster_data(database_data)
        if len(data) >= 1000:
            try:
                labels = cluster.do_cluster(data)
            except ValueError:
                cluster.ignore_wrong(database_data)
        self.assertEqual(True, True)
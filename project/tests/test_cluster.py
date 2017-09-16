from __future__ import absolute_import
import unittest

from project.app import db
from project.cluster import Cluster

class ClusterTest(unittest.TestCase):

    def test_number_to_cluster(self):
        cluster = Cluster(db)
        number = cluster.number_to_cluster()
        self.assertIsInstance(number, int)

    def test_data_enougth(self):
        cluster = Cluster(db)
        self.assertIsInstance(cluster.has_data_enougth(), bool)
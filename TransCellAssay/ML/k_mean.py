"""
K-mean clustering
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import pandas as pd
import numpy as np
import TransCellAssay as TCA


class k_mean_clustering():
    def __init__(self, Plate):
        assert isinstance(Plate, TCA.Plate)
        self.rawData = Plate.compute_all_features_from_replicat()

    def do_cluster(self):
        from sklearn.cluster import KMeans

        kmeans = KMeans(4, random_state=8)
        label = kmeans.fit(self.rawData.values).labels__
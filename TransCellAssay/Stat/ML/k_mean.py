# coding=utf-8
"""
K-mean clustering based on phenotype
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"

import numpy as np
import TransCellAssay as TCA


class k_mean_clustering():
    """

    :param Plate:
    """

    def __init__(self, plate):
        assert isinstance(plate, TCA.Plate)
        self.rawData = plate.get_agg_data_from_replica_channels()
        self.rawData = self.rawData.drop(['Well'], axis=1)

    def do_cluster(self, n_cluster=10):
        """

        :param n_cluster:
        """
        from sklearn.cluster import KMeans

        kmeans = KMeans(n_cluster, random_state=8)
        kmeans.fit(self.rawData)
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_

        from matplotlib import pyplot

        for i in range(n_cluster):
            # select only data observations with cluster label == i
            ds = self.rawData.values[np.where(labels == i)]
            # plot the data observations
            pyplot.plot(ds[:, 0], ds[:, 1], 'o')
            # plot the centroids
            lines = pyplot.plot(centroids[i, 0], centroids[i, 1], 'kx')
            # make the centroid x's bigger
            pyplot.setp(lines, ms=15.0)
            pyplot.setp(lines, mew=2.0)
        pyplot.show()

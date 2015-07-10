# coding=utf-8
"""
Method for graphics determination of replica correlation
"""

import numpy as np
import TransCellAssay as TCA


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class RepCor(object):
    def __init__(self, plate, channel):
        assert  isinstance(plate, TCA.Plate)
        if not len(plate) > 1:
            raise Exception('Plate must contain at least two replica')
        else:
            plate.agg_data_from_replica_channel(channel=channel, forced_update=True)
            self.arr = self.__create_array(plate)
            self.__triplicate()
            # # OR
            TCA.plot_3d_cloud_point(title='test', x=self.arr[:, 1], y=self.arr[:, 2], z=self.arr[:, 3])

    @staticmethod
    def __create_array(plate):
        __SIZE__ = len(plate.platemap.platemap.values.flatten())
        array = plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
        for key, rep in plate.replica.items():
            array = np.append(array, rep.array.flatten().reshape(__SIZE__, 1), axis=1)
        return array

    def __duplicate(self):
        raise NotImplementedError

    def __triplicate(self):
        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        plt.rcParams['legend.fontsize'] = 10
        ax.plot(self.arr[:, 1], self.arr[:, 2], self.arr[:, 3], '.', markersize=4, color='blue', alpha=0.5,
                label='Correlation')
        ax.plot(np.arange(0, 600, 10), np.arange(0, 600, 10), np.arange(0, 600, 10), color='red', label='perfect')

        ax.set_xlabel('rep1')
        ax.set_ylabel('rep2')
        ax.set_zlabel('rep3')

        plt.title('Correlation between replica')
        ax.legend(loc='upper right')
        plt.show()

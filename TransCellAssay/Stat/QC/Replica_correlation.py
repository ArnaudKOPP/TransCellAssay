# coding=utf-8
"""
In this correction method, the background signal corresponding to each well is calculated by averaging the activities
withing each well across all plate of screen.
Then, a kriging interpolation can be made but not sur for the moment.
We substract then the calculated background to value from plate or replicat.
"""

import numpy as np
import pandas as pd
import TransCellAssay as TCA


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class RepCor(object):
    def __init__(self, plate):
        if not isinstance(plate, TCA.Plate):
            raise TypeError('Must be a Plate object')
        else:
            if not len(plate) > 1:
                raise Exception('Plate must contain at least two replica')
            else:
                self.arr = self.__create_array(plate)
                # self.__triplicate()
                # # OR
                TCA.plot_3d_cloud_point(title='test', x=self.arr[:, 1], y=self.arr[:, 2], z=self.arr[:, 3])

    @staticmethod
    def __create_array(plate):
        __SIZE__ = len(plate.platemap.platemap.values.flatten())
        array = plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
        for key, rep in plate.replica.items():
            if rep.array is not None:
                array = np.append(array, rep.array.flatten().reshape(__SIZE__, 1), axis=1)
            else:
                raise Exception('Determine first array mean for replica')
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

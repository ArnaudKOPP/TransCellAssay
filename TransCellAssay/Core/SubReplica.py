# coding=utf-8
"""
Class for manipulating Subreplicat
"""

from TransCellAssay.Core.Replica import Replica
from TransCellAssay.Utils import get_opposite_well_format
import numpy as np

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "KOPP Arnaud"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class SubReplica(Replica):
    """
    class for creating sub replicat from previous replicat
    """

    def __init__(self, parent_replicat, rb, re, cb, ce):
        """
        Constructor
        :param parent_replicat: Replicat Parent object
        :param rb: Row Begin
        :param re: Row End
        :param cb: Col Begin
        :param ce: Col End
        """
        try:
            if isinstance(parent_replicat, Replica):
                Replica.__init__(self)
                self.ParentReplicat = parent_replicat
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must Provided Replicat for creating SubReplicat")

            self.rawdata = parent_replicat.rawdata
            self.name = parent_replicat.name

            self.isNormalized = parent_replicat.isNormalized
            self.isSpatialNormalized = parent_replicat.isSpatialNormalized

            self.datatype = parent_replicat.datatype
            if parent_replicat.array is None:
                self.array = None
            else:
                self.array = parent_replicat.array[rb - 1: re - 1, cb - 1: ce - 1]
            if parent_replicat.sec_array is None:
                self.sec_array = None
            else:
                self.sec_array = parent_replicat.sec_array[rb - 1: re - 1, cb - 1: ce - 1]

            self.rb = rb
            self.re = re
            self.cb = cb
            self.ce = ce

        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def compute_data_for_channel(self, channel, data_type="median"):
        """
        Compute data in matrix form, get mean or median for well and save them in replicat object
        :param data_type: median or mean data
        :param channel: which channel to keep in matrix
        :return:
        """
        try:
            if not self.isNormalized:
                print('!!! \033[0;33m[WARNING]\033[0m   !!!')
                print('     --> Data are not normalized for replicat : ', self.name)
                print('')

            grouped_data_by_well = self.rawdata.groupby('Well')

            if data_type == "median":
                tmp = grouped_data_by_well.mean()
            else:
                tmp = grouped_data_by_well.median()
            channel = tmp[channel]
            dict_mean = channel.to_dict()  # # dict : key = pos and item are mean
            if not len(dict_mean) > 96:
                data = np.zeros((8, 12))
            else:
                data = np.zeros((16, 24))
            for key, elem in dict_mean.items():
                pos = get_opposite_well_format(key)
                data[pos[0]][pos[1]] = elem

            self.array = data[self.rb - 1: self.re - 1, self.cb - 1: self.ce - 1]

        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return ("\n SubReplicat : " + repr(self.name) +
                    "\n Normalized Data : " + repr(self.isNormalized) +
                    "\n Spatial Normalized : " + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        """
        try:
            return self.__repr__()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

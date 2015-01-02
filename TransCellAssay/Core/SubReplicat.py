# coding=utf-8
"""
Class for manipulating Subreplicat
"""

from TransCellAssay.Core.Replicat import Replicat
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


class SubReplicat(Replicat):
    """
    class for creating sub replicat from previous replicat
    """

    def __init__(self, parent_replicat, RB, RE, CB, CE):
        """
        Constructor
        :param parent_replicat: Replicat Parent object
        :param RB: Row Begin
        :param RE: Row End
        :param CB: Col Begin
        :param CE: Col End
        """
        try:
            if isinstance(parent_replicat, Replicat):
                Replicat.__init__(self)
                self.ParentReplicat = parent_replicat
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must Provided Replicat for creating SubReplicat")

            self.RawData = parent_replicat.RawData
            self.name = parent_replicat.name

            self.isNormalized = parent_replicat.isNormalized
            self.isSpatialNormalized = parent_replicat.isSpatialNormalized

            self.DataType = parent_replicat.DataType
            if parent_replicat.Data is None:
                self.Data = None
            else:
                self.Data = parent_replicat.Data[RB - 1: RE - 1, CB - 1: CE - 1]
            if parent_replicat.SECData is None:
                self.SECData = None
            else:
                self.SECData = parent_replicat.SECData[RB - 1: RE - 1, CB - 1: CE - 1]

            self.RB = RB
            self.RE = RE
            self.CB = CB
            self.CE = CE

        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def compute_data_for_feature(self, feature, data_type="median"):
        """
        Compute data in matrix form, get mean or median for well and save them in replicat object
        :param data_type: median or mean data
        :param feature: which feature to keep in matrix
        :return:
        """
        try:
            if not self.isNormalized:
                print('!!! \033[0;33m[WARNING]\033[0m   !!!')
                print('     --> Data are not normalized for replicat : ', self.name)
                print('')

            grouped_data_by_well = self.RawData.groupby('Well')

            if data_type == "median":
                tmp = grouped_data_by_well.mean()
            else:
                tmp = grouped_data_by_well.median()
            feature = tmp[feature]
            dict_mean = feature.to_dict()  # # dict : key = pos and item are mean
            if not len(dict_mean) > 96:
                data = np.zeros((8, 12))
            else:
                data = np.zeros((16, 24))
            for key, elem in dict_mean.items():
                pos = get_opposite_well_format(key)
                data[pos[0]][pos[1]] = elem

            self.Data = data[self.RB - 1: self.RE - 1, self.CB - 1: self.CE - 1]

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
            return ("\n SubReplicat : " + repr(self.name) +
                    "\n Normalized Data : " + repr(self.isNormalized) +
                    "\n Spatial Normalized : " + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

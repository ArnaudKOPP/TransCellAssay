"""
Class for manipulating Subreplicat
"""

import Core
import numpy as np
import pandas as pd
import Utils

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "KOPP Arnaud"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class SubReplicat(Core.Replicat):
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
            if isinstance(parent_replicat, Core.Replicat):
                Core.Replicat.__init__(self)
                self.ParentReplicat = parent_replicat
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must Provided Replicat for creating SubReplicat")

            self.Dataframe = parent_replicat.Dataframe
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
            print(e)

    def computeDataForFeature(self, feature, data_type="median"):
        """
        Compute data in matrix form, get mean or median for well and save them in replicat object
        :param: feature: which feature to keep in matrix
        :return:
        """
        try:
            if not self.isNormalized:
                print('!!! \033[0;33m[WARNING]\033[0m   !!!')
                print('     --> Data are not normalized for replicat : ', self.name)
                print('')

            grouped_data_by_well = self.Dataframe.groupby('Well')

            if data_type == "median":
                tmp = grouped_data_by_well.mean()
            else:
                tmp = grouped_data_by_well.median()
            feature = tmp[feature]
            dict_mean = feature.to_dict()  # # dict : key = pos and item are mean
            if not len(dict_mean) > 96:
                Data = np.zeros((8, 12))
            else:
                Data = np.zeros((16, 24))
            for key, elem in dict_mean.items():
                pos = Utils.WellFormat.getOppositeWellFormat(key)
                Data[pos[0]][pos[1]] = elem

            self.Data = Data[self.RB - 1: self.RE - 1, self.CB - 1: self.CE - 1]

        except Exception as e:
            print(e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return ("\n SubReplicat : " + repr(self.name) +
                    "\n Normalized Data : " + repr(self.isNormalized) +
                    "\n Spatial Normalized : " + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print(e)

    def __str__(self):
        """
        Definition for the print
        """
        try:
            return ("\n SubReplicat : " + repr(self.name) +
                    "\n Normalized Data : " + repr(self.isNormalized) +
                    "\n Spatial Normalized : " + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print(e)
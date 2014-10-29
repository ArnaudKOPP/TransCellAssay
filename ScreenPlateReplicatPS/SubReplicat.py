"""
Class for manipulating Subreplicat
"""

import ScreenPlateReplicatPS
import numpy as np
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "KOPP Arnaud"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class SubReplicat(ScreenPlateReplicatPS.Replicat):
    def __init__(self, parent_replicat, RB, RE, CB, CE):
        """
        Constructor
        """
        try:
            if isinstance(parent_replicat, ScreenPlateReplicatPS.Replicat):
                ScreenPlateReplicatPS.Replicat.__init__(self)
                self.ParentReplicat = parent_replicat
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must Provided Replicat for creating SubReplicat")

            self.Dataframe = parent_replicat.Dataframe
            self.name = parent_replicat.name

            self.isNormalized = parent_replicat.isNormalized
            self.isSpatialNormalized = parent_replicat.isSpatialNormalized

            self.DataType = parent_replicat.DataType
            self.Data = parent_replicat.Data[RB - 1: RE - 1, CB - 1: CE - 1]
            self.SECData = parent_replicat.SECData[RB - 1: RE - 1, CB - 1: CE - 1]

        except Exception as e:
            print(e)

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        try:
            return ("\n SubReplicat : \n " + repr(self.name) +
                    "\n Normalized Data : \n" + repr(self.isNormalized) +
                    "\n Spatial Normalized : \n" + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print(e)

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        try:
            return ("\n SubReplicat : \n " + repr(self.name) +
                    "\n Normalized Data : \n" + repr(self.isNormalized) +
                    "\n Spatial Normalized : \n" + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print(e)
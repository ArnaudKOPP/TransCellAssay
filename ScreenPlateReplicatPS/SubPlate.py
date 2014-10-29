"""
Class for manipulating sub Plate object, sub Plate can serve in case that plate are not full or we focus only on part
of Plate
"""

import ScreenPlateReplicatPS
import numpy as np
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class SubPlate(ScreenPlateReplicatPS.Plate):
    def __init__(self, parent_plate, RB=None, RE=None, CB=None, CE=None):
        """
        Constructor
        """
        try:
            if isinstance(parent_plate, ScreenPlateReplicatPS.Plate):
                ScreenPlateReplicatPS.Plate.__init__(self)
                self.ParentPlate = parent_plate
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must Provided Plate for creating SubPlate")
            self._init_replicat(parent_plate.replicat)
            self.MetaInfo = parent_plate.MetaInfo
            self.Name = parent_plate.Name

            self.PlateSetup = parent_plate.PlateSetup.platesetup[RB - 1: RE - 1, CB - 1, CE - 1]
            self.Threshold = parent_plate.Threshold
            self.ControlPos = None

            self.Neg = parent_plate.Neg
            self.Pos = parent_plate.Pos
            self.Tox = parent_plate.Tox

            self.Result = parent_plate.Result
            self.isNormalized = parent_plate.isNormalized
            self.isSpatialNormalized = parent_plate.isSpatialNormalized

            self.DataType = parent_plate.DataType
            self.Data = parent_plate.Data[RB - 1: RE - 1, CB - 1, CE - 1]
            self.SECData = parent_plate.SECData[RB - 1: RE - 1, CB - 1, CE - 1]
        except Exception as e:
            print(e)

    def _init_replicat(self, plate, RB=None, RE=None, CB=None, CE=None):
        try:
            for key, value in plate.replicat.items():
                self.replicat[value.name] = ScreenPlateReplicatPS.SubReplicat(value, RB=None, RE=None, CB=None, CE=None)
        except Exception as e:
            print(e)

    def __add__(self, replicat):
        """
        Add replicat object, use + operator
        :param replicat:
        """
        try:
            assert isinstance(replicat, ScreenPlateReplicatPS.SubReplicat)
            name = replicat.name
            self.replicat[name] = replicat
        except Exception as e:
            print(e)

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        try:
            return (
                "\n SubPlate : \n" + repr(self.Name) +
                "\n MetaInfo : \n" + repr(self.MetaInfo) +
                "\n PlateSetup : \n" + repr(self.PlateSetup) +
                "\n Array Result :\n" + repr(self.Result) +
                "\n Data normalized ?" + repr(self.isNormalized) +
                "\n Data systematic error removed ? : \n" + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replicat))
        except Exception as e:
            print(e)

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        try:
            return (
                "\n SubPlate : \n" + repr(self.Name) +
                "\n MetaInfo : \n" + repr(self.MetaInfo) +
                "\n PlateSetup : \n" + repr(self.PlateSetup) +
                "\n Array Result :\n" + repr(self.Result) +
                "\n Data normalized ?" + repr(self.isNormalized) +
                "\n Data systematic error removed ? : \n" + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replicat))
        except Exception as e:
            print(e)
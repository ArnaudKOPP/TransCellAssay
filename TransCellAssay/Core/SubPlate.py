# coding=utf-8
"""
Class for manipulating sub Plate object, sub Plate can serve in case that plate are not full or we focus only on part
of Plate
"""
from TransCellAssay.Core import Plate
from TransCellAssay.Core.SubReplicat import SubReplicat
import collections

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class SubPlate(Plate):
    """
    Class subplate for creating subplate from plate
    """

    def __init__(self, parent_plate, RB, RE, CB, CE):
        """
        Constructor
        :param parent_plate: Plate Parent object
        :param RB: Row Begin
        :param RE: Row End
        :param CB: Col Begin
        :param CE: Col End
        """
        try:
            if isinstance(parent_plate, Plate):
                Plate.__init__(self)
                self.ParentPlate = parent_plate
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must Provided Plate for creating SubPlate")
            self.replicat = collections.OrderedDict()
            self._init_replicat(parent_plate, RB, RE, CB, CE)
            self.MetaInfo = parent_plate.MetaInfo
            self.Name = parent_plate.Name

            self.PlateMap = parent_plate.PlateMap.platemap.iloc[RB - 1: RE - 1, CB - 1: CE - 1]
            self.Threshold = parent_plate.Threshold
            self.ControlPos = None

            self.Neg = parent_plate.Neg
            self.Pos = parent_plate.Pos
            self.Tox = parent_plate.Tox

            self.isNormalized = parent_plate.isNormalized
            self.isSpatialNormalized = parent_plate.isSpatialNormalized

            self.DataType = parent_plate.DataType
            if parent_plate.Data is None:
                self.Data = None
            else:
                self.Data = parent_plate.Data[RB - 1: RE - 1, CB - 1: CE - 1]
            if parent_plate.SECData is None:
                self.SECData = None
            else:
                self.SECData = parent_plate.SECData[RB - 1: RE - 1, CB - 1: CE - 1]

            self.RB = RB
            self.RE = RE
            self.CB = CB
            self.CE = CE

        except Exception as e:
            print(e)

    def _init_replicat(self, plate, RB, RE, CB, CE):
        """
        select zone in replicat and put them into a dict
        :param plate: Plate object
        :param RB: Row Begin
        :param RE: Row End
        :param CB: Col Begin
        :param CE: Col End
        """
        try:
            for key, value in plate.replicat.items():
                self.replicat[value.name] = SubReplicat(value, RB, RE, CB, CE)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __add__(self, replicat):
        """
        Add replicat object, use + operator
        :param replicat:
        """
        try:
            assert isinstance(replicat, SubReplicat)
            name = replicat.name
            self.replicat[name] = replicat
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return (
                "\n SubPlate : " + repr(self.Name) +
                "\n MetaInfo : \n" + repr(self.MetaInfo) +
                "\n PlateMap : \n" + repr(self.PlateMap) +
                "\n Data normalized ? " + repr(self.isNormalized) +
                "\n Data systematic error removed ? " + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replicat) + "\n")
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

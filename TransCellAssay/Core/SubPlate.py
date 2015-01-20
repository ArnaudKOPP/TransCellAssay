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
            self._meta_info = parent_plate._meta_info
            self.name = parent_plate.name

            self.platemap = parent_plate.platemap.platemap.iloc[RB - 1: RE - 1, CB - 1: CE - 1]
            self.threshold = parent_plate.threshold
            self._control_position = None

            self._neg = parent_plate._neg
            self._pos = parent_plate._pos
            self._tox = parent_plate._tox

            self.isNormalized = parent_plate.isNormalized
            self.isSpatialNormalized = parent_plate.isSpatialNormalized

            self.datatype = parent_plate.datatype
            if parent_plate.array is None:
                self.array = None
            else:
                self.array = parent_plate.array[RB - 1: RE - 1, CB - 1: CE - 1]
            if parent_plate.sec_array is None:
                self.sec_array = None
            else:
                self.sec_array = parent_plate.sec_array[RB - 1: RE - 1, CB - 1: CE - 1]

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
                "\n SubPlate : " + repr(self.name) +
                "\n PlateMap : \n" + repr(self.platemap) +
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

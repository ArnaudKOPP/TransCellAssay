# coding=utf-8
"""
Platemap is designed to store matrix who represent the plate map, compatible with 96, 384 Well (1526 is tricky)
The matrix is representing by a pandas DataFrame (numpy array like)

design in csv file must follow this
    1   2   3   4   5   ..
A   XX
B
C
D
E
..
"""

import os
import pandas as pd
import numpy as np
from TransCellAssay import Utils as Utils
import collections
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class PlateMap(object):
    """
    classdocs
    Class for manipuling platemap
    self.platesetup = pd.DataFrame() # pandas dataframe object that contain the platemap, use this module for more
        easy manipulation of different type into array (more easy that numpy)
    """

    def __init__(self, platemap=None):
        """
        Constructor
        """
        self.platemap = pd.DataFrame()
        if platemap is not None:
            self.set_platemap(platemap)
        self._is_cutted = False
        self._rb = None
        self._re = None
        self._cb = None
        self._ce = None

    def set_platemap(self, platemap_file=None):
        """
        Define platemap
        Read csv with first row as column name and first column as row name
        :param platemap_file: csv file with platemap
        """
        if os.path.isfile(platemap_file):
            log.info('Reading PlateMap %s File' % platemap_file)
            self.platemap = pd.read_csv(platemap_file, index_col=0)
        else:
            raise IOError('File don\'t exist')

    def shape(self):
        """
        get the shape of platemap, so we can determine number of well
        :return: shape of platemap
        """
        return self.platemap.shape

    def search_coord(self, to_search):
        """
        Search position of the gene and return coord
        :param to_search: gene to search
        :return: list of coord
        """
        list_coord = [x for x in zip(*np.where(self.platemap.values == to_search))]
        if len(list_coord) < 1:
            raise KeyError('This gene don\'t exist: %s' % to_search)
        return list_coord

    def search_well(self, to_search):
        """
        Search position of the gene and return Well (list if multiple)
        :param to_search: gene to search
        :return: list of Well
        """
        list_well = [Utils.get_opposite_well_format(x) for x in zip(*np.where(self.platemap.values == to_search))]
        if len(list_well) < 1:
            raise KeyError('This gene don\'t exist: %s' % to_search)
        return list_well

    def as_dict(self):
        """
        Return Platemap as a dict
        :return: dataframe
        """
        mat = self.platemap.as_matrix()  # # transform PS dataframe into numpy matrix
        size = mat.shape  # # get shape of matrix
        row = size[0]
        col = size[1]
        map_as_dict = collections.OrderedDict()
        for r in range(row):
            for c in range(col):
                pos = (r, c)
                genename = mat[r][c]
                if not genename == "":  # # check if empty well
                    well = Utils.get_opposite_well_format(pos)
                    map_as_dict[well] = genename
        return map_as_dict

    def as_matrix(self):
        """
        Return PS as numpy array
        :return: numpy array
        """
        return self.platemap.as_matrix()

    def cut(self, rb, re, cb, ce):
        """
        Cut platemap
        :param rb: row begin
        :param re: row end
        :param cb: col begin
        :param ce: col end
        :return:
        """
        if self._is_cutted:
            raise AttributeError('Already cutted')
        self.platemap = self.platemap.iloc[rb: re, cb: ce]
        self._is_cutted = True
        self._rb = rb
        self._re = re
        self._cb = cb
        self._ce = ce

    def __getitem__(self, position):
        """
        Return geneName from specified position
        A1 = (0,0)
        :param position: A1 or (0, 0)
        :return: string geneName of platesetup
        """
        # # for (0, 0) format
        if isinstance(position, tuple):
            return self.platemap.iloc[position[0], position[1]]
        # # for 'A1' format
        elif isinstance(position, str):
            return self.platemap.loc[[position[0]], [position[1:]]]

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        return "PlateMap: \n" + repr(self.platemap) + "\n"

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        return self.__repr__()
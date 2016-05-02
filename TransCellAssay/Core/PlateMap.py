# coding=utf-8
"""
Platemap is designed to store matrix who represent the plate map, compatible with 96, 384 Well (1536 is tricky)
The matrix is representing by a pandas DataFrame (numpy array like)

design in csv file must follow this
    1   2   3   4   5   ..
A   XX
B
C
D
E

if 1536 layout, only this one is supported

    1   2   3    ...... 48
A
B
..
AE
AF

The goal of this object is to store location of multiple control or bank product, we can get all well for one product
..
"""

import os
import pandas as pd
import numpy as np
from TransCellAssay import Utils as Utils
import collections
import string
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class PlateMap(object):
    """
    Class for manipulating platemap
    self.platemap = pd.DataFrame()      # pandas dataframe object that contain the platemap, use this module for more
                                            easy manipulation of different type into array (more easy that numpy)
    self._is_cutted = False             # Bool for know if plate are cutted or no
    self._rb = None                     # row begin of cutting operation
    self._re = None                     # row end of cutting operation
    self._cb = None                     # col begin of cutting operation
    self._ce = None                     # col end of cutting operation
    """

    def __init__(self, fpath=None, size=96,**kwargs):
        """
        Constructor
        :param fpath: file path from csv file, if no one is provided, a generic platemap is created
        :param size: default size for platemap if not file is provided
        :param kwargs: add param for pandas arg reading
        """
        log.debug('Created PlateMap')
        self.__file = None
        if fpath is not None:
            self.set_platemap(fpath, **kwargs)
            self.__file = fpath
        else:
            self.generate_empty_platemap(size=size)
            log.debug('Generic platemap created')
        self._is_cutted = False
        self._rb = None
        self._re = None
        self._cb = None
        self._ce = None

    def set_platemap(self, file_path=None, **kwargs):
        """
        Define platemap, read a csv file with first row as column name and first column as row name
        :param file_path: csv file with platemap
        :param kwargs: add param for pandas arg reading
        """
        if os.path.isfile(file_path):
            log.info('Reading PlateMap %s File' % file_path)
            self.platemap = pd.read_csv(file_path, index_col=0, header=0, **kwargs)
        else:
            raise IOError('File don\'t exist')

    def shape(self, alt_frmt=False):
        """
        Get the shape of platemap, so we can determine number of well
        :param alt_frmt: if true, return 96, 384 or 1536 well format, if False return numpy shape (8,12)
        :return: shape of platemap
        """
        if alt_frmt:
            return self.platemap.shape[0] * self.platemap.shape[1]
        else:
            return self.platemap.shape

    def search_coord(self, elem):
        """
        Search position of the gene and return coord (list if multiple)
        raise keyerror if element not found
        :param elem: gene to search
        :return: list of coord
        """
        if not isinstance(elem, list):
            elem = [elem]
        list_wells = []
        for well in elem:
            list_wells.extend(self.__search_element(well))
        return list_wells

    def search_well(self, elem):
        """
        Search position of the gene and return Well (list if multiple)
        raise keyerror if element not found
        :param elem: gene to search
        :return: list of Well
        """
        if not isinstance(elem, list):
            elem = [elem]
        list_wells = []
        for well in elem:
            list_wells.extend(self.__search_element(well))
        res = [Utils.get_opposite_well_format(x) for x in list_wells]
        return res

    def __search_element(self, elem):
        list_coord = [x for x in zip(*np.where(self.platemap.values == elem))]
        if len(list_coord) < 1:
            raise KeyError('This element don\'t exist: %s' % elem)
        return list_coord

    def as_dict(self):
        """
        Return Platemap as a dict
        :return: dataframe
        """
        mat = self.platemap.as_matrix()  # # transform platemap into numpy matrix
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

    def as_array(self):
        """
        return platemap as numpy array with Well and PlateMap
        :return:
        """
        data = self.as_dict()
        array = np.array([(key, val) for (key, val) in data.items()], {'formats': ['object', 'object'], 'names': ['Well', 'PlateMap']})
        return array

    def as_matrix(self):
        """
        Return PS as numpy array
        :return: numpy array
        """
        return self.platemap.as_matrix()

    def cut(self, rb, re, cb, ce):
        """
        Cut the platemap with specified coordinate
        :param rb: row begin
        :param re: row end
        :param cb: col begin
        :param ce: col end
        :return:
        """
        if self._is_cutted:
            raise AttributeError('Already cutted')
        log.debug('Cutting operation on platemap (param {0}:{1},{2}:{3})'.format(rb, re, cb, ce))
        self.platemap = self.platemap.iloc[rb: re, cb: ce]
        self._is_cutted = True
        self._rb = rb
        self._re = re
        self._cb = cb
        self._ce = ce

    def generate_empty_platemap(self, size=96):
        """
        Generate an empty platemap with defined size
        :param size: number of well for plate, only 96,384 or 1536
        """
        df = self._generate_empty(size=size)
        self.platemap = self._fill_empty(df)


    @staticmethod
    def _generate_empty(size=96):
        if int(size) == 96:
            df = pd.DataFrame(data='Empty',index=list(string.ascii_uppercase)[0:8],
                            columns=[str(x) for x in range(1, 13, 1)])
            return df
        elif int(size) == 384:
            df = pd.DataFrame(data='Empty',index=list(string.ascii_uppercase)[0:16],
                            columns=[str(x) for x in range(1, 25, 1)])
            return df
        elif int(size) == 1536:
            df = pd.DataFrame(data='Empty',index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                                                             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                                             'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF'],
                            columns=[str(x) for x in range(1, 49, 1)])
            return df
        else:
            raise ValueError('Expected size : 96, 384 or 1536')

    @staticmethod
    def _fill_empty(df):
        for r in df.index:
            for c in df.columns:
                df.loc[r, c] = str(r)+str(c)
        return df

    def get_file_location(self):
        """
        return file location if available
        :return:
        """
        if self.__file is not None:
            return self.__file
        else:
            return 'Not available'

    def __setitem__(self, key, value):
        """
        Set geneName from specified position
        :param key: position (A1 or (0, 0))
        :param value: string genename for well
        """
        # # for (0, 0) format
        if isinstance(key, tuple):
            self.platemap.iloc[int(key[0]), int(key[1])] = str(value)
        # # for 'A1' format
        elif isinstance(key, str):
            self.platemap.loc[str(key[0]), str(key[1:])] = str(value)

    def __getitem__(self, position):
        """
        Return geneName from specified position
        A1 = (0,0)
        :param position: A1 or (0, 0)
        :return: string geneName of plateMap
        """
        # # for (0, 0) format
        if isinstance(position, tuple):
            return self.platemap.iloc[int(position[0]), int(position[1])]
        # # for 'A1' format
        elif isinstance(position, str):
            return self.platemap.loc[str(position[0]), str(position[1:])]

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        return "\nPlateMap: \n" + repr(self.platemap) + "\nPlateMap File location :"+repr(self.__file) + "\n"

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        return self.__repr__()

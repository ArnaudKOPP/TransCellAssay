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
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class PlateMap(object):
    """
    Class for manipulating platemap
    self.platemap = pd.DataFrame()      # pandas dataframe object that contain the platemap, use this module for more
                                            easy manipulation of different type into array (more easy that numpy)
    self._is_cutted = False             # Bool for know if plate are cutted
    self._rb = None                     # row begin
    self._re = None                     # row end
    self._cb = None                     # col begin
    self._ce = None                     # col end
    """

    def __init__(self, fpath=None, size=96,**kwargs):
        """
        Constructor
        :param fpath: file path from csv file
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
        self._is_cutted = False
        self._rb = None
        self._re = None
        self._cb = None
        self._ce = None

    def set_platemap(self, file_path=None, **kwargs):
        """
        Define platemap
        Read csv with first row as column name and first column as row name
        :param file_path: csv file with platemap
        :param kwargs: add param for pandas arg reading
        """
        if os.path.isfile(file_path):
            log.info('Reading PlateMap %s File' % file_path)
            self.platemap = pd.read_csv(file_path, index_col=0, **kwargs)
        else:
            raise IOError('File don\'t exist')

    def shape(self, alt_frmt=False):
        """
        get the shape of platemap, so we can determine number of well
        :return: shape of platemap
        """
        if alt_frmt:
            return self.platemap.shape[0] * self.platemap.shape[1]
        else:
            return self.platemap.shape

    def search_coord(self, elem):
        """
        Search position of the gene and return coord (list of multiple)
        :param elem: gene to search
        :return: list of coord
        """
        list_coord = [x for x in zip(*np.where(self.platemap.values == elem))]
        if len(list_coord) < 1:
            raise KeyError('This element don\'t exist: %s' % elem)
        return list_coord

    def search_well(self, elem):
        """
        Search position of the gene and return Well (list if multiple)
        :param elem: gene to search
        :return: list of Well
        """
        list_well = [Utils.get_opposite_well_format(x) for x in zip(*np.where(self.platemap.values == elem))]
        if len(list_well) < 1:
            raise KeyError('This element don\'t exist: %s' % elem)
        return list_well

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
        return platemap as numpy array with genename and well
        :return:
        """
        data = self.as_dict()
        names = ['Well', 'GeneName']
        formats = ['object', 'object']
        dtype = dict(names=names, formats=formats)
        array = np.array([(key, val) for (key, val) in data.items()], dtype)
        return array

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
        if int(size) == 96:
            self.__generate_empty_96()
        elif int(size) == 384:
            self.__generate_empty_384()
        elif int(size) == 1536:
            self.__generate_empty_1536()
        else:
            raise ValueError('Expected size : 96, 348 or 1536')

    def __generate_empty_96(self):
        self.platemap = pd.DataFrame(data='Empty',index=list(string.ascii_uppercase)[0:8], columns=range(1, 9, 1))
        self.__fill_empty()

    def __generate_empty_384(self):
        self.platemap = pd.DataFrame(data='Empty',index=list(string.ascii_uppercase)[0:16], columns=range(1, 25, 1))
        self.__fill_empty()

    def __generate_empty_1536(self):
        self.platemap = pd.DataFrame(data='Empty',index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                                                         'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                                         'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF'],
                                     columns=range(1, 49, 1))
        self.__fill_empty()

    def __fill_empty(self):
        for r in self.platemap.index:
            for c in self.platemap.columns:
                self.platemap.loc[r, c] = str(r)+str(c)

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
            self.platemap.loc[str(key[0]), int(key[1:])] = str(value)

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
            return self.platemap.loc[str(position[0]), int(position[1:])]

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        return "\nPlateMap: \n" + repr(self.platemap) + "\nFile location ->"+repr(self.__file) + "\n"

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        return self.__repr__()
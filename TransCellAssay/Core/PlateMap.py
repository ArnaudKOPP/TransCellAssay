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

import pandas as pd
from TransCellAssay import Utils as Utils

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

    def set_platemap(self, platemap_file=None):
        """
        Define platemap
        Read csv with first row as column name and first column as row name
        :param platemap_file: csv file with platemap
        """
        try:
            self.platemap = pd.read_csv(platemap_file, index_col=0)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_platemap(self):
        """
        Return platemap
        :return: platemap (dataframe)
        """
        try:
            return self.platemap
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_platemape_shape(self):
        """
        get the shape of platemap, so we can determine number of well
        :return: shape of platemap
        """
        try:
            return self.platemap.shape
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_coord(self, to_search):
        """
        Search position of the gene and return coord
        :param to_search: gene to search
        :return: list of coord
        """
        try:
            mat = self.platemap.as_matrix()  # # transform PS dataframe into numpy matrix
            size = mat.shape  # # get shape of matrix
            list_coord = []
            # # TODO alternative (more fast)
            # [x for x in zip(*np.where(mat == 'to_search'))]
            for r in range(size[0]):
                for c in range(size[1]):
                    if to_search == mat[r][c]:
                        list_coord.append((r, c))
            if not list_coord:
                raise AttributeError('\033[0;31m[ERROR]\033[0m  This gene don\'t exist: %s' % to_search)
            return list_coord
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_well(self, to_search):
        """
        Search position of the gene and return Well (list if multiple)
        :param to_search: gene to search
        :return: list of Well
        """
        try:
            mat = self.platemap.as_matrix()  # # transform PS dataframe into numpy matrix
            size = mat.shape  # # get shape of matrix
            row = size[0]
            col = size[1]
            list_well = list()
            for r in range(row):
                for c in range(col):
                    if mat[r][c] == to_search:
                        list_well.append(Utils.get_opposite_well_format((r, c)))
            if not list_well:
                raise AttributeError('\033[0;31m[ERROR]\033[0m  This gene don\'t exist: %s' % to_search)
            return list_well
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_map_as_dict(self):
        """
        Return Platemap as a dict
        :return: dataframe
        """
        try:
            mat = self.platemap.as_matrix()  # # transform PS dataframe into numpy matrix
            size = mat.shape  # # get shape of matrix
            row = size[0]
            col = size[1]
            map_as_dict = {}
            for r in range(row):
                for c in range(col):
                    pos = (r, c)
                    genename = mat[r][c]
                    if not genename == "":  # # check if empty well
                        well = Utils.get_opposite_well_format(pos)
                        map_as_dict[well] = genename
            return map_as_dict
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_map_as_matrix(self):
        """
        Return PS as numpy array
        :return: numpy array
        """
        try:
            return self.platemap.as_matrix()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __getitem__(self, position):
        """
        Return geneName from specified position
        A1 = (0,0)
        :param position: A1 or (0, 0)
        :return: string geneName of platesetup
        """
        try:
            # # for (0, 0) format
            if isinstance(position, tuple):
                return self.platemap.iloc[position[0], position[1]]
            # # for 'A1' format
            elif isinstance(position, str):
                return self.platemap.loc[[position[0]], [position[1:]]]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        try:
            return "PlateMap: \n" + repr(self.platemap) + "\n"
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        try:

            return "PlateMap: \n" + repr(self.platemap) + "\n"
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

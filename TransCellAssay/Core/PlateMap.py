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
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class PlateMap():
    """
    classdocs
    Class for manipuling platemap
    self.platesetup = pd.DataFrame() # pandas dataframe object that contain the platemap, use this module for more
        easy manipulation of different type into array (more easy that numpy)
    """

    def __init__(self, ):
        """
        Constructor
        """
        self.platemap = pd.DataFrame()

    def setPlateSetup(self, InputFile=None):
        """
        Define platemap
        Read csv with first row as column name and first column as row name
        :param InputFile: csv file with platemap
        """
        try:
            self.platemap = pd.read_csv(InputFile, index_col=0)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getPlateSetup(self):
        """
        Return platemap
        :return: platemap (dataframe)
        """
        try:
            return self.platemap
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getSize(self):
        """
        get the shape of platemap, so we can determine number of well
        :return: shape of platemap
        """
        try:
            return self.platemap.shape
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getGenePos(self, gene):
        """
        Search position of the gene and return coord
        :return: list of coord
        """
        try:
            mat = self.platemap.as_matrix()  # # transform PS dataframe into numpy matrix
            size = mat.shape  # # get shape of matrix
            CoordList = []
            for r in range(size[0]):
                for c in range(size[1]):
                    if gene == mat[r][c]:
                        CoordList.append((r, c))
            if not CoordList:
                raise AttributeError('\033[0;31m[ERROR]\033[0m  This gene don\'t exist')
            return CoordList
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getGeneWell(self, gene):
        """
        Search position of the gene and return Well (list if multiple)
        :return: list of Well
        """
        try:
            mat = self.platemap.as_matrix()  # # transform PS dataframe into numpy matrix
            size = mat.shape  # # get shape of matrix
            row = size[0]
            col = size[1]
            CoordList = list()
            for r in range(row):
                for c in range(col):
                    if mat[r][c] == gene:
                        CoordList.append(Utils.getOppositeWellFormat((r, c)))
            if not CoordList:
                raise AttributeError('\033[0;31m[ERROR]\033[0m  This gene don\'t exist')
            return CoordList
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getMapAsDict(self):
        """
        Return Platemap as a dict
        :return: dataframe
        """
        try:
            mat = self.platemap.as_matrix()  # # transform PS dataframe into numpy matrix
            size = mat.shape  # # get shape of matrix
            row = size[0]
            col = size[1]
            dict = {}
            for r in range(row):
                for c in range(col):
                    pos = (r, c)
                    genename = mat[r][c]
                    if not genename == "":  # # check if empty well
                        well = Utils.getOppositeWellFormat(pos)
                        dict[well] = genename
            return dict
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getMapAsMatrix(self):
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
            return "A PlateSetup object: \n" + repr(self.platemap) + "\n"
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        try:

            return "A PlateSetup object: \n" + repr(self.platemap) + "\n"
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)
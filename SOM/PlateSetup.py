"""
Platesetup is designed to store matrix who represent the plate setup, compatible with 96, 384 Well (1526 is tricky)
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
import Utils.WellFormat as Utils

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class PlateSetup():
    """
    classdocs
    Class for manipuling platesetup
    self.platesetup = pd.DataFrame() # pandas dataframe object that contain the platesetup, use this module for more
        easy manipulation of different type into array (more easy that numpy)
    """

    def __init__(self, ):
        """
        Constructor
        """
        self.platesetup = pd.DataFrame()

    def setPlateSetup(self, InputFile=None):
        """
        Define platesetup
        Read csv with first row as column name and first column as row name
        :param InputFile: csv file with platesetup
        """
        try:
            self.platesetup = pd.read_csv(InputFile, index_col=0)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getPlateSetup(self):
        """
        Return platesetup
        :return: platesetup (dataframe)
        """
        try:
            return self.platesetup
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getSize(self):
        """
        get the shape of platesetup, so we can determine number of well
        :return: shape of platesetup
        """
        try:
            return self.platesetup.shape
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getGenePos(self, gene):
        """
        Search position of the gene and return coord
        :return: list of coord
        """
        try:
            mat = self.platesetup.as_matrix()  # # transform PS dataframe into numpy matrix
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
            print(e)

    def getGeneWell(self, gene):
        """
        Search position of the gene and return Well (list if multiple)
        :return: list of Well
        """
        try:
            mat = self.platesetup.as_matrix()  # # transform PS dataframe into numpy matrix
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
            print(e)

    def getPSasDict(self):
        """
        Return Platesetup as a dict
        :return: dataframe
        """
        try:
            mat = self.platesetup.as_matrix()  # # transform PS dataframe into numpy matrix
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

    def getPSasMatrix(self):
        """
        Return PS as numpy array
        :return: numpy array
        """
        try:
            return self.platesetup.as_matrix()
        except Exception as e:
            print(e)

    def __getitem__(self, position, human_readable=False):
        """
        Return geneName from specified position
        A1 = (0,0)
        :param position: A1 or (0, 0)/(1, 1)
        :param human_readable: for human index A1 = (1, 1)
        :return: string geneName of platesetup
        """
        try:
            # # for (1, 1) format
            if isinstance(position, tuple):
                if human_readable:
                    return self.platesetup.iloc[position[0] - 1, position[1] - 1]
                else:
                    return self.platesetup.iloc[position[0], position[1]]
            # # for 'A1' format
            elif isinstance(position, str):
                return self.platesetup.loc[[position[0]], [position[1]]]
        except Exception as e:
            print(e)

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        try:
            return "A PlateSetup object: \n" + repr(self.platesetup) + "\n"
        except Exception as e:
            print(e)

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        try:

            return "A PlateSetup object: \n" + repr(self.platesetup) + "\n"
        except Exception as e:
            print(e)
__author__ = 'Arnaud KOPP'
"""
Platesetup is designed to store matrix who represent the plate setup, he is compatible with 96, 384, ... Well
The matrix is representing by a pandas DataFrame (numpy array like)
"""
import pandas as pd
import TCA.Utils as Utils


class PlateSetup():
    '''
    classdocs
    Class for manipuling platesetup
    '''

    def __init__(self, ):
        '''
        Constructor init
        :return: nothing
        '''
        self.platesetup = pd.DataFrame()

    def setPlateSetup(self, InputFile=None):
        '''
        Define platesetup
        Read csv with first row as column name and first column as row name
        :param InputFile: csv file with platesetup
        :return: nothing
        '''
        try:
            self.platesetup = pd.read_csv(InputFile, index_col=0)
        except Exception as e:
            print(e)

    def getPlateSetup(self):
        '''
        Return platesetup in dataframe
        :return: platesetup (dataframe)
        '''
        try:
            return self.platesetup
        except Exception as e:
            print(e)
            print('Error in getting platesetup')

    def getSize(self):
        '''
        get the shape of platesetup, so we can determine number of well
        :return: shape of platesetup
        '''
        try:
            return self.platesetup.shape
        except Exception as e:
            print(e)

    def getGenePos(self, gene):
        '''
        Search position of the gene and return coord
        :return: coord
        '''
        try:
            mat = self.platesetup.as_matrix()  # # transform PS dataframe into numpy matrix
            size = mat.shape  # # get shape of matrix
            row = size[0]
            col = size[1]
            for r in range(row):
                for c in range(col):
                    if gene == mat[r][c]:
                        return row, col
            print('Gene not found')
        except Exception as e:
            print(e)
            print('Error occured at getGenePos')

    def getPSasDict(self):
        '''
        Return Platesetup as a dict
        :return: dataframe
        '''
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
            print(e)
            print('Error occured at getPSasList')

    def getPSasMatrix(self):
        '''
        Return PS as numpy array
        :return: numpy array
        '''
        try:
            return self.platesetup.as_matrix()
        except Exception as e:
            print(e)
            print('Error in getting matrix of platesetup')

    def __repr__(self):
        '''
        Definition for the representation
        :return:
        '''
        try:
            return "A PlateSetup object: " + repr(self.platesetup)
        except Exception as e:
            print(e)

    def __str__(self):
        '''
        Definition for the print
        :return:
        '''
        try:
            return "Platesetup: \n " + repr(self.platesetup)
        except Exception as e:
            print(e)
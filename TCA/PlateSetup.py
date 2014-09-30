__author__ = 'Arnaud KOPP'
"""
Platesetup is designed to store matrix who represent the plate setup, he is compatible with 96, 384, ... Well
The matrix is representing by a pandas DataFrame (numpy array like)
"""
import pandas as pd


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

    def printPlateSetup(self):
        '''
        Print platesetup
        :return: print platesetup
        '''
        try:
            print(self.platesetup)
        except Exception as e:
            print(e)
            print('Error when printing platesetup')

    def getGenePos(self, gene):
        '''
        Search position of the gene and return coord
        :return: coord
        '''
        try:
            mat = self.platesetup.as_matrix()  # # get dataframe into numpy matrix
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

    def getPSasList(self):
        '''
        Return Platesetup as a list (dataframe)
        :return: dataframe
        '''
        try:
            # TODO Make matrix as list here
            return 0
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
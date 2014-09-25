__author__ = 'Arnaud KOPP'

import numpy as np


class Result():
    '''
    Class for representing record array for result
    '''


    def __init__(self, size):
        '''
        Constructor
        :return:
        '''
        self.Data = np.zeros(size, dtype=[('GeneName', object), ('Well', object), ('CellsCount', int),
                                          ('PositiveCells', float), ('Infection', float), ('Toxicity', float),
                                          ('SSMDr', float), ('SSMDrSpatNorm', float)])


    def addGene(self, GeneList):
        '''
        Add gene into the record Array in the first column
        :param GeneList:
        :return:
        '''
        try:
            return 0
        # TODO implement this
        except Exception as e:
            print(e)


    def addCol(self, colName):
        '''

        :param col:
        :return:
        '''
        try:
            return 0
        except Exception as e:
            print(e)


    def getCol(self, col):
        '''

        :param col:
        :return:
        '''
        try:
            return 0
        except Exception as e:
            print(e)


    def save(self, FilePath):
        '''
        Save Result Array into csv
        :param FilePath:
        :return:
        '''
        try:
            np.savetxt(FilePath, self.Data, delimiter=';')
        except Exception as e:
            print(e)

    def getGeneEffectCount(self):
        '''

        :return:
        '''
        try:
            # TODO
            return 0
        except Exception as e:
            print(e)
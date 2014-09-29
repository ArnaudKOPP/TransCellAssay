__author__ = 'Arnaud KOPP'
"""
Result is created for store result in a tabe-like (numpy array), feature are column and GeneName/Well are stored at the
first col, each row represent a gene/well
We can save the tabe in csv by using pandas Dataframe.
"""
import numpy as np
import pandas as pd


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
        self.GenePos = {}  # # To save Gene position in numpy Array

    def addGene(self, GeneList):
        '''
        Add gene into the record Array in the first column
        :param GeneList:
        :return:
        '''
        try:
            for i in GeneList:
                self.GenePos[GeneList[i]] = i
                self.Data['GeneName'][i] = GeneList[i]
        except Exception as e:
            print(e)


    def addCol(self, colName):
        '''
        Add column to result array
        :param col:
        :return:
        '''
        try:
            # TODO maybe don't need that
            return 0
        except Exception as e:
            print(e)


    def addValue(self, Gene, Feature, Value):
        '''
        Insert Value at Gene row and Feature Col
        :param Gene:
        :param Feature:
        :param Value:
        :return:
        '''
        try:
            self.Data[Feature][self.GenePos[Gene]] = Value
        except Exception as e:
            print(e)


    def getCol(self, col):
        '''
        Get col/feature from result array
        :param col:
        :return: return numpy array
        '''
        try:
            return self.Data[col]
        except ValueError:
            print('No Valid Column Name')


    def save(self, FilePath):
        '''
        Save Result Array into csv
        :param FilePath:
        :return:
        '''
        try:
            tmp = pd.DataFrame(self.Data)
            tmp.to_csv(FilePath)
        except:
            try:
                np.savetxt(FilePath, self.Data, delimiter=';')
            except Exception as e:
                print(e)
                print('Error in saving results data')

    def getGeneEffectCount(self):
        '''
        getGeneEffectCount on SSMD col
        :return: don't know now
        '''
        try:
            return 0
        except Exception as e:
            print(e)
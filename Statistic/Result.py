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

    def __init__(self, size=None):
        '''
        Constructor
        if size is not given, init by 386 plate size
        :return: none init only dataframe
        '''
        if size == None:
            size = 396
        self.Data = np.zeros(size, dtype=[('GeneName', object), ('Well', object), ('CellsCount', int),
                                          ('SDCellsCunt', float), ('PositiveCells', float), ('Infection', float),
                                          ('Toxicity', float), ('SSMDr', float), ('SSMDrSpatNorm', float)])
        self.GenePos = {}  # # To save GeneName (key)and  Gene position (value)
        self.GenePosI = {}  # # To save Well (key) and Gene position (value)

    def getData(self):
        '''
        return data array
        :return: array
        '''
        try:
            return self.Data
        except Exception as e:
            print(e)

    def initGeneWell(self, GeneList):
        '''
        Add gene and well into the record Array in the first/second column
        :param GeneList: Dict with key are Well and Value are geneName
        :return:
        '''
        try:
            i = 0
            for k, v in GeneList.items():
                self.Data['GeneName'][i] = v
                self.Data['Well'][i] = k
                self.GenePos[v] = i
                self.GenePosI[k] = i
                i += 1
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

    def addDict(self, dict, Feature, by):
        '''
        Insert Value from a dict where key = GeneName/pos and Value are value to insert
        :param dict: dict that contain value to insert with key are GeneName or Pos/Well
        :param Feature:
        :param by: insert by GeneName or Well
        :return:
        '''
        try:
            for item, value in dict.items():
                if by == 'GeneName':
                    self.Data[Feature][self.GenePos[item]] = value
                elif by == 'Pos':
                    self.Data[Feature][self.GenePosI[item]] = value
                else:
                    print("Error")
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

"""
Result is created for store result like score and hit resulting of SSMD or other technics in a tabe-like (numpy array),
feature are column and GeneName/Well are stored at the first col, each row represent a gene/well
We can save the tabe in csv by using pandas Dataframe.

This class store data with dict in input, where key are well and item are data.

"""

import numpy as np
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class Result(object):
    """
    Class for representing record array for result
    """

    def __init__(self, size=None):
        """
        Constructor
        if size is not given, init by 386 plate size, defined size if 96 or 1526 plate well
        :return: none init only dataframe
        """
        if size == None:
            size = 384
        self.Data = np.zeros(size, dtype=[('GeneName', object), ('Well', object), ('CellsCount', float),
                                          ('SDCellsCunt', float), ('PositiveCells', float), ('SDPositiveCells', float),
                                          ('mean', float), ('median', float), ('std', float), ('stdm', float),
                                          ('Viability', float), ('Toxicity', float)])

        self.GenePos = {}  # # To save GeneName (key)and  Gene position (value)
        self.GenePosI = {}  # # To save Well (key) and Gene position (value)

    def getData(self):
        """
        return data array
        :return: array
        """
        try:
            return self.Data
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def initGeneWell(self, GeneList):
        """
        Add gene and well into the record Array in the first/second column
        :param GeneList: Dict with key are Well and Value are geneName
        :return:
        """
        try:
            i = 0
            for k, v in GeneList.items():
                self.Data['GeneName'][i] = v
                self.Data['Well'][i] = k
                self.GenePos.setdefault(v, []).append(i)  # # make this form because Gene can be in multiple Well
                self.GenePosI[k] = i
                i += 1
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def addValue(self, Gene, Feature, Value):
        """
        Insert Value at Gene row and Feature Col
        If GeneName is contain in multiple Well, it will be
        :param Gene:
        :param Feature:
        :param Value:
        :return:
        """
        try:
            if len(self.GenePos[Gene]) > 1:  # # loop in case geneName is in multiple Well
                for i in (self.GenePos[Gene]):
                    self.Data[Feature][i] = Value
            else:
                self.Data[Feature][self.GenePos[Gene]] = Value
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def addDataDict(self, datadict, Feature, by='Pos'):
        """
        Insert Value from a dict where key = GeneName/pos and Value are value to insert
        Prefer by = pos in case of empty well
        :param datadict: dict that contain value to insert with key are GeneName or Pos/Well
        :param Feature:
        :param by: insert by GeneName or Well
        :return:
        """
        try:
            for item, value in datadict.items():
                if by == 'GeneName':
                    print(
                        " !! \033[0;33m[WARNING]\033[0m  !! addDataDict with by=GeneName is not fully stable in case of empty Well")
                    print("     Prefer by=Pos")
                    if len(self.GenePos[item]) > 1:
                        for i in (self.GenePos[item]):
                            self.Data[Feature][i] = value
                    else:
                        self.Data[Feature][self.GenePos[item]] = value
                elif by == 'Pos':
                    self.Data[Feature][self.GenePosI[item]] = value
                else:
                    print("\033[0;31m[ERROR]\033[0m")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getCol(self, col):
        """
        Get col/feature from result array
        :param col:
        :return: return numpy array
        """
        try:
            return self.Data[col]
        except ValueError:
            print('\033[0;31m[ERROR]\033[0m  No Valid Column Name')

    def save(self, FilePath):
        """
        Save Result Array into csv
        :param FilePath:
        :return:
        """
        try:
            tmp = pd.DataFrame(self.Data)
            tmp.to_csv(FilePath, index=False)
        except:
            try:
                np.savetxt(FilePath, self.Data, delimiter=';')
            except Exception as e:
                print('\033[0;31m[ERROR]\033[0m  Error in saving results data', e)

    def __add__(self, other):
        """
        add result object to other one MERGING Function
        :param other: other Résult object
        :return:
        """
        try:
            print('Not yet implemented')
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        try:
            return "Result object: " + repr(pd.DataFrame(self.Data))
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        try:
            return "Result Array: \n " + repr(pd.DataFrame(self.Data))
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)
__author__ = 'Arnaud KOPP'

import pandas as pd


class PlateSetup():
    def __init__(self,):
        '''
        Constructor init
        :return: nothing
        '''
        self.platesetup = pd.DataFrame()


    def setplatesetup(self, InputFile=None):
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


    def printplatesetup(self):
        '''
        Print platesetup
        :return: print platesetup
        '''
        try:
            print(self.platesetup)
        except Exception as e:
            print(e)


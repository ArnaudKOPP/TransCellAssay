__author__ = 'Arnaud KOPP'

import pandas as pd


class Replicat():
    '''
    classdocs
    Class for manipuling replicat of plate
    '''

    def __init__(self,):
        '''
        Constructor
        :return: nothing
        '''
        self.Data = pd.DataFrame()


    def setdata(self, InputFile):
        '''
        Set data in replicat
        :param InputFile: csv file
        :return: nothing
        '''

        try:
            self.Data = pd.read_csv(InputFile)
        except:
            try:
                self.data = pd.read_csv(input, decimal=",", sep=";")
            except Exception as e:
                print(e)
                print('Error in reading %s File' % (InputFile))


    def getdata(self):
        '''
        Get Data
        :return: Data
        '''
        return self.Data
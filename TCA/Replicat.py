__author__ = 'Arnaud KOPP'
"""
Replicat implement the notion of technical replicat for one plate
"""
import pandas as pd


class Replicat():
    '''
    classdocs
    Class for manipuling replicat of plate
    '''

    def __init__(self, ):
        '''
        Constructor
        :return: nothing
        '''
        self.Data = pd.DataFrame()
        self.info = ""
        self.isNormalized = False
        self.isSpatialNormalized = False

    def setData(self, InputFile):
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

    def getData(self):
        '''
        Get all Data
        :return: DataFrame with all data
        '''
        try:
            return self.Data
        except Exception as e:
            print(e)
            print('Error in exporting data')


    def setInfo(self, info):
        '''
        set info like name
        :param info: info on replicat
        :return:
        '''
        try:
            self.info = info
        except Exception as e:
            print(e)
            print('Error in setting Info')

    def getInfo(self):
        '''
        return info from replicat
        :return: info
        '''
        try:
            return self.info
        except Exception as e:
            print(e)
            print('Error in getting info')

    def printInfo(self):
        '''
        print info from replicat
        :return: nothing
        '''
        print(self.info)


    def getDataByWell(self, well):
        '''
        Get all data for well
        :param well:
        :return: dataframe with data for specified well
        '''
        try:
            return self.Data[self.Data['Well'] == well]
        except Exception as e:
            print(e)
            print('Error in exporting data by well')


    def getDataByFeatures(self, featList):
        '''
        Return a data frame with Well col and features data col in list []
        if no Well col is given, then auto add
        :param featList: give a list with feature in [] format
        :return: output a dataframe with Well col and feature col
        '''
        try:
            if not "Well" in featList:
                featList.insert(0, 'Well')
                return self.Data[featList]
            else:
                return self.Data[featList]
        except Exception as e:
            print(e)

    def getDataMatrixForm(self, feature):
        '''
        Return data in matrix form, get mean or median for well
        :return:
        '''
        try:
            # TODO
            return 0
        except Exception as e:
            print(e)
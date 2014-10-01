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
        self.IsSingleCell = True  # If Single Cell data, default is True because design for this data
        self.SpatNormData = None  # matrix that contain data corrected by median polish

    def setData(self, InputFile):
        '''
        Set data in replicat
        :param InputFile: csv file
        :return: nothing
        '''
        try:
            self.Data = pd.read_csv(InputFile)
            print('Reading %s File' % (InputFile))
        except:
            try:
                self.data = pd.read_csv(input, decimal=",", sep=";")
                print('Reading %s File' % (InputFile))
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

    def getDataMatrixForm(self, feature, method="mean"):
        '''
        Return data in matrix form, get mean or median for well
        :param: feature: which feature to keep in matrix
        :param: method: which method to choose mean or median
        :return:
        '''
        try:
            if method == "mean":
                tmp = self.Data.groupby('Well')
                mean = tmp.mean()
                value = mean[feature]['']
            else:
                tmp = self.Data.groupby('Well')
                median = tmp.median()
                return 0
        except Exception as e:
            print(e)

    def __repr__(self):
        '''
        Definition for the representation
        :return:
        '''
        try:
            return ("\n Replicat : \n " + repr(self.info) + "\n Normalized Data \n:" + repr(self.isNormalized) +
                    "\n Spatial Normalized : \n" + repr(self.isSpatialNormalized) + "\n Single Cell Data : \n" +
                    repr(self.IsSingleCell) + "\n Data containing in this replicat" + repr(
                self.Data) + "\n Spatial normalized Data containing \n" + repr(self.SpatNormData))
        except Exception as e:
            print(e)

    def __str__(self):
        '''
        Definition for the print
        :return:
        '''
        try:
            return ("\n Replicat : \n " + repr(self.info) + "\n Normalized Data \n:" + repr(self.isNormalized) +
                    "\n Spatial Normalized : \n" + repr(self.isSpatialNormalized) + "\n Single Cell Data : \n" +
                    repr(self.IsSingleCell) + "\n Data containing in this replicat" + repr(
                self.Data) + "\n Spatial normalized Data containing \n" + repr(self.SpatNormData))
        except Exception as e:
            print(e)

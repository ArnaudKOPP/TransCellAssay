__author__ = 'Arnaud KOPP'
"""
Replicat implement the notion of technical replicat for one plate
"""
import pandas as pd
import numpy as np
import Statistic.Normalization
import Utils


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
        self.DataMatrixMean = None  # matrix that contain mean of interested features to analyze
        self.DataMatrixMedian = None  # matrix that contain median of interested feature to analyze
        self.SpatNormDataMean = None  # matrix that contain data corrected by median polish (bscore) or others technics
        self.SpatNormDataMedian = None  # matrix that contain data corrected by median polish (bscore) or others technics

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

    def getDataByWell(self, well):
        '''
        Get all data for well
        :param well: get well position like A1
        :return: dataframe with data for specified well
        '''
        try:
            return self.Data[self.Data['Well'] == well]
        except Exception as e:
            print(e)
            print('Error in exporting data by well')

    def getDataByWells(self, feature, wells):
        '''
        get all data for specified wellS
        :param wells: list of wells
        :return: return dataframe with data specified wells
        '''
        try:
            data = pd.DataFrame()
            for i in wells:
                if data.empty:
                    data = self.Data[feature][self.Data['Well'] == i]
                data.append(self.Data[feature][self.Data['Well'] == i])
            return data
        except Exception as e:
            print(e)
            print('Error in exporting data for wells')

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

    def computeDataMatrixForFeature(self, feature):
        '''
        Return data in matrix form, get mean or median for well
        :param: feature: which feature to keep in matrix
        :param: method: which method to choose mean or median
        :return: compute data in matrix form
        '''
        try:

            groupbydata = self.Data.groupby('Well')

            mean_tmp = groupbydata.mean()
            mean_feature = mean_tmp[feature]
            dict_mean = mean_feature.to_dict()  # # dict : key = pos and item are mean
            if not len(dict_mean) > 96:
                self.DataMatrixMean = np.zeros((8, 12))
            else:
                self.DataMatrixMean = np.zeros((16, 24))
            for key, elem in dict_mean.items():
                pos = Utils.Utils.getOppositeWellFormat(key)
                self.DataMatrixMean[pos[0]][pos[1]] = elem

            groupbydata_mean = groupbydata.median()
            median_feature = groupbydata_mean[feature]
            dict_mean = median_feature.to_dict()  # # dict : key = pos and item are mean
            if not len(dict_mean) > 96:
                self.DataMatrixMedian = np.zeros((8, 12))
            else:
                self.DataMatrixMedian = np.zeros((16, 24))
            for key, elem in dict_mean.items():
                pos = Utils.Utils.getOppositeWellFormat(key)
                self.DataMatrixMedian[pos[0]][pos[1]] = elem
        except Exception as e:
            print(e)

    def getDataMatrix(self, feature, method="mean"):
        '''
        Return data in matrix form, get mean or median for well
        :param: feature: which feature to keep in matrix
        :param: method: which method to choose mean or median
        :return: compute data in matrix form
        '''
        try:
            if method == "mean":
                if self.DataMatrixMean == None:
                    self.computeDataMatrixForFeature(feature)
                return self.DataMatrixMean
            else:
                if self.DataMatrixMedian == None:
                    self.computeDataMatrixForFeature(feature)
                return self.DataMatrixMedian
        except Exception as e:
            print(e)


    def BScoreNormalization(self, verbose, save=False):
        '''
        Apply a median polish for remove edge effect
        residual matrix are save in replicat object
        :param:  verbose : output the result ?
        :param: save: save the residual into self.SpatNormData , default = False
        :return:
        '''
        try:
            if self.DataMatrixMean == None:
                print("Compute Mean of replicat first by using computeDataMatrixForFeature")
                return 0
            else:
                mp = Statistic.Normalization.MedianPolish(self.DataMatrixMean)
                ge, ce, re, resid, tbl_org = mp.median_polish(100)
                if verbose:
                    print("")
                    print("median polish:   MeanData for replicat ", self.info)
                    print("grand effect = ", ge)
                    print("column effects = ", ce)
                    print("row effects = ", re)
                    print("-----Table of Residuals-------")
                    print(resid)
                    print("-----Original Table-------")
                    print(tbl_org)
                    print("")
                if save:
                    self.SpatNormDataMean = resid
                    self.isSpatialNormalized = True

            if self.DataMatrixMedian == None:
                print("Compute Median of replicat first by using computeDataMatrixForFeature")
                return 0
            else:
                mp = Statistic.Normalization.MedianPolish(self.DataMatrixMedian)
                ge, ce, re, resid, tbl_org = mp.median_polish(100)
                if verbose:
                    print("median polish:    MeanData for replicat ", self.info)
                    print("grand effect = ", ge)
                    print("column effects = ", ce)
                    print("row effects = ", re)
                    print("-----Table of Residuals-------")
                    print(resid)
                    print("-----Original Table-------")
                    print(tbl_org)
                    print("")
                if save:
                    self.SpatNormDataMedian = resid
                    self.isSpatialNormalized = True
        except Exception as e:
            print(e)


def __repr__(self):
    '''
    Definition for the representation
    :return:
    '''
    try:
        return ("\n Replicat : \n " + repr(self.info) + "\n Normalized Data \n:" + repr(
            self.isNormalized) + "\n Spatial Normalized : \n" + repr(
            self.isSpatialNormalized) + "\n Data containing in this replicat :\n" + repr(
            self.Data) + "\n Spatial normalized Data containing \n" + repr(self.SpatNormData) +
                "\n Matrix Mean data of feature \n" + repr(self.DataMatrixMean) + "\n Matrix Median of feature \n" +
                repr(self.DataMatrixMedian))
    except Exception as e:
        print(e)


def __str__(self):
    '''
    Definition for the print
    :return:
    '''
    try:
        return ("\n Replicat : \n " + repr(self.info) + "\n Normalized Data \n:" + repr(
            self.isNormalized) + "\n Spatial Normalized : \n" + repr(
            self.isSpatialNormalized) + "\n Data containing in this replicat :\n" + repr(
            self.Data) + "\n Spatial normalized Data containing \n" + repr(self.SpatNormData) +
                "\n Matrix Mean data of feature \n" + repr(self.DataMatrixMean) + "\n Matrix Median of feature \n" +
                repr(self.DataMatrixMedian))
    except Exception as e:
        print(e)

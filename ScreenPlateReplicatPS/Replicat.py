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
        self.Data = pd.DataFrame()  # data frame that contains data
        self.info = ""  # Name of replicat
        self.isNormalized = False  # Well correction or somethings else
        self.isSpatialNormalized = False  # systematics error removed or not
        self.DataMean = None  # matrix that contain mean of interested features to analyze
        self.DataMedian = None  # matrix that contain median of interested feature to analyze
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

    def getDataByFeatures(self, featList, Well=False):
        '''
        Return a data frame with Well col and features data col in list []
        if no Well col is given, then auto add
        :param featList: give a list with feature in [] format
        :param Well: if we want to have Well col in data
        :return: output a dataframe with Well col and feature col
        '''
        try:
            if Well:
                featList.insert(0, 'Well')
                return self.Data[featList]
            else:
                return self.Data[featList]
        except Exception as e:
            print(e)

    def computeDataForFeature(self, feature):
        '''
        Compute data in matrix form, get mean or median for well and save them in replicat object
        :param: feature: which feature to keep in matrix
        :return:
        '''
        try:
            if not self.isNormalized:
                print('!!! Warnings !!!')
                print('     --> Data are not normalized for replicat : ', self.info)
                print('')

            grouped_data_by_well = self.Data.groupby('Well')

            mean_tmp = grouped_data_by_well.mean()
            mean_feature = mean_tmp[feature]
            dict_mean = mean_feature.to_dict()  # # dict : key = pos and item are mean
            if not len(dict_mean) > 96:
                self.DataMean = np.zeros((8, 12))
            else:
                self.DataMean = np.zeros((16, 24))
            for key, elem in dict_mean.items():
                pos = Utils.Utils.getOppositeWellFormat(key)
                self.DataMean[pos[0]][pos[1]] = elem

            median_tmp = grouped_data_by_well.median()
            median_feature = median_tmp[feature]
            dict_median = median_feature.to_dict()  # # dict : key = pos and item are mean
            if not len(dict_median) > 96:
                self.DataMedian = np.zeros((8, 12))
            else:
                self.DataMedian = np.zeros((16, 24))
            for key, elem in dict_median.items():
                pos = Utils.Utils.getOppositeWellFormat(key)
                self.DataMedian[pos[0]][pos[1]] = elem
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
                if self.DataMean is None:
                    self.computeDataForFeature(feature)
                return self.DataMean
            else:
                if self.DataMedian is None:
                    self.computeDataForFeature(feature)
                return self.DataMedian
        except Exception as e:
            print(e)

    def Normalization(self, feature, method, log=True):
        '''
        Performed normalization on data
        :param: feature; which feature to normalize
        :param method: Performed X Transformation
        :param log:  Performed log2 Transformation
        '''
        try:
            if not self.isNormalized:
                self.Data = Statistic.Normalization.VariabilityNormalization(self.Data.copy(), feature=feature,
                                                                             method=method, log2_transformation=log)
                self.isNormalized = True
            else:
                print("Data are already normalized")
                raise Exception
        except Exception as e:
            print(e)

    def SystematicErrorCorrection(self, Methods='Bscore', verbose=False, save=False, max_iterations=100):
        '''

        Apply a spatial normalization for remove edge effect
        The Bscore method showed a more stable behavior than MEA and PMP only when the number of rows and columns
        affected by the systematics error, hit percentage and systematic error variance were high (mainly du to a
        mediocre performance of the t-test in this case). MEA was generally the best method for correcting
        systematic error within 96-well plates, whereas PMP performed better for 384 /1526 well plates.

        :param Methods: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param verbose: Output in console
        :param save: save the result into self.SpatNormData, default = False
        :param max_iterations: maximum iterations loop, default = 100
        '''

        try:
            if Methods == 'Bscore':
                if self.DataMean is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Mean of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.MedianPolish(self.DataMean.copy(),
                                                                                      max_iterations=max_iterations,
                                                                                      verbose=verbose)
                    if save:
                        self.SpatNormDataMean = resid

                if self.DataMedian is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Median of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.MedianPolish(self.DataMedian.copy(),
                                                                                      max_iterations=max_iterations,
                                                                                      verbose=verbose)
                    if save:
                        self.SpatNormDataMedian = resid
                        self.isSpatialNormalized = True

            if Methods == 'BZscore':
                if self.DataMean is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Mean of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.BZMedianPolish(self.DataMean.copy(),
                                                                                        max_iterations=max_iterations,
                                                                                        verbose=verbose)
                    if save:
                        self.SpatNormDataMean = resid

                if self.DataMedian is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Median of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.BZMedianPolish(self.DataMedian.copy(),
                                                                                        max_iterations=max_iterations,
                                                                                        verbose=verbose)
                    if save:
                        self.SpatNormDataMedian = resid
                        self.isSpatialNormalized = True

            if Methods == 'PMP':
                if self.DataMean is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Mean of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    resid = Statistic.Normalization.PartialMeanPolish(self.DataMean.copy(),
                                                                      max_iteration=max_iterations, verbose=verbose)
                    if save:
                        self.SpatNormDataMean = resid

                if self.DataMedian is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Median of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    resid = Statistic.Normalization.PartialMeanPolish(self.DataMedian.copy(),
                                                                      max_iteration=max_iterations, verbose=verbose)
                    if save:
                        self.SpatNormDataMedian = resid
                        self.isSpatialNormalized = True

            if Methods == 'MEA':
                if self.DataMean is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Mean of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    resid = Statistic.Normalization.MatrixErrorAmendment(self.DataMean.copy(), verbose=verbose)
                    if save:
                        self.SpatNormDataMean = resid

                if self.DataMedian is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Median of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    resid = Statistic.Normalization.MatrixErrorAmendment(self.DataMedian.copy(), verbose=verbose)
                    if save:
                        self.SpatNormDataMedian = resid
                        self.isSpatialNormalized = True

            if Methods == 'DiffusionModel':
                if self.DataMean is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Mean of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    CorrectedTable = Statistic.Normalization.diffusionModel(self.DataMean,
                                                                            max_iterations=max_iterations,
                                                                            verbose=verbose)

                    if save:
                        self.SpatNormDataMedian = CorrectedTable
                        self.isSpatialNormalized = True

                if self.DataMedian is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Median of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    CorrectedTable = Statistic.Normalization.diffusionModel(self.DataMedian,
                                                                            max_iterations=max_iterations,
                                                                            verbose=verbose)

                    if save:
                        self.SpatNormDataMedian = CorrectedTable
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
                self.isSpatialNormalized))
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
                self.isSpatialNormalized))
        except Exception as e:
            print(e)

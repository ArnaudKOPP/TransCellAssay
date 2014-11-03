"""
Replicat implement the notion of technical replicat for one plate
"""

import pandas as pd
import numpy as np
import TransCellAssay as TCA

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class Replicat():
    """
    classdocs
    Class for manipuling replicat of plate
    self.Dataframe = pd.DataFrame()  # data frame that contains data
    self.info = ""  # Name of replicat
    self.isNormalized = False  # are the data normalized
    self.isSpatialNormalized = False  # systematics error removed or not
    self.DataType = "median" # median or mean of data
    self.Data = None  # matrix that contain mean of interested features to analyze
    self.SpatNormData = None  # matrix that contain data corrected
    """

    def __init__(self):
        '''
        Constructor
        '''
        self.Dataframe = pd.DataFrame()
        self.name = ""

        self.isNormalized = False
        self.isSpatialNormalized = False

        self.DataType = "median"
        self.Data = None
        self.SECData = None

    def setData(self, InputFile):
        """
        Set data in replicat
        :param InputFile: csv file
        """
        try:
            self.Dataframe = pd.read_csv(InputFile)
            print('Reading %s File' % InputFile)
        except:
            try:
                self.Dataframe = pd.read_csv(input, decimal=",", sep=";")
                print('Reading %s File' % InputFile)
            except Exception as e:
                print(e)
                print('\033[0;31m[ERROR]\033[0m  Error in reading %s File' % InputFile)

    def getData(self):
        """
        Get all Data from dataframe
        :return: return DataFrame with all data
        """
        try:
            return self.Dataframe
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def setDataX(self, Array, type):
        """
        Set attribut data matrix into self.Data
        This method is designed for 1Data/Well or for manual analysis
        :param Array: numpy array with good shape
        :param type: median or mean data
        """
        try:
            if isinstance(Array, np.ndarray):
                self.Data = Array
                if type == 'median':
                    self.DataType = type
                elif type == 'mean':
                    self.DataType = type
                else:
                    raise AttributeError("\033[0;31m[ERROR]\033[0m Must provided data type")
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must provided numpy ndarray")
        except Exception as e:
            print(e)

    def setName(self, info):
        """
        set name for the replicat
        :param info: info on replicat
        :return:
        """
        try:
            self.name = info
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getName(self):
        """
        return name from replicat
        :return: info
        """
        try:
            return self.name
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getDataByWell(self, well, feature=None):
        """
        Get all data for well
        :param well: get well position like A1
        :param feature: can have data for specified feature
        :return: dataframe with data for specified well
        """
        try:
            if feature is None:
                return self.Dataframe[self.Dataframe['Well'] == well]
            else:
                return self.Dataframe[feature][self.Dataframe['Well'] == well]
        except Exception as e:
            print(e)

    def getDataByWells(self, wells, feature=None):
        """
        get all data for specified wellS
        :param wells: list of wells
        :param feature: can have data for specified feature or not
        :return: return dataframe with data specified wells
        """
        try:
            data = None
            for i in wells:
                print(i)
                if feature is None:
                    if data is None:
                        data = self.Dataframe[self.Dataframe['Well'] == i]
                    data.append(self.Dataframe[self.Dataframe['Well'] == i])
                else:
                    if data is None:
                        data = self.Dataframe[feature][self.Dataframe['Well'] == i]
                    data.append(self.Dataframe[feature][self.Dataframe['Well'] == i])
            return data
        except Exception as e:
            print(e)

    def getDataByFeatures(self, featList, Well=False):
        """
        Return a data frame with Well col and features data col in list []
        if no Well col is given, then auto add
        :param featList: give a list with feature in [] format
        :param Well: if we want to have Well col in data
        :return: output a dataframe with Well col and feature col
        """
        try:
            if Well:
                featList.insert(0, 'Well')
                return self.Dataframe[featList]
            else:
                return self.Dataframe[featList]
        except Exception as e:
            print(e)

    def computeDataForFeature(self, feature):
        """
        Compute data in matrix form, get mean or median for well and save them in replicat object
        :param: feature: which feature to keep in matrix
        :return:
        """
        try:
            if not self.isNormalized:
                print('!!! \033[0;33m[WARNING]\033[0m   !!!')
                print('     --> Data are not normalized for replicat : ', self.name)
                print('')

            grouped_data_by_well = self.Dataframe.groupby('Well')
            if self.DataType == 'median':
                tmp = grouped_data_by_well.median()
            else:
                tmp = grouped_data_by_well.mean()
            feature = tmp[feature]
            dict_mean = feature.to_dict()  # # dict : key = pos and item are mean
            if not len(dict_mean) > 96:
                self.Data = np.zeros((8, 12))
            else:
                self.Data = np.zeros((16, 24))
            for key, elem in dict_mean.items():
                pos = TCA.Utils.WellFormat.getOppositeWellFormat(key)
                self.Data[pos[0]][pos[1]] = elem

        except Exception as e:
            print(e)

    def getDataMatrix(self, feature, SEC=False):
        """
        Return data in matrix form, get mean or median for well
        :param: feature: which feature to keep in matrix
        :param: method: which method to choose mean or median default = mean
        :param: SEC: want Systematic Error Corrected data ? default=False
        :return: compute data in matrix form
        """
        try:
            if SEC:
                if self.SECData is None:
                    raise ValueError('\033[0;31m[ERROR]\033[0m  Launch Systematic Error Correction before')
                else:
                    return self.SECData
            elif self.Data is None:
                self.computeDataForFeature(feature)
            return self.Data

        except Exception as e:
            print(e)

    def Normalization(self, feature, method='Zscore', log=True, neg=None, pos=None):
        """
        Performed normalization on data
        :param: feature; which feature to normalize
        :param method: Performed X Transformation
        :param log:  Performed log2 Transformation
        """
        try:
            if not self.isNormalized:
                self.Dataframe = TCA.VariabilityNormalization(self.Dataframe, feature=feature, method=method,
                                                              log2_transformation=log,
                                                              Cneg=neg, Cpos=pos)
                self.isNormalized = True
            else:
                raise Exception("\033[0;33m[WARNING]\033[0m Data are already normalized")
        except Exception as e:
            print(e)

    def SystematicErrorCorrection(self, Algorithm='Bscore', method='median', verbose=False, save=False,
                                  max_iterations=100):
        """

        Apply a spatial normalization for remove edge effect
        The Bscore method showed a more stable behavior than MEA and PMP only when the number of rows and columns
        affected by the systematics error, hit percentage and systematic error variance were high (mainly du to a
        mediocre performance of the t-test in this case). MEA was generally the best method for correcting
        systematic error within 96-well plates, whereas PMP performed better for 384 /1526 well plates.

        :param Algorithm: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param verbose: Output in console
        :param save: save the result into self.SpatNormData, default = False
        :param max_iterations: maximum iterations loop, default = 100
        """

        try:
            if self.Data is None:
                raise ValueError(
                    "\033[0;31m[ERROR]\033[0m  Compute Median of replicat first by using computeDataFromReplicat")
            elif self.isSpatialNormalized is True:
                raise ValueError(
                    "\033[0;31m[ERROR]\033[0m  SystematicErrorCorrection -> Systematics error have already been removed")
            else:
                if Algorithm == 'Bscore':
                    ge, ce, re, resid, tbl_org = TCA.MedianPolish(self.Data, method=method,
                                                                  max_iterations=max_iterations,
                                                                  verbose=verbose)
                    if save:
                        self.SECData = resid
                        self.isSpatialNormalized = True

                if Algorithm == 'BZscore':
                    ge, ce, re, resid, tbl_org = TCA.BZMedianPolish(self.Data, method=method,
                                                                    max_iterations=max_iterations,
                                                                    verbose=verbose)
                    if save:
                        self.SECData = resid
                        self.isSpatialNormalized = True

                if Algorithm == 'PMP':
                    CorrectedTable = TCA.PartialMeanPolish(self.Data, max_iteration=max_iterations, verbose=verbose)
                    if save:
                        self.SECData = CorrectedTable
                        self.isSpatialNormalized = True

                if Algorithm == 'MEA':
                    CorrectedTable = TCA.MatrixErrorAmendment(self.Data, verbose=verbose)
                    if save:
                        self.SECData = CorrectedTable
                        self.isSpatialNormalized = True

                if Algorithm == 'DiffusionModel':
                    CorrectedTable = TCA.diffusionModel(self.Data, max_iterations=max_iterations, verbose=verbose)
                    if save:
                        self.SECData = CorrectedTable
                        self.isSpatialNormalized = True

        except Exception as e:
            print(e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return ("\n Replicat : " + repr(self.name) +
                    "\n Normalized Data : " + repr(self.isNormalized) +
                    "\n Spatial Normalized : " + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print(e)

    def __str__(self):
        """
        Definition for the print
        """
        try:
            return ("\n Replicat : " + repr(self.name) +
                    "\n Normalized Data : " + repr(self.isNormalized) +
                    "\n Spatial Normalized : " + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print(e)
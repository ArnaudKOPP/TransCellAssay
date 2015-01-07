# coding=utf-8
"""
Replicat implement the notion of technical replicat for one plate
The replicat contains the raw data given in input by the csv, this data are stored into a pandas DataFrame.

Input format MUST BE like that :

WELL   X    X     X     X
A1
A1
A1
...
B2
B2

"""

import pandas as pd
import numpy as np
import TransCellAssay as TCA

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

DEBUG = 1


class Replicat(object):
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
    self.skip_well = None # list of well to skip in control computation, stored in this form ((1, 1), (5, 16))
    """

    def __init__(self, name=None, data=None, single=True, skip=None):
        """
        Constructor
        """
        self.RawData = None
        self.isNormalized = False
        self.isSpatialNormalized = False
        self.DataType = "median"
        self.Data = None
        self.SECData = None

        if data is not None:
            if not single:
                self.set_data_overide(data)
            else:
                self.set_raw_data(data)

        if name is not None:
            self.name = name
        else:
            self.name = None

        self.skip_well = skip

    def set_raw_data(self, input_file):
        """
        Set data in replicat
        :param input_file: csv file
        """
        try:
            self.RawData = pd.read_csv(input_file)
            if DEBUG:
                print('\033[0;32m[INFO]\033[0m Reading %s File' % input_file)
        except:
            try:
                self.RawData = pd.read_csv(input, decimal=",", sep=";")
                if DEBUG:
                    print('\033[0;32m[INFO]\033[0m Reading %s File' % input_file)
            except Exception as e:
                print('\033[0;31m[ERROR]\033[0m  Error in reading %s File' % input_file, e)

    def get_raw_data(self):
        """
        Get all Data from dataframe
        :return: return DataFrame with all data
        """
        try:
            return self.RawData
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_feature_list(self):
        """
        Get all features/component in list
        :return: list of feature/component
        """
        try:
            return self.RawData.columns.tolist()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def set_data_overide(self, array, array_type='median'):
        """
        Set attribut data matrix into self.Data
        This method is designed for 1Data/Well or for manual analysis
        :param array: numpy array with good shape
        :param array_type: median or mean data
        """
        try:
            if isinstance(array, np.ndarray):
                self.Data = array
                if array_type == 'median':
                    print("\033[0;33m[WARNING]\033[0m Manual overide")
                    self.DataType = array_type
                elif array_type == 'mean':
                    print("\033[0;33m[WARNING]\033[0m Manual overide")
                    self.DataType = array_type
                else:
                    raise AttributeError("\033[0;31m[ERROR]\033[0m Must provided data type")
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must provided numpy ndarray")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def set_rep_name(self, info):
        """
        set name for the replicat
        :param info: info on replicat
        :return:
        """
        try:
            self.name = info
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_rep_name(self):
        """
        return name from replicat
        :return: info
        """
        try:
            return self.name
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def set_skip_well(self, to_skip):
        """
        Set the well to skip in neg or pos control
        :param to_skip: list of well to skip (1,3) or B3
        """
        try:
            well_list = list()
            for elem in to_skip:
                if isinstance(elem, tuple):
                    well_list.append(elem)
                elif isinstance(elem, str):
                    well_list.append(TCA.get_opposite_well_format(elem))
                else:
                    pass
            self.skip_well = well_list
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_skip_well(self):
        """
        Set the well to skip in neg or pos control
        """
        try:
            return self.skip_well
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_raw_data_by_well(self, well, feature=None):
        """
        Get all data for well
        :param well: get well position like A1
        :param feature: can have data for specified feature
        :return: dataframe with data for specified well
        """
        try:
            if feature is None:
                return self.RawData[self.RawData['Well'] == well]
            else:
                return self.RawData[feature][self.RawData['Well'] == well]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_raw_data_by_wells(self, wells, feature=None):
        """
        get all data for specified wellS
        :param wells: list of wells
        :param feature: can have data for specified feature or not
        :return: return dataframe with data specified wells
        """
        try:
            data = None
            datagp = self.RawData.groupby("Well")
            check_well = self.RawData.Well.unique()
            gen = (i for i in wells if i in check_well)
            for i in gen:
                if feature is None:
                    if data is None:
                        data = datagp.get_group(i)
                    data = data.append(datagp.get_group(i))
                else:
                    if data is None:
                        data = datagp.get_group(i)[feature]
                    data = data.append(datagp.get_group(i)[feature])
            return data
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_raw_data_by_feature(self, featlist, well_idx=False):
        """
        Return a data frame with Well col and features data col in list []
        if no Well col is given, then auto add
        :param featlist: give a list with feature in [] format
        :param well_idx: if we want to have Well col in data
        :return: output a dataframe with Well col and feature col
        """
        try:
            if well_idx:
                featlist.insert(0, 'Well')
                return self.RawData[featlist]
            else:
                return self.RawData[featlist]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def compute_data_for_feature(self, feature):
        """
        Compute data in matrix form, get mean or median for well and save them in replicat object
        :param feature: which feature to keep in matrix
        :return:
        """
        try:
            if not self.isNormalized:
                print('!!! \033[0;33m[WARNING]\033[0m   !!!')
                print('     --> Data are not normalized for replicat : ', self.name)
                print('')

            grouped_data_by_well = self.RawData.groupby('Well')
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
                pos = TCA.Utils.WellFormat.get_opposite_well_format(key)
                self.Data[pos[0]][pos[1]] = elem

        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_data_array(self, feature, sec=False):
        """
        Return data in matrix form, get mean or median for well
        :param feature: which feature to keep in matrix
        :param sec: want Systematic Error Corrected data ? default=False
        :return: compute data in matrix form
        """
        try:
            if sec:
                if self.SECData is None:
                    raise ValueError('\033[0;31m[ERROR]\033[0m  Launch Systematic Error Correction before')
                else:
                    return self.SECData
            elif self.Data is None:
                self.compute_data_for_feature(feature)
            return self.Data

        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def normalization(self, feature, method='Zscore', log=True, neg=None, pos=None):
        """
        Performed normalization on data
        :param feature; which feature to normalize
        :param method: Performed X Transformation
        :param log:  Performed log2 Transformation
        :param pos: postive control
        :param neg: negative control
        """
        try:
            if not self.isNormalized:
                self.RawData = TCA.variability_normalization(self.RawData, feature=feature, method=method,
                                                             log2_transf=log, neg_control=neg, pos_control=pos)
                self.isNormalized = True
            else:
                raise Exception("\033[0;33m[WARNING]\033[0m Data are already normalized")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def systematic_error_correction(self, algorithm='Bscore', method='median', verbose=False, save=False,
                                    max_iterations=100, alpha=0.05):
        """

        Apply a spatial normalization for remove edge effect
        The Bscore method showed a more stable behavior than MEA and PMP only when the number of rows and columns
        affected by the systematics error, hit percentage and systematic error variance were high (mainly du to a
        mediocre performance of the t-test in this case). MEA was generally the best method for correcting
        systematic error within 96-well plates, whereas PMP performed better for 384 /1526 well plates.

        :param algorithm: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param method: median or mean data
        :param verbose: Output in console
        :param save: save the result into self.SECData, default = False
        :param max_iterations: maximum iterations loop, default = 100
        """

        try:
            if self.Data is None:
                raise ValueError("\033[0;31m[ERROR]\033[0m Compute Median of replicat first by using "
                                 "computeDataFromReplicat")
            elif self.isSpatialNormalized is True:
                raise ValueError("\033[0;31m[ERROR]\033[0m systematic_error_correction -> Systematics error have "
                                 "already been removed")
            else:
                if algorithm == 'Bscore':
                    ge, ce, re, resid, tbl_org = TCA.median_polish(self.Data, method=method,
                                                                   max_iterations=max_iterations,
                                                                   verbose=verbose)
                    if save:
                        self.SECData = resid
                        self.isSpatialNormalized = True

                if algorithm == 'BZscore':
                    ge, ce, re, resid, tbl_org = TCA.bz_median_polish(self.Data, method=method,
                                                                      max_iterations=max_iterations,
                                                                      verbose=verbose)
                    if save:
                        self.SECData = resid
                        self.isSpatialNormalized = True

                if algorithm == 'PMP':
                    corrected_data_array = TCA.partial_mean_polish(self.Data, max_iteration=max_iterations,
                                                                   verbose=verbose, alpha=alpha)
                    if save:
                        self.SECData = corrected_data_array
                        self.isSpatialNormalized = True

                if algorithm == 'MEA':
                    corrected_data_array = TCA.matrix_error_amendmend(self.Data, verbose=verbose, alpha=alpha)
                    if save:
                        self.SECData = corrected_data_array
                        self.isSpatialNormalized = True

                if algorithm == 'DiffusionModel':
                    corrected_data_array = TCA.diffusion_model(self.Data, max_iterations=max_iterations,
                                                               verbose=verbose)
                    if save:
                        self.SECData = corrected_data_array
                        self.isSpatialNormalized = True

        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    @staticmethod
    def write_pickle(path):
        """
        Write pickle object
        :param path: where to save
        """
        try:
            print(path)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    @staticmethod
    def load_pickle(path):
        """
        read pickle object
        :param path: where to read
        """
        try:
            print(path)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def save_raw_data(self, path):
        """
        Save normalized Raw data
        :param path: Where to write .csv file
        """
        try:
            self.RawData.to_csv(path=path)
        except Exception as e:
            print(e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return ("\n Replicat : " + repr(self.name) +
                    "\n Raw Data head : " + repr(self.RawData.head()) +
                    "\n Data normalized ? : " + repr(self.isNormalized) +
                    "\n Data systematic error removed ? : " + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        """
        try:
            return ("\n Replicat : " + repr(self.name) +
                    "\n Raw Data head : " + repr(self.RawData.head()) +
                    "\n Data normalized ? : " + repr(self.isNormalized) +
                    "\n Data systematic error removed ? : " + repr(self.isSpatialNormalized) + "\n")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

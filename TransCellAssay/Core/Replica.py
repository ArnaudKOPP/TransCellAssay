# coding=utf-8
"""
Replicat implement the notion of technical replicat for plate
"""

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


class Replica(object):
    """
    classdocs
    Class for manipuling replicat of plate
    self.rawdata = rawdata  # data frame that contains data
    self.name = ""  # Name of replicat
    self.isNormalized = False  # are the data normalized
    self.isSpatialNormalized = False  # systematics error removed or not
    self.datatype = "median" # median or mean of data
    self.array = None  # matrix that contain mean of interested channels to analyze
    self._array_channel = None, which channel is stored in data
    self.sec_array = None  # matrix that contain data corrected
    self.skip_well = () # list of well to skip in control computation, stored in this form ((1, 1), (5, 16))
    """

    def __init__(self, name=None, data=None, single=True, skip=(), datatype='median'):
        """
        Constructor
        """
        self.rawdata = None
        self.isNormalized = False
        self.isSpatialNormalized = False
        self.datatype = datatype
        self._array_channel = None
        self.array = None
        self.sec_array = None

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
        self._is_cutted = False
        self._rb = None
        self._re = None
        self._cb = None
        self._ce = None

    def set_raw_data(self, input_file):
        """
        Set data in replicat
        :param input_file: csv file
        """
        self.rawdata = TCA.RawData(input_file)

    def get_channel_list(self):
        """
        Get all channels/component in list
        :return: list of channel/component
        """
        return self.rawdata.get_channel_list

    def set_data_overide(self, array, array_type='median'):
        """
        Set attribut data matrix into self.Data
        This method is designed for 1Data/Well or for manual analysis
        :param array: numpy array with good shape
        :param array_type: median or mean data
        """
        __valide_datatype = ['median', 'mean']
        if isinstance(array, np.ndarray):
            if array_type not in __valide_datatype:
                raise ValueError("Must provided data type, possibilities : {}".format(__valide_datatype))
            print("\033[0;33m[WARNING]\033[0m Manual overide")
            self.array = array
            if array_type == 'median':
                self.datatype = array_type
            else:
                self.datatype = array_type
        else:
            raise AttributeError("Must provided numpy ndarray")

    def set_name(self, info):
        """
        set name for the replicat
        :param info: info on replicat
        :return:
        """
        self.name = info

    def get_name(self):
        """
        return name from replicat
        :return: info
        """
        return self.name

    def set_skip_well(self, to_skip):
        """
        Set the well to skip in neg or pos control
        :param to_skip: list of well to skip (1,3) or B3
        """
        well_list = list()
        for elem in to_skip:
            if isinstance(elem, tuple):
                well_list.append(elem)
            elif isinstance(elem, str):
                well_list.append(TCA.get_opposite_well_format(elem))
            else:
                pass
        self.skip_well = well_list

    def get_skip_well(self):
        """
        Set the well to skip in neg or pos control
        """
        return self.skip_well

    def get_valid_well(self, to_check):
        """
        :type to_check: list to check if all well are not to skip
        """
        if len(self.skip_well) < 1:
            return to_check
        if len(to_check) > 0:
            # type check
            elem = to_check[0]
            if isinstance(elem, tuple):
                tmp = [x for x in to_check if x not in self.skip_well]
                return tmp
            if isinstance(elem, str):
                tmp = [x for x in to_check if TCA.get_opposite_well_format(x) not in self.skip_well]
                return tmp
        else:
            raise ValueError('Empty List')

    def get_raw_data(self, channel=None, well=None, well_idx=False):
        """
        Get Raw data with specified param
        :param channel: defined or not channel
        :param well: defined or not which well you want, in list [] or simple string format
        :param well_idx: add or not well id
        :return: raw data in pandas dataframe
        """
        return self.rawdata.get_raw_data(channel=channel, well=well, well_idx=well_idx)

    def compute_data_for_channel(self, channel):
        """
        Compute data in matrix form, get mean or median for well and save them in replicat object
        :param channel: which channel to keep in matrix
        :return:
        """
        if self.array is not None:
            if self._array_channel is not channel:
                print('\033[0;33m[WARNING]\033[0m Overwriting previous channel data from {} to {}'.format(
                    self._array_channel, channel))
        if not self.isNormalized:
            print('\033[0;33m[WARNING]\033[0m Data are not normalized for replicat : ', self.name)

        if self.datatype == 'median':
            self.array = self.rawdata.compute_matrix(channel=channel, type_mean=self.datatype)
            self._array_channel = channel
        else:
            self.array = self.rawdata.compute_matrix(channel=channel, type_mean=self.datatype)
            self._array_channel = channel

    def get_data_array(self, channel, sec=False):
        """
        Return data in matrix form, get mean or median for well
        :param channel: which channel to keep in matrix
        :param sec: want Systematic Error Corrected data ? default=False
        :return: compute data in matrix form
        """
        if sec:
            if self.sec_array is None:
                raise ValueError('Launch Systematic Error Correction before')
            else:
                return self.sec_array
        if self.array is None:
            self.compute_data_for_channel(channel)
        if channel is self._array_channel:
            return self.array
        else:
            self.compute_data_for_channel(channel)
            return self.array

    def cut(self, rb, re, cb, ce):
        """
        Cut the replicat to 'zoom' into a defined zone, for avoiding crappy effect during SEC process
        :param rb: row begin
        :param re: row end
        :param cb: col begin
        :param ce: col end
        """
        if self._is_cutted:
            raise AttributeError('Already cutted')
        if self.array is not None:
            self.array = self.array[rb: re, cb: ce]
        if self.sec_array is not None:
            self.sec_array = self.sec_array[rb: re, cb: ce]
        self._is_cutted = True
        self._rb = rb
        self._re = re
        self._cb = cb
        self._ce = ce

    def __normalization(self, channel, method='Zscore', log=True, neg=None, pos=None, skipping_wells=False):
        """
        Performed normalization on data
        :param channel; which channel to normalize
        :param method: Performed X Transformation
        :param log:  Performed log2 Transformation
        :param pos: postive control
        :param neg: negative control
        :param skipping_wells: skip defined wells, use it with poc and npi
        """
        if not self.isNormalized:
            if skipping_wells:
                self.rawdata = TCA.rawdata_variability_normalization(self.rawdata, channel=channel,
                                                                     method=method, log2_transf=log,
                                                                     neg_control=[x for x in neg if (
                                                                         TCA.get_opposite_well_format(
                                                                             x) not in self.skip_well)],
                                                                     pos_control=[x for x in pos if (
                                                                         TCA.get_opposite_well_format(
                                                                             x) not in self.skip_well)])
            else:
                self.rawdata = TCA.rawdata_variability_normalization(self.rawdata, channel=channel,
                                                                     method=method,
                                                                     log2_transf=log,
                                                                     neg_control=neg,
                                                                     pos_control=pos)
            self.isNormalized = True
            self.compute_data_for_channel(channel)
            print(
                '\033[0;32m[INFO]\033[0m Raw Data normalization processing for replicat {} on channel {}'.format(
                    self.name, channel))
        else:
            print("\033[0;33m[WARNING]\033[0m Data are already normalized, do nothing")

    def normalization_channels(self, channels, method='Zscore', log=True, neg=None, pos=None, skipping_wells=False):
        """
        Apply a normalization method to multiple
        :param pos: positive control
        :param neg: negative control
        :param channels: channel to normalize
        :param method: which method to perform
        :param log:  Performed log2 Transformation
        :param skipping_wells: skip defined wells, use it with poc and npi
        """
        if isinstance(channels, str):
            self.__normalization(channel=channels, method=method, log=log, neg=neg, pos=pos,
                                 skipping_wells=skipping_wells)
        elif isinstance(channels, list):
            for chan in channels:
                self.__normalization(channel=chan, method=method, log=log, neg=neg, pos=pos,
                                     skipping_wells=skipping_wells)
                self.isNormalized = True
            print("\033[0;33m[WARNING]\033[0m Choose your channels that you want to work with plate.compute_data_"
                  "from_replicat or replica.compute_data_for_channel")

    def systematic_error_correction(self, algorithm='Bscore', method='median', verbose=False, save=True,
                                    max_iterations=100, alpha=0.05, epsilon=0.01, skip_col=None, skip_row=None):
        """
        Apply a spatial normalization for remove edge effect
        The Bscore method showed a more stable behavior than MEA and PMP only when the number of rows and columns
        affected by the systematics error, hit percentage and systematic error variance were high (mainly du to a
        mediocre performance of the t-test in this case). MEA was generally the best method for correcting
        systematic error within 96-well plates, whereas PMP performed better for 384 /1526 well plates.

        :param alpha: alpha for some algorithme
        :param algorithm: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param method: median or mean data
        :param verbose: Output in console
        :param save: save the result into self.SECData, default = False
        :param max_iterations: maximum iterations loop, default = 100
        :param epsilon: epsilon parameters for PMP
        :param skip_col: index of col to skip in MEA or PMP
        :param skip_row: index of row to skip in MEA or PMP
        """
        __valid_sec_algo = ['Bscore', 'BZscore', 'PMP', 'MEA', 'DiffusionModel']

        if algorithm not in __valid_sec_algo:
            raise ValueError('Algorithm is not good choose : {}'.format(__valid_sec_algo))

        if self.array is None:
            raise ValueError("Use first : compute_data_for_channel")

        else:
            if self.isSpatialNormalized:
                print('\033[0;33m[WARNING]\033[0m SEC already performed -> overwriting previous sec data')

            print('\033[0;32m[INFO]\033[0m Systematic Error Correction processing : {} -> replica {}'.
                  format(algorithm, self.name))

            if algorithm == 'Bscore':
                ge, ce, re, resid, tbl_org = TCA.median_polish(self.array.copy(), method=method,
                                                               max_iterations=max_iterations,
                                                               verbose=verbose)
                if save:
                    self.sec_array = resid
                    self.isSpatialNormalized = True

            if algorithm == 'BZscore':
                ge, ce, re, resid, tbl_org = TCA.bz_median_polish(self.array.copy(), method=method,
                                                                  max_iterations=max_iterations,
                                                                  verbose=verbose)
                if save:
                    self.sec_array = resid
                    self.isSpatialNormalized = True

            if algorithm == 'PMP':
                corrected_data_array = TCA.partial_mean_polish(self.array.copy(), max_iteration=max_iterations,
                                                               verbose=verbose, alpha=alpha, epsilon=epsilon,
                                                               skip_col=skip_col, skip_row=skip_row)
                if save:
                    self.sec_array = corrected_data_array
                    self.isSpatialNormalized = True

            if algorithm == 'MEA':
                corrected_data_array = TCA.matrix_error_amendmend(self.array.copy(), verbose=verbose, alpha=alpha,
                                                                  skip_col=skip_col, skip_row=skip_row)
                if save:
                    self.sec_array = corrected_data_array
                    self.isSpatialNormalized = True

            if algorithm == 'DiffusionModel':
                corrected_data_array = TCA.diffusion_model(self.array.copy(), max_iterations=max_iterations,
                                                           verbose=verbose)
                if save:
                    self.sec_array = corrected_data_array
                    self.isSpatialNormalized = True

    def save_raw_data(self, path, name=None):
        """
        Save normalized Raw data
        :param name: Give name to file
        :param path: Where to write .csv file
        """
        if name is None:
            name = self.name+".csv"
        self.rawdata.save_raw_data(path=path, name=name)

    def save_memory(self, only_cache=True):
        """
        Save memory by deleting Raw Data that use a lot of memory
        :param only_cache: Remove only cache or all
        """
        self.rawdata.save_memory(only_cache=only_cache)
        if DEBUG:
            print('\033[0;32m[INFO]\033[0m Saving memory')

    def __repr__(self):
        """
        Definition for the representation
        """
        return ("\n Replicat : " + repr(self.name) +
                repr(self.rawdata) +
                "\n Data normalized ? : " + repr(self.isNormalized) +
                "\n Data systematic error removed ? : " + repr(self.isSpatialNormalized) + "\n")

    def __str__(self):
        """
        Definition for the print
        """
        return self.__repr__()
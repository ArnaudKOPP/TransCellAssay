# coding=utf-8
"""
Plate is designed for manipulating one or more replicat
"""

import numpy as np
import TransCellAssay as TCA
import os
import collections


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class Plate(object):
    """
    classdocs
    Class for manipuling plate and their replicat :

    self.replica = {}  # Dict that contain all replicat, key are name and value are replicat object
    self.name = None  # Name of Plate
    self.platemap = ScreenPlateReplicatPS.PlateMap()  # Plate Setup object
    self.threshold = None  # Threeshold for considering Cell as positive
    self._control_position = ((0, 11), (0, 23))  # column where control is positionned in plate (default pos)
    self._neg = None  # Name of negative control
    self._pos = None  # Name of positive control
    self._tox = None  # Name of toxics control
    self.isNormalized = False  # Are replicat data normalized
    self.isSpatialNormalized = False  # Systematic error removed from plate data ( resulting from replicat )
    self.datatype = "median" # median or mean data, default is median
    self.array = None  # matrix that contain data from replicat of interested channel to analyze
    self._array_channel = None, which channel is stored in data
    self.sec_array = None  # matrix that contain data corrected or from replicat data
    self.skip_well = None # list of well to skip in control computation, stored in this form ((1, 1), (5, 16))
    """

    def __init__(self, name=None, platemap=None, skip=()):
        """
        Constructor
        """
        self.replica = collections.OrderedDict()
        self._meta_info = {}
        self.name = name

        self.platemap = TCA.Core.PlateMap()
        if platemap is not None:
            self.platemap = platemap
        self.threshold = None
        self._control_position = ((0, 11), (0, 23))

        self._neg = None
        self._pos = None
        self._tox = None

        self.isNormalized = False
        self.isSpatialNormalized = False

        self.datatype = "median"
        self.array = None
        self.sec_array = None

        self.skip_well = skip

    def print_meta_info(self):
        """
        Print all data contains in MetaInfo for Plate object
        :return: print some output
        """
        try:
            for keys, values in self._meta_info.items():
                print(keys, values)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def set_plate_name(self, name):
        """
        Set Name for plate
        :param name:
        """
        try:
            self.name = name
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_plate_name(self):
        """
        Get Name of plate
        :return: Name of plate
        """
        try:
            return self.name
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def set_data(self, array, array_type):
        """
        Set attribut data matrix into self.Data
        This method is designed for 1Data/Well or for manual analysis
        :param array: numpy array with good shape
        :param array_type: median or mean data
        """
        try:
            if isinstance(array, np.ndarray):
                print()
                self.array = array
                if array_type == 'median':
                    self.datatype = array_type
                elif array_type == 'mean':
                    self.datatype = array_type
                else:
                    raise AttributeError("\033[0;31m[ERROR]\033[0m Must provided data type")
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must provied numpy ndarray")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def add_replicat(self, replicat):
        """
        Add replicat object to plate
        :param replicat: Give a replicat object
        """
        try:
            assert isinstance(replicat, TCA.Core.Replica)
            name = replicat.name
            self.replica[name] = replicat
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_replicat(self, name):
        """
        Get the replicat specified by name
        :param name: string : key of replicat in dict
        :return: Replicat object
        """
        try:
            return self.replica[name]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_all_replicat(self):
        """
        Get all replicat from plate
        :return: dict of replicat
        """
        try:
            return self.replica
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
        get the well to skip in neg or pos control
        """
        try:
            return self.skip_well
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def check_data_consistency(self, remove=False):
        """
        Check if all replicat have same well
        :param remove: remove or not replicat with data error
        :return: 0 if error, 1 if data good
        """
        try:
            from itertools import chain

            # Collect the input lists for use with chain below
            all_lists = []
            name = []
            for key, value in self.replica.items():
                all_lists.append(list(value.rawdata.get_unique_well()))
                name.append(key)

            for A, B in zip(all_lists, name):
                # Combine all the lists into one
                super_list = list(chain(*all_lists))
                # Get the unique items remaining in the combined list
                super_set = set(super_list)
                # Compute the unique items in this list and print them
                uniques = super_set - set(A)
                if len(uniques) > 0:
                    print("\033[0;33m !!!!! [WARNING] !!!!! \033[0m")
                    print("Missing Well in Raw Data replicat ", B, " : ", sorted(uniques))
                    print("Missing Value can insert ERROR in further Analyzis")
                    if remove:
                        del self.replica[B]
                        print(B, "Will be removed ---->")
                    else:
                        print("----> Can be removed with appropriate parameters : remove True or False")
                    return 0

            return 1
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def add_info(self, key, value):
        """
        Add Info into the dict
        :param key: key of info
        :param value: text for info
        """
        try:
            self._meta_info.pop(key, value)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_info(self, key):
        """
        Get desired info with key
        :param key: key of info
        :return: info value from key
        """
        try:
            return self._meta_info[key]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m ", e)

    def get_raw_data(self, replicat=None, channel=None, well=None, well_idx=False):
        """
        Return a dict that contain raw data from all replica (or specified replicat), we can specified channel (list)
        and if we want to have well id
        :param replicat: replicat id
        :param channel: channel list
        :param well: defined or not which well you want, in list [] or simple string format
        :param well_idx: true or false for keeping well id (A1..)
        :return: dict with data
        """
        data = {}
        try:
            if replicat is not None:
                for key, value in self.replica.items():
                    data[value.get_rep_name()] = value.get_raw_data(channel=channel, well=well, well_idx=well_idx)
            else:
                for rep in replicat:
                    data[self.replica[rep].get_rep_name()] = rep.get_raw_data(channel=channel, well=well,
                                                                               well_idx=well_idx)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def add_platemap(self, platemap):
        """
        Add the platemap to the plate
        :param platemap:
        """
        try:
            assert isinstance(platemap, TCA.Core.PlateMap)
            self.platemap = platemap
        except Exception as e:
            print(e)

    def get_platemap(self):
        """
        Get the platemap from the plate
        :return: platemap
        """
        try:
            return self.platemap
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def compute_all_channels_from_replicat(self):
        """
        compute all component mean from all replicat for each well
        :return: dataframe
        """
        try:
            df = None
            for key, rep in self.replica.items():
                assert isinstance(rep, TCA.Replica)
                tmp = rep.rawdata.get_groupby_data()
                if df is None:
                    df = tmp.median()
                else:
                    df += tmp.median()
            return df / len(self.replica)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def compute_data_from_replicat(self, channel, use_sec_data=False, forced_update=False):
        """
        Compute the mean/median matrix data of all replicat
        If replicat data is SpatialNorm already, this function will fill spatDataMatrix
        :param forced_update: Forced redetermination of replicat data, to use when you have determine matrix too soon
        :param use_sec_data: use or not sec data from replicat
        :param channel: which channel to have into sum up data
        """
        try:
            tmp_array = np.zeros(self.platemap.platemap.shape)
            i = 0

            for key, replicat in self.replica.items():
                i += 1
                if self.array is None:
                    replicat.compute_data_for_channel(channel)
                if forced_update:
                    replicat.compute_data_for_channel(channel)

                if not use_sec_data:
                    tmp_array = tmp_array + replicat.array
                else:
                    tmp_array = tmp_array + replicat.sec_array

            if not use_sec_data:
                self.array = tmp_array / i
            else:
                self.sec_array = tmp_array / i
                self.isSpatialNormalized = True
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def normalization(self, channel, method='Zscore', log=True, neg=None, pos=None, skipping_wells=False):
        """
        Apply Well correction on all replicat data
        call function like from replicat object
        :param pos: positive control
        :param neg: negative control
        :param channel: channel to normalize
        :param method: which method to perform
        :param log:  Performed log2 Transformation
        :param skipping_wells: skip defined wells, use it with poc and npi
        """
        try:
            for key, value in self.replica.items():
                value.normalization(channel=channel, method=method, log=log, neg=neg, pos=pos,
                                    skipping_wells=skipping_wells)
            self.isNormalized = True
            self.compute_data_from_replicat(channel, forced_update=True)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def normalization_channels(self, channels, method='Zscore', log=True, neg=None, pos=None, skipping_wells=False):
        """
        Apply multi channels normalization
        :param pos: positive control
        :param neg: negative control
        :param channels: channel to normalize
        :param method: which method to perform
        :param log:  Performed log2 Transformation
        :param skipping_wells: skip defined wells, use it with poc and npi
        """
        if isinstance(channels, list):
            try:
                for key, value in self.replica.items():
                    value.normalization_channels(channels=channels, method=method, log=log, neg=neg, pos=pos,
                                                 skipping_wells=skipping_wells)
                self.isNormalized = True
            except Exception as e:
                print("\033[0;31m[ERROR]\033[0m", e)
        else:
            self.normalization(channels, method, log, neg, pos, skipping_wells)

    def systematic_error_correction(self, algorithm='Bscore', method='median', apply_down=False, verbose=False,
                                    save=False, max_iterations=100, alpha=0.05):
        """
        Apply a spatial normalization for remove edge effect
        Resulting matrix are save in plate object if save = True
        Be careful !! if the replicat data was already be spatial norm, it will degrade data !!
        :param algorithm: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param method: for bscore : use median or average method
        :param apply_down: apply strategie to replicat, if true apply SEC on replicat !! not re-use function on plate
        :param verbose: verbose : output the result ?
        :param save: save: save the residual into self.SECData , default = False
        :param max_iterations: max iterations for all technics
        :param alpha: alpha for TTest
        """
        try:
            if apply_down:
                for key, value in self.replica.items():
                    value.systematic_error_correction(algorithm=algorithm, method=method, verbose=verbose, save=save,
                                                      max_iterations=max_iterations, alpha=alpha)
                    self.compute_data_from_replicat(channel=None, use_sec_data=True)
                return

            if self.array is None:
                raise ValueError(
                    "\033[0;31m[ERROR]\033[0m Compute Median of replicat first by using computeDataFromReplicat")
            else:
                if self.isSpatialNormalized:
                    print('\033[0;33m[WARNING]\033[0m SEC already performed -> overwriting previous sec data')
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
                                                                   alpha=alpha, verbose=verbose)
                    if save:
                        self.sec_array = corrected_data_array
                        self.isSpatialNormalized = True

                if algorithm == 'MEA':
                    corrected_data_array = TCA.matrix_error_amendmend(self.array.copy(), verbose=verbose, alpha=alpha)
                    if save:
                        self.sec_array = corrected_data_array
                        self.isSpatialNormalized = True

                if algorithm == 'DiffusionModel':
                    corrected_data_array = TCA.diffusion_model(self.array.copy(), max_iterations=max_iterations,
                                                               verbose=verbose)
                    if save:
                        self.sec_array = corrected_data_array
                        self.isSpatialNormalized = True

        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def save_raw_data(self, path):
        """
        Save normalized raw data
        :param path: path where to save raw data
        """
        try:
            if not os.path.isdir(path):
                os.mkdir(path)
            for key, value in self.replica.items():
                value.save_raw_data(path)
        except Exception as e:
            print(e)

    def save_memory(self, only_cache=True):
        """
        Save memory by deleting Raw Data
        :param only_cache: Remove only cache
        """
        try:
            for key, value in self.replica.items():
                value.save_memory(only_cache=only_cache)
        except Exception as e:
            print(e)

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

    def __sub__(self, to_rm):
        """
        Remove replicat from plate, use - operator
        :param to_rm:
        """
        try:
            del self.replica[to_rm]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __add__(self, to_add):
        """
        Add replicat to plate, use + operator
        :param to_add:
        """
        try:
            if isinstance(to_add, TCA.Core.Replica):
                name = to_add.name
                self.replica[name] = to_add
            elif isinstance(to_add, TCA.Core.PlateMap):
                self.platemap = to_add
            elif isinstance(to_add, list):
                for elem in to_add:
                    assert isinstance(elem, TCA.Core.Replica)
                    self.replica[elem.name] = elem
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Unsupported Type")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __getitem__(self, key):
        """
        Return replicat object, use [] operator
        :param key:
        :return: return replicat
        """
        try:
            return self.replica[key]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __setitem__(self, key, value):
        """
        Set replicat objet, use [] operator
        :param key: name of replicat
        :param value: replicat object
        """
        try:
            if not isinstance(value, TCA.Replica):
                raise AttributeError("\033[0;31m[ERROR]\033[0m Unsupported Type")
            else:
                self.replica[key] = value
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __len__(self):
        """
        Get len /number of replicat inside Plate, use len(object)
        :return: number of replicat
        """
        try:
            return len(self.replica)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return (
                "\n Plate : " + repr(self.name) +
                "\n PlateMap : \n" + repr(self.platemap) +
                "\n Data normalized ? " + repr(self.isNormalized) +
                "\n Data systematic error removed ? " + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replica))
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        """
        try:
            return self.__repr__()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

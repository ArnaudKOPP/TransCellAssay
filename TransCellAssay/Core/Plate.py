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
        self._is_cutted = False
        self._rb = None
        self._re = None
        self._cb = None
        self._ce = None

    def set_plate_name(self, name):
        """
        Set Name for plate
        :param name:
        """
        self.name = name

    def get_plate_name(self):
        """
        Get Name of plate
        :return: Name of plate
        """
        return self.name

    def set_data(self, array, array_type):
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
            self.array = array
            if array_type == 'median':
                self.datatype = array_type
            else:
                self.datatype = array_type
        else:
            raise AttributeError("Must provied numpy ndarray")

    def add_replicat(self, replicat):
        """
        Add replicat object to plate
        :param replicat: Give a replicat object
        """
        assert isinstance(replicat, TCA.Core.Replica)
        name = replicat.name
        self.replica[name] = replicat

    def get_replicat(self, name):
        """
        Get the replicat specified by name
        :param name: string : key of replicat in dict
        :return: Replicat object
        """
        return self.replica[name]

    def get_all_replicat(self):
        """
        Get all replicat from plate
        :return: dict of replicat
        """
        return self.replica

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
        get the well to skip in neg or pos control
        """
        return self.skip_well

    def check_data_consistency(self, remove=False):
        """
        Check if all replicat have same well
        :param remove: remove or not replicat with data error
        :return: 0 if error, 1 if data good
        """
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
        if replicat is not None:
            for key, value in self.replica.items():
                data[value.get_rep_name()] = value.get_raw_data(channel=channel, well=well, well_idx=well_idx)
        else:
            for rep in replicat:
                data[self.replica[rep].get_rep_name()] = rep.get_raw_data(channel=channel, well=well,
                                                                          well_idx=well_idx)

    def add_platemap(self, platemap):
        """
        Add the platemap to the plate
        :param platemap:
        """
        assert isinstance(platemap, TCA.Core.PlateMap)
        self.platemap = platemap

    def get_platemap(self):
        """
        Get the platemap from the plate
        :return: platemap
        """
        return self.platemap

    def compute_all_channels_from_replicat(self):
        """
        compute all component mean from all replicat for each well
        :return: dataframe
        """
        df = None
        for key, rep in self.replica.items():
            assert isinstance(rep, TCA.Replica)
            tmp = rep.rawdata.get_groupby_data()
            if df is None:
                df = tmp.median()
            else:
                df += tmp.median()
        return df / len(self.replica)

    def compute_data_from_replicat(self, channel, use_sec_data=False, forced_update=False):
        """
        Compute the mean/median matrix data of all replicat
        If replicat data is SpatialNorm already, this function will fill spatDataMatrix
        :param forced_update: Forced redetermination of replicat data, to use when you have determine matrix too soon
        :param use_sec_data: use or not sec data from replicat
        :param channel: which channel to have into sum up data
        """
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

    def cut(self, rb, re, cb, ce, apply_down=True):
        """
        Cut a plate and replicat to 'zoom' into a defined zone, for avoiding crappy effect during SEC process
        :param rb: row begin
        :param re: row end
        :param cb: col begin
        :param ce: col end
        :param apply_down: apply the cutting to replica
        """
        if self._is_cutted:
            raise AttributeError('Already cutted')
        print("\033[0;33m[WARNING]\033[0m Cutting operation cannot be reverted, so plate Analysis and "
              "some other function may not be functionnal anymore")
        if self.array is not None:
            self.array = self.array[rb: re, cb: ce]
        else:
            raise AttributeError('array is empty')
        if self.sec_array is not None:
            self.sec_array = None
            print('\033[0;33m[WARNING]\033[0m Must reperforme SEC process')
        if apply_down:
            for key, value in self.replica.items():
                value.cut(rb, re, cb, ce)
        self.platemap.cut(rb, re, cb, ce)
        self._is_cutted = True
        self._rb = rb
        self._re = re
        self._cb = cb
        self._ce = ce

    def __normalization(self, channel, method='Zscore', log=True, neg=None, pos=None, skipping_wells=False):
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
        for key, value in self.replica.items():
            value.normalization_channels(channels=channel, method=method, log=log, neg=neg, pos=pos,
                                         skipping_wells=skipping_wells)
        self.isNormalized = True
        self.compute_data_from_replicat(channel, forced_update=True)

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
            self.__normalization(channels, method, log, neg, pos, skipping_wells)

    def systematic_error_correction(self, algorithm='Bscore', method='median', apply_down=True, verbose=False,
                                    save=True, max_iterations=100, alpha=0.05, epsilon=0.01, skip_col=None,
                                    skip_row=None):
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
        :param epsilon: epsilon parameters for PMP
        :param skip_col: index of col to skip in MEA or PMP
        :param skip_row: index of row to skip in MEA or PMP
        """
        __valid_sec_algo = ['Bscore', 'BZscore', 'PMP', 'MEA', 'DiffusionModel']

        if algorithm not in __valid_sec_algo:
            raise ValueError('Algorithm is not good choose : {}'.format(__valid_sec_algo))

        if apply_down:
            for key, value in self.replica.items():
                value.systematic_error_correction(algorithm=algorithm, method=method, verbose=verbose, save=save,
                                                  max_iterations=max_iterations, alpha=alpha, epsilon=epsilon)
            self.compute_data_from_replicat(channel=None, use_sec_data=True)
            return

        if self.array is None:
            raise ValueError("Use first : compute_data_from_replicat")
        else:
            if self.isSpatialNormalized:
                print('\033[0;33m[WARNING]\033[0m SEC already performed -> overwriting previous sec data')
            print('\033[0;32m[INFO]\033[0m Systematic Error Correction processing : {}'.format(algorithm))
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
                                                               alpha=alpha, verbose=verbose, epsilon=epsilon,
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

    def save_raw_data(self, path):
        """
        Save normalized raw data
        :param path: path where to save raw data
        """
        if not os.path.isdir(path):
            os.mkdir(path)
        for key, value in self.replica.items():
            value.save_raw_data(path)

    def save_memory(self, only_cache=True):
        """
        Save memory by deleting Raw Data
        :param only_cache: Remove only cache
        """
        for key, value in self.replica.items():
            value.save_memory(only_cache=only_cache)

    def __sub__(self, id_rep):
        """
        Remove replicat from plate, use - operator
        :param id_rep: replica id to remove from plate
        """
        del self.replica[id_rep]

    def __add__(self, id_rep):
        """
        Add replicat to plate, use + operator
        :param id_rep: replica id that is added
        """
        if isinstance(id_rep, TCA.Core.Replica):
            name = id_rep.name
            self.replica[name] = id_rep
        elif isinstance(id_rep, TCA.Core.PlateMap):
            self.platemap = id_rep
        elif isinstance(id_rep, list):
            for elem in id_rep:
                assert isinstance(elem, TCA.Core.Replica)
                self.replica[elem.name] = elem
        else:
            raise AttributeError("Unsupported Type")

    def __getitem__(self, key):
        """
        Return replicat object, use [] operator
        :param key:
        :return: return replicat
        """
        return self.replica[key]

    def __setitem__(self, key, value):
        """
        Set replicat objet, use [] operator
        :param key: name of replicat
        :param value: replicat object
        """
        if not isinstance(value, TCA.Replica):
            raise AttributeError("Unsupported Type")
        else:
            self.replica[key] = value

    def __len__(self):
        """
        Get len /number of replicat inside Plate, use len(object)
        :return: number of replicat
        """
        return len(self.replica)

    def __repr__(self):
        """
        Definition for the representation
        """
        return (
            "\n Plate : " + repr(self.name) +
            "\n PlateMap : \n" + repr(self.platemap) +
            "\n Data normalized ? " + repr(self.isNormalized) +
            "\n Data systematic error removed ? " + repr(self.isSpatialNormalized) +
            "\n Replicat List : \n" + repr(self.replica))

    def __str__(self):
        """
        Definition for the print
        """
        return self.__repr__()
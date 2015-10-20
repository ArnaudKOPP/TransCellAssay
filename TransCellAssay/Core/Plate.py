# coding=utf-8
"""
Plate is designed for manipulating one or more replica, we store in this class replica object, a platemap object is
attached to this class
"""

import numpy as np
import pandas as pd
import TransCellAssay as TCA
from TransCellAssay.Core.MasterPlate import MasterPlate
import os
import collections
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class Plate(MasterPlate):
    """
    Class for manipulating plate and their replica, get all attribute and method from MasterPlate

    self.replica = {}                 # Dict that contain all replica, key are name and value are replica object
    self.platemap = TCA.Core.PlateMap()  # Plate Setup object
    """

    def __init__(self, name, platemap=None, skip=(), replica=None, datatype='mean'):
        """
        Constructor for init default value
        :param name: name of plate, very important to file this, it will be use for certain function
        :param platemap: platemap object for this plate
        :param skip: Well to skip for all replica
        :param replica: add one or a list of replica
        :param datatype : mean or median for working array
        """
        super(Plate, self).__init__(name=name, datatype=datatype, skip=skip)
        log.info('Plate created : {}'.format(name))
        self.replica = collections.OrderedDict()
        if platemap is not None:
            self.__add__(platemap)
        else:
            self.platemap = TCA.Core.PlateMap()
        if replica is not None:
            self.__add__(replica)

    def add_platemap(self, platemap):
        """
        Add the platemap to the plate, equivalent to + operator
        :param platemap:
        """
        self.__add__(platemap)

    def get_platemap(self):
        """
        Get the platemap from the plate
        :return: platemap
        """
        return self.platemap

    def add_replica(self, replica):
        """
        Add replicat object to plate, equivalent to + operator
        :param replica: Give a replica object
        """
        self.__add__(replica)

    def get_replica(self, name):
        """
        Get the replicat specified by name, equivalent to [] operator
        :param name: string : key of replica in dict
        :return: Replica object
        """
        return self.replica[name]

    def get_replica_listId(self):
        return [values.name for key, values in self.replica.items()]

    def get_replica_file_location(self):
        return [values.rawdata.get_file_location() for key, values in self.replica.items()]

    def get_all_replica(self):
        """
        Get all replica from plate into a dict
        :return: dict of replica
        """
        return self.replica

    def check_data_consistency(self, remove=False):
        """
        Check if all replica have same well
        :param remove: remove or not replica with data error
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
                log.warning("Missing Well in RawData : {}, missing value can insert ERROR in further analysis.".format(
                    sorted(uniques)))
                if remove:
                    del self.replica[B]
                    log.info("Will be removed -> :{}".format(B))
                else:
                    log.warning("----> Can be removed with appropriate parameters : remove True or False(default)")
                return 0
        return 1

    def get_raw_data(self, replica=None, channel=None, well=None, well_idx=False, as_dict=False):
        """
        Return a dict or serie that contain raw data from all replica (or specified replica), we can specified channel
        (list) and if we want to have well id
        :param replica: replica id
        :param channel: channel list
        :param well: defined or not which well you want, in list [] or simple string format
        :param well_idx: true or false for keeping well id (A1..)
        :return: dict with data
        """
        if as_dict:
            data = {}
        else:
            data = None
        if replica is not None:
            return self.replica[replica].get_rawdata(channel=channel, well=well, well_idx=well_idx)
        else:
            for key, value in self.replica.items():
                try:
                    if as_dict:
                        data[value.get_name()] = value.get_rawdata(channel=channel, well=well, well_idx=well_idx)
                    else:
                        if data is None:
                            data = value.get_rawdata(channel=channel, well=well, well_idx=well_idx)
                        else:
                            data = data.append(value.get_rawdata(channel=channel, well=well, well_idx=well_idx))
                except:
                    continue
            return data

    def get_agg_data_from_replica_channels(self, by='Median'):
        """
        compute all component mean from all replica for each well
        :param by: 'Median' or 'Mean'
        :return: dataframe
        """
        df = None
        for key, rep in self.replica.items():
            assert isinstance(rep, TCA.Replica)
            tmp = rep.rawdata.get_groupby_data()
            if by == 'Median':
                if df is None:
                    df = tmp.median()
                else:
                    df += tmp.median()
            else:
                if df is None:
                    df = tmp.mean()
                else:
                    df += tmp.mean()
        df /= len(self.replica)
        return df.reset_index()

    def agg_data_from_replica_channel(self, channel, use_sec_data=False, forced_update=False, datatype=None):
        """
        Compute the mean/median matrix data of all replica
        If replica data is SpatialNorm already, this function will fill array_c
        :param forced_update: Forced update of replica data, to use when you have determine matrix too soon
        :param use_sec_data: use or not sec data from replica
        :param channel: which channel to have into sum up data
        :param datatype : default to None -> take plate parameters, otherwise compute with given choice
        """
        tmp_array = np.zeros(self.platemap.platemap.shape)
        i = 0
        if datatype is None:
            datatype=self.datatype
        for key, replica in self.replica.items():
            i += 1
            if replica.array is None:
                replica.compute_data_channel(channel, datatype=datatype)
            else:
                if forced_update:
                    replica.compute_data_channel(channel, datatype=datatype)
            self.datatype = datatype
            if not use_sec_data:
                tmp_array = tmp_array + replica.array
            else:
                tmp_array = tmp_array + replica.array_c

        if not use_sec_data:
            self.array = tmp_array / i
        else:
            self.array_c = tmp_array / i
            self.isSpatialNormalized = True

    def cut(self, rb, re, cb, ce, apply_down=True):
        """
        Cut a plate and replica to 'zoom' into a defined zone, for avoiding crappy effect during SEC process
        :param rb: row begin
        :param re: row end
        :param cb: col begin
        :param ce: col end
        :param apply_down: apply the cutting to replica
        """
        if self._is_cutted:
            raise AttributeError('Already cutted')
        log.warning("Cutting operation performed on plate %s" % self.name)
        self.cut(rb, re, cb, ce)
        if apply_down:
            for key, value in self.replica.items():
                value.cut(rb, re, cb, ce)
        self.platemap.cut(rb, re, cb, ce)

    def get_count(self):
        """
        Get count of element (cells) for all wells
        """
        cnt = None
        for key, value in self.replica.items():
            df = value.get_count()
            df = df.transpose()
            if cnt is None:
                cnt = df
            else:
                cnt = pd.concat([cnt, df], axis=0)
        cnt = cnt.fillna(0)
        return cnt

    def __normalization(self, channel, method='Zscore', log_t=True, neg=None, pos=None, skipping_wells=False,
                        threshold=None):
        """
        Apply Well correction on all replica data
        call function like from replica object
        :param pos: positive control
        :param neg: negative control
        :param channel: channel to normalize
        :param method: which method to perform
        :param log_t:  Performed log2 Transformation
        :param skipping_wells: skip defined wells, use it with poc and npi
        :param threshold: used in background subtraction (median is 50) you can set as you want
        """
        for key, value in self.replica.items():
            value.normalization_channels(channels=channel, method=method, log_t=log_t, neg=neg, pos=pos,
                                         skipping_wells=skipping_wells, threshold=threshold)
        self.isNormalized = True
        self.agg_data_from_replica_channel(channel, forced_update=True)

    def normalization_channels(self, channels, method='Zscore', log_t=True, neg=None, pos=None, skipping_wells=False,
                               threshold=None):
        """
        Apply multi channels normalization
        :param pos: positive control
        :param neg: negative control
        :param channels: channel to normalize
        :param method: which method to perform
        :param log_t:  Performed log2 Transformation
        :param skipping_wells: skip defined wells, use it with poc and npi
        :param threshold: used in background subtraction (median is 50) you can set as you want
        """
        log.info("Raw data normalization on {0} with {1} method".format(self.name, method))
        if isinstance(channels, list):
            try:
                for key, value in self.replica.items():
                    value.normalization_channels(channels=channels, method=method, log_t=log_t, neg=neg, pos=pos,
                                                 skipping_wells=skipping_wells, threshold=threshold)
                self.isNormalized = True
            except Exception as e:
                log.error(e)
        else:
            self.__normalization(channels, method, log_t, neg, pos, skipping_wells, threshold=threshold)

    def apply_systematic_error_correction(self, algorithm='Bscore', method='median', apply_down=True, verbose=False,
                                         save=True, max_iterations=100, alpha=0.05, epsilon=0.01, skip_col=[],
                                         skip_row=[], trimmed=0.0, poly_deg=4, low_max_iter=3, f=2./3.):
        """
        Apply a spatial normalization for remove edge effect on all replica (but not to Plate objet himself, use
        instead systematic_error_correction function for only plate array)
        Resulting matrix are save in plate object if save = True
        Be careful !! if the replica data was already be spatial norm, it will degrade data !!
        :param algorithm: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param method: for Bscore : use median or average method
        :param apply_down: apply strategies to replica, if true apply SEC on replica !! not re-use function on plate
        :param verbose: verbose : output the result ?
        :param save: save: save the residual into self.SECData , default = False
        :param max_iterations: max iterations for all technics
        :param alpha: alpha for TTest
        :param epsilon: epsilon parameters for PMP
        :param skip_col: index of col to skip in MEA or PMP
        :param skip_row: index of row to skip in MEA or PMP
        :param trimmed: Bscore only for average method only, trimmed the data with specified value, default is 0.0
        :param poly_deg: polynomial degree 4 or 5
        :param low_max_iter: lowess max iteration
        :param f: lowess smotting span
        """
        __valid_sec_algo = ['Bscore', 'BZscore', 'PMP', 'MEA', 'DiffusionModel', 'Lowess', 'Polynomial']

        if algorithm not in __valid_sec_algo:
            log.error('Algorithm is not good choose : {}'.format(__valid_sec_algo))
            raise ValueError()
        log.info('Systematic Error Correction processing {} : {}'.format(self.name, algorithm))
        if apply_down:
            for key, value in self.replica.items():
                value.systematic_error_correction(algorithm=algorithm, method=method, verbose=verbose, save=save,
                                                  max_iterations=max_iterations, alpha=alpha, epsilon=epsilon,
                                                  skip_col=skip_col, skip_row=skip_row, trimmed=trimmed,
                                                  poly_deg=poly_deg, low_max_iter=low_max_iter, f=f)
            self.agg_data_from_replica_channel(channel=None, use_sec_data=True)
            return


    def write_rawdata(self, path, name=None):
        """
        Save normalized raw data
        :param path: path where to save raw data
        """
        if not os.path.isdir(path):
            os.mkdir(path)
        for key, value in self.replica.items():
            if name is not None:
                value.write_rawdata(path=path, name=name)
            else:
                value.write_rawdata(path=path, name=self.name)

    def write_data(self, path, channel, sec=False):
        """
        Save the Mean of replica and all replica array data
        :param path:
        :param channel: which channel to save
        :param sec: use sec data
        :return:
        """
        if not os.path.isdir(path):
            os.makedirs(path)
        self.agg_data_from_replica_channel(channel=channel, use_sec_data=sec, forced_update=True)

        if sec :
            np.savetxt(fname=os.path.join(path, str(self.name)+'_'+str(channel)) + ".csv", X=self.array_c,
                       delimiter=",", fmt='%1.4f')
            for key, value in self.replica.items():
                np.savetxt(fname=os.path.join(path, str(self.name)+'_'+str(value.name)+'_'+str(channel)) + ".csv",
                           X=value.array_c, delimiter=",", fmt='%1.4f')
        else:
            np.savetxt(fname=os.path.join(path, str(self.name)+'_'+str(channel)) + ".csv", X=self.array,
                       delimiter=",", fmt='%1.4f')
            for key, value in self.replica.items():
                np.savetxt(fname=os.path.join(path, str(self.name)+'_'+str(value.name)+'_'+str(channel)) + ".csv",
                           X=value.array, delimiter=",", fmt='%1.4f')

    def clear_memory(self, only_cache=True):
        """
        Save memory by deleting Raw Data
        :param only_cache: Remove only cache
        """
        for key, value in self.replica.items():
            value.clear_memory(only_cache=only_cache)

    def get_file_location(self):
        """
        return in dict all file location from all replica
        :return:
        """
        floc = collections.OrderedDict()
        for key, value in self.replica.items():
            floc[str(key)] = str(value.get_file_location())
        return floc

    def __sub__(self, to_rm):
        """
        Remove replica from plate, use - operator
        :param to_rm: replica id to remove from plate
        """
        del self.replica[to_rm]

    def __add__(self, to_add):
        """
        Add replica/platemap or list of replica to plate, use + operator
        :param to_add: replica id that is added
        """
        if isinstance(to_add, TCA.Core.Replica):
            name = to_add.name
            to_add.datatype = self.datatype
            self.replica[name] = to_add
        elif isinstance(to_add, TCA.Core.PlateMap):
            self.platemap = to_add
        elif isinstance(to_add, list):
            for elem in to_add:
                assert isinstance(elem, TCA.Core.Replica)
                elem.datatype = self.datatype
                self.replica[elem.name] = elem
        else:
            raise AttributeError("Unsupported Type")

    def __getitem__(self, key):
        """
        Return replica object, use [] operator
        :param key:
        :return: return replica
        """
        return self.replica[key]

    def __setitem__(self, key, value):
        """
        Set replica object, use [] operator
        :param key: name of replica
        :param value: replica object
        """
        if not isinstance(value, TCA.Replica):
            raise AttributeError("Unsupported Type")
        else:
            self.replica[key] = value

    def __len__(self):
        """
        Get len /number of replica inside Plate, use len(object)
        :return: number of replica
        """
        return len(self.replica)

    def __repr__(self):
        """
        Definition for the representation
        """
        return (
            "\nPlate ID : " + repr(self.name) +
            "\n" + repr(self.platemap) +
            "\nData normalized : " + repr(self.isNormalized) +
            "\nData systematic error removed : " + repr(self.isSpatialNormalized) +
            "\nReplica List ID: " + repr(self.get_replica_listId())+
            "\nRawData File location: " + repr(self.get_replica_file_location())
        )

    def __str__(self):
        """
        Definition for the print
        """
        return self.__repr__()

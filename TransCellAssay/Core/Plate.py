# coding=utf-8
"""
Plate is designed for manipulating one or more replica, we store in this class replica object, a platemap object is
attached to this class
"""

import numpy as np
import pandas as pd
import TransCellAssay as TCA
from TransCellAssay.Core.GenericPlate import GenericPlate
import os
import collections
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2017 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class Plate(GenericPlate):
    """
    Class for manipulating plate and their replica, get all attribute and method from MasterPlate

    self.replica = {}                 # Dict that contain all replica, key are name and value are replica object
    self.platemap = TCA.Core.PlateMap()  # Plate Setup object
    """

    def __init__(self, name, platemap=None, skip=(), replica=None, datatype='mean'):
        """
        Constructor for init default value
        :param name: name of plate, very important to file this, it will be use for certain function
        :param platemap: platemap object for this plate,  if none, it will be filled with 96 platemap size
        :param skip: Well to skip for all replica
        :param replica: add one or a list of replica
        :param datatype : mean or median for working array
        """
        super(Plate, self).__init__(name=name, datatype=datatype, skip=skip)
        log.info('Plate created : {}'.format(name))
        self.replica = collections.OrderedDict()
        if platemap is not None:
            if isinstance(platemap, str):
                self.platemap = TCA.Core.PlateMap(fpath=platemap)
            else:
                self.__add__(platemap)
        else:
            self.platemap = TCA.Core.PlateMap()
        if replica is not None:
            self.__add__(replica)

    def set_name(self, name):
        """
        Set name of plate
        """
        if name is not None:
            self.name = name

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

    def remove_replica(self, id):
        """
        remove replica by id
        """
        try:
            self.__sub__(id)
        except Exception as e:
            log.error(e)

    def get_replica(self, name):
        """
        Get the replicat specified by name, equivalent to [] operator
        :param name: string : key of replica in dict
        :return: Replica object
        """
        return self.replica[name]

    def get_replica_listId(self):
        """
        Get the list of replica id
        """
        return [values.name for key, values in self.replica.items()]

    def get_replica_file_location(self):
        """
        Get the list of replica file location
        """
        return [values.get_file_location() for key, values in self.replica.items()]

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
            all_lists.append(list(value.get_unique_well()))
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
        :param as_dict: export data as dict
        :return: dict with data
        """
        if as_dict:
            data = {}
        else:
            data = list()

        if replica is not None:
            return self.replica[replica].get_rawdata(channel=channel, well=well, well_idx=well_idx)
        else:
            for key, value in self.replica.items():
                try:
                    if as_dict:
                        data[value.get_name()] = value.get_rawdata(channel=channel, well=well, well_idx=well_idx)
                    else:
                        data.append(value.get_rawdata(channel=channel, well=well, well_idx=well_idx))
                except:
                    continue
            if as_dict:
                return data
            else:
                return pd.concat(data)

    def get_agg_data_from_replica_channels(self, by='Median'):
        """
        compute all component mean from all replica for each well
        :param by: 'Median' or 'Mean'
        :return: dataframe
        """
        method = ["Median", "Mean"]
        assert by in method, "Must be {0}".format(method)
        df = []
        for key, rep in self.replica.items():
            assert isinstance(rep, TCA.Replica)
            tmp = rep.get_groupby_data()
            if by == 'Median':
                df.append(tmp.median())
            else:
                df.append(tmp.mean())
        DF = pd.concat(df)
        return DF.reset_index().groupby(by=self.WellKey).mean()

    def get_agg_data_from_replica_channel(self, chan=None, sec_data=False):
        """
        get for all rep the data into array format
        """
        if chan is not None:
            self.agg_data_from_replica_channel(chan, forced_update=True)

        lst = []
        namelst = []

        for name, data in self.replica.items():
            if sec_data:
                if data.array_c is not None:
                    lst.append(pd.DataFrame(data.array_c.flatten()))
                    namelst.append(name)
                else:
                    raise AttributeError("Data not corrected")
            else:
                if data.array is not None:
                    lst.append(pd.DataFrame(data.array.flatten()))
                    namelst.append(name)
                else:
                    raise AttributeError("Data not computed")

        res = pd.concat(lst, axis=1)
        res.columns = namelst
        return res

    def use_count_as_data(self):
        """
        Use cells count from raw data, and fill array member with this data
        """
        cnt = self.get_count()
        self.array = cnt.loc[:, "CellsCount Mean"].values.reshape((self.platemap.shape()))
        for name, rep in self.replica.items():
            rep.array = cnt.loc[:, "{} CellsCount".format(name)].values.reshape((self.platemap.shape()))

    def agg_data_from_replica_channel(self, channel, use_sec_data=False, forced_update=False, datatype=None):
        """
        Compute the mean/median (defined by .datatype variable ) matrix (.array or .array_c) data of all replica and plate
        If replica data is SpatialNorm already, this function will fill array_c
        :param forced_update: Forced update of replica data, to use when you have determine matrix too soon
        :param use_sec_data: use or not sec data from replica
        :param channel: which channel to have into sum up data
        :param datatype : default to None -> take plate parameters, otherwise compute with given choice
        """

        i = 0
        if datatype is None:
            datatype = self.datatype
        self.datatype = datatype
        change = False
        for key, replica in self.replica.items():
            if forced_update:
                replica.compute_data_channel(channel, datatype=datatype)
                change = True
            else:
                if replica.array is None:
                    replica.compute_data_channel(channel, datatype=datatype)
                else:
                    replica.compute_data_channel(channel, datatype=datatype)
                    change = True

            i += 1

        if change:
            if self._array_channel != channel:
                log.warning('Overwriting Data : {0} -> {1} on {2}'.format(
                    self._array_channel, channel, self.name))

        if not use_sec_data:
            self._mean_array()
        else:
            self._mean_array_c()

        self._array_channel = channel

    def _mean_array(self):
        """
        Compute the mean of data of all replica
        """

        lst = []
        for key, replica in self.replica.items():
            lst.append(pd.DataFrame(replica.array.flatten()))

        x = pd.concat(lst, axis=1).mean(axis=1).values.reshape(self.platemap.platemap.shape)
        self.array = x

    def _mean_array_c(self):
        """
        Compute the mean of corrected data of all replica
        """
        lst = []
        for key, replica in self.replica.items():
            lst.append(pd.DataFrame(replica.array_c.flatten()))

        x = pd.concat(lst, axis=1).mean(axis=1).values.reshape(self.platemap.platemap.shape)
        self.array_c = x

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
        return TCA.getEventsCounts(self)

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
        log.info("{0} -> Rawdata normalization with {1} method".format(self.name, method))
        if isinstance(channels, list):
            for channel in channels:
                self.__normalization(channel=channel, method=method, log_t=log_t, neg=neg, pos=pos,
                                         skipping_wells=skipping_wells, threshold=threshold)
        else:
            self.__normalization(channels, method, log_t, neg, pos, skipping_wells, threshold=threshold)
        self.isNormalized = True
        self.RawDataNormMethod = method
        self.clear_cache()

    def apply_systematic_error_correction(self, algorithm='Bscore', apply_down=True, verbose=False,
                                          save=True, max_iterations=100, alpha=0.05, epsilon=0.01, skip_col=[],
                                          skip_row=[], poly_deg=4, low_max_iter=3, f=2./3.):
        """
        Apply a spatial normalization for remove edge effect on all replica (but not to Plate objet himself, use
        instead systematic_error_correction function for only plate array)
        Resulting matrix are save in plate object if save = True
        Be careful !! if the replica data was already be spatial norm, it will degrade data !!
        :param algorithm: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param apply_down: apply strategies to replica, if true apply SEC on replica !! not re-use function on plate
        :param verbose: verbose : output the result ?
        :param save: save: save the residual into self.SECData , default = False
        :param max_iterations: max iterations for all technics
        :param alpha: alpha for TTest
        :param epsilon: epsilon parameters for PMP
        :param skip_col: index of col to skip in MEA or PMP
        :param skip_row: index of row to skip in MEA or PMP
        :param poly_deg: polynomial degree 4 or 5
        :param low_max_iter: lowess max iteration
        :param f: lowess smotting span
        """
        __valid_sec_algo = ['Bscore', 'BZscore', 'PMP', 'MEA', 'DiffusionModel', 'Lowess', 'Polynomial']

        if algorithm not in __valid_sec_algo:
            log.error('Algorithm is not available choose : {}'.format(__valid_sec_algo))
            raise ValueError()
        log.info('Systematic Error Correction processing {0} : {1}'.format(self.name, algorithm))
        # Apply only to replica array and get mean of these replica array_c
        if apply_down:
            for key, value in self.replica.items():
                value.systematic_error_correction(algorithm=algorithm, verbose=verbose, save=save,
                                                  max_iterations=max_iterations, alpha=alpha, epsilon=epsilon,
                                                  skip_col=skip_col, skip_row=skip_row, poly_deg=poly_deg,
                                                  low_max_iter=low_max_iter, f=f)
            self._mean_array_c()
        else:
            # apply sec only on plate.array to get array_c
            self.systematic_error_correction(algorithm=algorithm, verbose=verbose, save=save,
                                             max_iterations=max_iterations, alpha=alpha, epsilon=epsilon,
                                             skip_col=skip_col, skip_row=skip_row, poly_deg=poly_deg,
                                             low_max_iter=low_max_iter, f=f)

    def write_rawdata(self, path, name=None):
        """
        Save normalized raw data
        :param path: path where to save raw data
        :param name: name of file
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

    def clear_cache(self):
        """
        Save memory by deleting Raw Data
        """
        for key, value in self.replica.items():
            value.clear_cache()

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
            "\nReplica List ID: " + repr(self.get_replica_listId()) +
            "\nRawData File location: " + repr(self.get_replica_file_location())
        )

    def __str__(self):
        """
        Definition for the print
        """
        return self.__repr__()

    def __iter__(self):
        """
        Iterator on replica
        """
        for key, value in self.replica.items():
            yield key, value

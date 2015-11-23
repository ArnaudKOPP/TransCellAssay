# coding=utf-8
"""
Replica implement the notion of technical replica for plate, in real, it represent one plate
"""

import pandas as pd
import os
import numpy as np
import TransCellAssay as TCA
from TransCellAssay.Core.GenericPlate import GenericPlate
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class Replica(GenericPlate):
    """
    Class for manipulating replica of plate, get all attribute and method from MasterPlate
    self.rawdata = rawdata              # rawdata object
    """

    def __init__(self, name, fpath, FlatFile=True, skip=(), datatype='mean', **kwargs):
        """
        Constructor
        :param name: name of replica
        :param fpath: Data for replica object
        :param singleCells: Are data single cell type or not
        :param skip: Well to skip
        :param datatype: Median or Mean data
        """
        super(Replica, self).__init__(name=name, datatype=datatype, skip=skip)
        log.debug('Replica created : {}'.format(name))

        if not FlatFile:
            self.set_data(fpath)

        else:
            if isinstance(fpath, str):
                if os.path.isfile(fpath):
                    log.info('Reading FlatFile : %s' % fpath)
                    self.df = pd.read_csv(fpath, engine='c', **kwargs)
                    log.debug('Finished')
                    self.__file = fpath
                else:
                    raise IOError('File don\'t exist')

            elif isinstance(fpath, TCA.InputFile):
                if fpath.dataframe is not None:
                    self.df = fpath.dataframe
                    self.__file = fpath.get_file_path()
                else:
                    raise ValueError('Empty Input File')
            else:
                raise NotImplementedError('Input types not handled')

        self.__CACHING_gbdata = None
        self.__CACHING_gbdata_key = None

    def get_channels_list(self):
        """
        Get all channels/component in list
        :return: list of channel/component
        """
        if self.df is not None:
            return self.df.columns.tolist()
        else:
            raise IOError('Empty rawdata')

    def set_rawdata(self, df):
        """
        Set data in replica
        :param input_file: csv file
        """
        assert isinstance(df, pd.DataFrame)
        self.df = df

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

    def df_to_array(self, chan, rowId='Row', colId='Columm'):
        """
        To use only with 1data/well Raw data !!
        :param chan: on which channel to work
        :param rowId: row Columm name
        :param colId: column Column name
        :return:
        """
        log.warning("Only to use with 1Data/Well Raw data")
        size = len(self.df)
        if size <= 96:
            array = np.zeros((8, 12))
        elif size <= 384:
            array = np.zeros((16, 24))
        elif size > 384:
            array = np.zeros((32, 48))
            log.warning('1536 well plate size')
        for i in range(size):
            array[self.df[rowId][i]][self.df[colId][i]] = self.df[chan][i]
        return array

    def get_unique_well(self, well_key='Well'):
        """
        return all unique wells
        :return:
        """
        if self.df is None:
            raise IOError('Empty rawdata')
        return self.df[well_key].unique()

    def get_rawdata(self, channel=None, well=None, well_idx=False):
        """
        Get Raw data with specified param
        :param channel: defined or not channel
        :param well: defined or not which well you want, in list [] or simple string format
        :param well_idx: add or not well id
        :return: raw data in pandas dataframe
        """
        if self.df is None:
            raise IOError('Empty rawdata')
        # # add well to columns that we want
        # # check valid channel
        if channel is not None and channel not in self.get_channels_list():
            raise ValueError('Wrong Channel')
        if well_idx:
            if not isinstance(channel, list):
                channel = [channel]
            channel.insert(0, 'Well')

        # # init a empty list
        data = list()

        # # if well not a list -> become a list
        if well is not None:
            if not isinstance(well, list):
                well = [well]
                if well not in self.get_unique_well():
                    raise ValueError('Wrong Well')

        # # Grab data
        if well is not None:
            for i in well:
                try:
                    x = self.__get_Well_group(i, channel)
                    data.append(x)
                except:
                    pass
                # # return wells data for channel
            return pd.concat(data)
        else:
            # # return channel data for all well
            return self.df

    def compute_data_channel(self, channel, datatype='mean'):
        """
        Compute data in matrix form, get mean or median for well and save them in replica object
        :param channel: which channel to keep in matrix
        :return:
        """
        if self.array is not None:
            if self._array_channel is not channel:
                log.warning('Overwriting previous channel data from {} to {}'.format(
                    self._array_channel, channel))
        self.array = self.__compute_data_channel(channel=channel, type_mean=datatype)
        self.datatype = datatype
        self._array_channel = channel

    def __compute_data_channel(self, channel, type_mean='mean', defsize=None):
        """
        Compute mean or median for each well in matrix format
        :param channel: Which channel to get
        :param type_mean: Mean or median
        :param defsize: you can set the size of plate if you want
        :return:
        """
        if self.df is None:
            raise IOError('Empty rawdata')
        gbdata = self.get_groupby_data()
        if type_mean is 'median':
            tmp = gbdata.median()
        elif type_mean is 'mean':
            tmp = gbdata.mean()
        channel_val = tmp[channel]
        position_value_dict = channel_val.to_dict()  # # dict : key = pos and item are mean
        size = len(position_value_dict)
        if defsize is None:
            data = self.__init_array(size)
        else:
            data = self.__init_array(defsize)
        for key, elem in position_value_dict.items():
            try:
                pos = TCA.get_opposite_well_format(key)
                data[pos[0]][pos[1]] = elem
            except IndexError:
                return self.get_data_channel(channel,type_mean, size*2)
        return data

    def __init_array(self, size):
        if size <= 96:
            return np.zeros((8,12))
        elif size <= 384:
            return np.zeros((16,24))
        else:
            return np.zeros((32,42))

    def get_mean_channels(self):
        """
        Compute for all channels the mean for each wells
        :return: mean for each wells for all channels
        """
        tmp = self.get_groupby_data()
        return tmp.mean().reset_index()

    def get_median_channels(self):
        """
        Compute for all channels the median for each wells
        :return: median for each wells for all channels
        """
        tmp = self.get_groupby_data()
        return tmp.median().reset_index()

    def get_data_channel(self, channel, sec=False):
        """
        Return data in matrix form, get mean or median for well
        :param channel: which channel to keep in matrix
        :param sec: want Systematic Error Corrected data ? default=False
        :return: compute data in matrix form
        """
        if sec:
            if self.array_c is None:
                raise ValueError('Process Systematic Error Correction method before')
            else:
                return self.array_c
        if self.array is None:
            self.compute_data_channel(channel)
        if channel is self._array_channel:
            return self.array
        else:
            self.compute_data_channel(channel)
            return self.array

    def get_count(self, well_key='Well'):
        """
        Get the count for all well
        :return:
        """
        gb_data = self.get_groupby_data()
        cnt = gb_data[well_key].count().to_frame()
        cnt.columns = ['Count_'+str(self.name)]
        cnt = cnt.fillna(0)
        return cnt

    def __normalization(self, channel, method='Zscore', log_t=True, neg=None, pos=None, skipping_wells=False,
                        threshold=None):
        """
        Performed normalization on data
        :param channel; which channel to normalize
        :param method: Performed X Transformation
        :param log_t:  Performed log2 Transformation
        :param pos: positive control
        :param neg: negative control
        :param skipping_wells: skip defined wells, use it with poc and npi
        :param threshold: used in background subtraction (median is 50) you can set as you want
        """
        if not self.isNormalized:
            log.warning("RawData are already normalized on some channel")

        log.debug('Replica {} : RawData normalization on channel {}'.format(self.name, channel))
        if skipping_wells:
            negative = [x for x in neg if (TCA.get_opposite_well_format(x) not in self.skip_well)]
            positive = [x for x in pos if (TCA.get_opposite_well_format(x) not in self.skip_well)]
        else:
            negative = neg
            positive = pos
        TCA.rawdata_variability_normalization(self,
                                                channel=channel,
                                                method=method,
                                                log2_transf=log_t,
                                                neg_control=negative,
                                                pos_control=positive,
                                                threshold=threshold)
        self.compute_data_channel(channel)

    def normalization_channels(self, channels, method='Zscore', log_t=True, neg=None, pos=None, skipping_wells=False,
                               threshold=None):
        """
        Apply a normalization method to multiple
        :param pos: positive control
        :param neg: negative control
        :param channels: channel to normalize
        :param method: which method to perform
        :param log_t:  Performed log2 Transformation
        :param skipping_wells: skip defined wells, use it with poc and npi
        :param threshold: used in background subtraction (median is 50) you can set as you want
        """
        if isinstance(channels, str):
            self.__normalization(channel=channels, method=method, log_t=log_t, neg=neg, pos=pos,
                                 skipping_wells=skipping_wells, threshold=threshold)
        elif isinstance(channels, list):
            for chan in channels:
                self.__normalization(channel=chan, method=method, log_t=log_t, neg=neg, pos=pos,
                                     skipping_wells=skipping_wells, threshold=threshold)

            log.warning("Choose your channels that you want to work with plate.agg_data_from_replica_channel or "
                        "replica.data_for_channel")
        self.isNormalized = True
        self.RawDataNormMethod = method

    def write_rawdata(self, path, name=None):
        """
        Save normalized Raw data
        :param name: Give name to file
        :param path: Where to write .csv file
        """
        if name is None:
            name = self.name
        self.rawdata.write_rawdata(path=path, name=name)

    def __write_raw_data(self, filepath, **kwargs):
        """
        Save normalized Raw data
        :param name: Give name to file
        :param path: Where to write .csv file
        """
        if not os.path.isdir(path):
            os.mkdir(path)
        if name is not None:
            fpath = os.path.join(path, name)+'.csv'
            self.__write_raw_data(fpath, **kwargs)
            log.info('Writing File : {}'.format(fpath))
        else:
            raise Exception("Writing Raw data problem")

    def write_data(self, path, channel, sec=False):
        """
        Write array
        :param path:
        :param channel:
        :param sec:
        :return:
        """
        self.compute_data_channel(channel=channel)
        if sec:
            np.savetxt(fname=os.path.join(path, str(self.name)+'_'+str(channel)) + ".csv",
                           X=self.array_c, delimiter=",", fmt='%1.4f')
        else:
            np.savetxt(fname=os.path.join(path, str(self.name)+'_'+str(channel)) + ".csv",
                           X=self.array, delimiter=",", fmt='%1.4f')

    def get_file_location(self):
        """
        return file location from data
        :return:
        """
        return self.__file

    def clear_memory(self, only_cache=True):
        """
        Remove some data for saving memory
        :param only_caching: remove only cache
        """
        self.__CACHING_gbdata = None
        self.__CACHING_gbdata_key = None
        log.debug('Cache cleared')
        if not only_cache:
            self.df = None
            log.debug('Rawdata cleared')

    def get_groupby_data(self, key='Well'):
        """
        Perform a groupby on raw data, a 'caching' is set up for avoid computations if groupby was already performed
        :param key:
        :return:
        """
        if self.__CACHING_gbdata is not None:
            if key is self.__CACHING_gbdata_key:
                return self.__CACHING_gbdata
            else:
                self._new_caching(key)
                return self.__CACHING_gbdata
        else:
            self._new_caching(key)
            return self.__CACHING_gbdata

    def _new_caching(self, key='Well'):
        self.__CACHING_gbdata = self.df.groupby(key)
        self.__CACHING_gbdata_key = key
        log.debug('Created rawdata cache')

    def __get_Well_group(self, key, channel=None):
        """
        Get all data for a well
        :param channel:
        :param key:
        :return:
        """
        if self.__CACHING_gbdata is None:
            self._new_caching()
        if channel is not None:
            return self.__CACHING_gbdata.get_group(key)[channel]
        else:
            return self.__CACHING_gbdata.get_group(key)

    def __iter__(self):
        """
        iterate on group with groups key
        """
        if self.__CACHING_gbdata is None:
            self.__new_caching()
        for key, value in self.__CACHING_gbdata.groups.items():
            yield key, value

    def __repr__(self):
        """
        Definition for the representation
        """
        return ("\nReplica ID : " + repr(self.name) +
                "\nData normalized : " + repr(self.isNormalized) +
                "\nData systematic error removed : " + repr(self.isSpatialNormalized) +
                "\nRawData File location :"+repr(self.__file) +
                "\n" + repr(self.df.head()) + "\n")

    def __str__(self):
        """
        Definition for the print
        """
        return self.__repr__()

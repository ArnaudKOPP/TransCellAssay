# coding=utf-8
"""
Class that store raw data in single cell, we use pandas dataframe for storing in memory
Need a specific format for running optimum

Well    Channel1     Channel2
A1
A1
A2
..
"""

import pandas as pd
import os
import numpy as np
import TransCellAssay as TCA
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class RawData(object):
    """
    Raw data that contain value in single cell level
    """

    def __init__(self, path_or_file):
        """
        Constructor
        :param path_or_file:
        :return:
        """
        if isinstance(path_or_file, str):
            if os.path.isfile(path_or_file):
                self.df = pd.read_csv(path_or_file, engine='c')
                log.info('Reading RawData %s File' % path_or_file)
            else:
                raise IOError('File don\'t exist')

        elif isinstance(path_or_file, TCA.InputFile):
            if path_or_file.dataframe is not None:
                self.df = path_or_file.dataframe
            else:
                raise ValueError('Empty Input File')
        else:
            raise NotImplementedError('Input types not handled')

        self.__CACHING_gbdata = None
        self.__CACHING_gbdata_key = None

    def get_channel_list(self):
        """
        Get all channels/component in list
        :return: list of channel/component
        """
        if self.df is not None:
            return self.df.columns.tolist()
        else:
            raise IOError('Empty rawdata')

    def get_raw_data(self, channel=None, well=None, well_idx=False):
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
        if well_idx:
            if not isinstance(channel, list):
                channel = [channel]
            channel.insert(0, 'Well')

        # # init a empty df
        data = None

        # # if well not a list -> become a list
        if well is not None:
            if not isinstance(well, list):
                well = [well]
                if well not in self.get_unique_well():
                    raise ValueError('Wrong Well')

        # # Grab data
        if channel is not None:
            # # check valid channel
            if channel not in self.get_channel_list():
                raise ValueError('Wrong Channel')
            if well is not None:
                for i in well:
                    if data is None:
                        data = self.__get_group(i, channel)
                    data = data.append(self.__get_group(i, channel))
                    # # return wells data for channel
                return data
            else:
                # # return channel data for all well
                return self.df[channel]
        else:
            if well is not None:
                for i in well:
                    if data is None:
                        data = self.__get_group(i)
                    data = data.append(self.__get_group(i))
                    # # return wells data for all channel
                return data
            else:
                # # return all data
                return self.df

    def get_unique_well(self):
        """
        return all unique wells
        :return:
        """
        if self.df is None:
            raise IOError('Empty rawdata')
        return self.df.Well.unique()

    def df_to_array(self, chan):
        """
        To use only with 1data/well Raw data !!
        :param chan:
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
            array[self.df['Row'][i]][self.df['Column'][i]] = self.df[chan][i]
        return array

    def compute_matrix(self, channel, type_mean='mean'):
        """
        Compute mean or median for each well in matrix format
        :param channel:
        :param type_mean:
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
        if len(position_value_dict) <= 96:
            data = np.zeros((8, 12))
        elif len(position_value_dict) <= 384:
            data = np.zeros((16, 24))
        elif len(position_value_dict) > 384:
            raise NotImplementedError('MAX 384 Well plate: bigger plate are not implemented')
        for key, elem in position_value_dict.items():
            pos = TCA.get_opposite_well_format(key)
            data[pos[0]][pos[1]] = elem
        return data

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

    def __get_group(self, key, channel=None):
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

    def save_raw_data(self, path, name=None):
        """
        Save normalized Raw data
        :param name: Give name to file
        :param path: Where to write .csv file
        """
        if not os.path.isdir(path):
            os.mkdir(path)
        if name is not None:
            self.__write_raw_data(os.path.join(path, name)+'.csv')
        else:
            raise Exception("Writing Raw data problem")

    def __write_raw_data(self, filepath):
        self.df.to_csv(path=filepath, index=False)
        log.info('Writing File : {}'.format(filepath))

    def save_memory(self, only_caching=True):
        """
        Remove some data for saving memory
        :param only_caching: remove only cache
        """
        self.__CACHING_gbdata = None
        self.__CACHING_gbdata_key = None
        log.debug('Cache cleared')
        if not only_caching:
            self.df = None
            log.debug('Rawdata cleared')

    def __len__(self):
        return len(self.df)

    def __repr__(self):
        return "\nRaw Data head : \n" + repr(self.df.head())

    def __str__(self):
        return self.__repr__()
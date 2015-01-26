# coding=utf-8
"""
Class that store raw data in single cell or 1data/well
use pandas dataframe for storing

Need a specific format for running optimum

Well    X     X
A1
A2
..
"""

import pandas as pd
import os
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


class RawData(object):
    """
    Raw data that contain value in single cell level or 1data/well
    :param path_or_file:
    """

    def __init__(self, path_or_file):
        if isinstance(path_or_file, str):
            self.__CACHING_gbdata = None
            self.__CACHING_gbdata_key = None
            try:
                self.df = pd.read_csv(path_or_file, engine='c')
                print('\033[0;32m[INFO]\033[0m Reading %s File' % path_or_file)
            except Exception:
                try:
                    self.df = pd.read_csv(path_or_file, decimal=",", sep=";", engine='c')
                    print('\033[0;32m[INFO]\033[0m Reading %s File' % path_or_file)
                except Exception as e:
                    print('\033[0;31m[ERROR]\033[0m  Error in reading %s File : ' % path_or_file, e)
        elif isinstance(path_or_file, TCA.InputFile):
            raise NotImplementedError
        else:
            print("\033[0;31m[ERROR]\033[0m")

    def get_channel_list(self):
        """
        Get all channels/component in list
        :return: list of channel/component
        """
        try:
            return self.df.columns.tolist()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_raw_data(self, channel=None, well=None, well_idx=False):
        """
        Get Raw data with specified param
        :param channel: defined or not channel
        :param well: defined or not which well you want, in list [] or simple string format
        :param well_idx: add or not well id
        :return: raw data in pandas dataframe
        """
        try:
            if well_idx:
                if not isinstance(channel, list):
                    channel = [channel]
                channel.insert(0, 'Well')
            data = None
            if well is not None:
                if not isinstance(well, list):
                    well = [well]
                datagp = self.get_groupby_data()

            if channel is not None:
                if well is not None:
                    for i in well:
                        if data is None:
                            data = datagp.get_group(i)[channel]
                        data = data.append(datagp.get_group(i)[channel])
                    return data
                else:
                    return self.df[channel]
            else:
                if well is not None:
                    for i in well:
                        if data is None:
                            data = datagp.get_group(i)
                        data = data.append(datagp.get_group(i))
                    return data
                else:
                    return self.df
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_unique_well(self):
        """
        return all unique wells
        :return:
        """
        try:
            return self.df.Well.unique()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def df_to_array(self, chan):
        """
        To use only with 1data/well Raw data !!
        :param chan:
        :return:
        """
        print("\033[0;33m[INFO/WARNING]\033[0m Only to use with 1Data/Well Raw data")
        size = len(self.df)
        if size <= 96:
            array = np.zeros((8, 12))
        elif size <= 384:
            array = np.zeros((16, 24))
        elif size > 384:
            raise NotImplementedError('MAX 384 Well plate are not implemented')
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
        try:
            gbdata = self.get_groupby_data()
            if type_mean is 'median':
                tmp = gbdata.median()
            elif type_mean is 'mean':
                tmp = gbdata.mean()
            channel = tmp[channel]
            dict_pos_mean = channel.to_dict()  # # dict : key = pos and item are mean
            if len(dict_pos_mean) <= 96:
                data = np.zeros((8, 12))
            elif len(dict_pos_mean) <= 384:
                data = np.zeros((16, 24))
            elif len(dict_pos_mean) > 384:
                raise NotImplementedError('MAX 384 Well plate are not implemented')
            for key, elem in dict_pos_mean.items():
                pos = TCA.get_opposite_well_format(key)
                data[pos[0]][pos[1]] = elem
            return data
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_groupby_data(self, key='Well'):
        """
        Perform a groupby on raw data, a 'caching' is set up for avoid computations if groupby was already perfomed
        :param key:
        :return:
        """
        try:
            if self.__CACHING_gbdata is not None:
                if key is self.__CACHING_gbdata_key:
                    return self.__CACHING_gbdata
                else:
                    self._new_caching(key)
                    return self.__CACHING_gbdata
            else:
                self._new_caching(key)
                return self.__CACHING_gbdata
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def _new_caching(self, key):
        self.__CACHING_gbdata = self.df.groupby(key)
        self.__CACHING_gbdata_key = key

    def save_raw_data(self, path, name=None):
        """
        Save normalized Raw data
        :param name: Give name to file
        :param path: Where to write .csv file
        """
        try:
            if not os.path.isdir(path):
                os.mkdir(path)
            if name is not None:
                self._write_raw_data(os.path.join(path, name)+'.csv')
            else:
                raise Exception("Writing Raw data problem")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def _write_raw_data(self, filepath):
        self.df.to_csv(path=os.path.join(filepath) + ".csv", index=False)
        print('\033[0;32m[INFO]\033[0m Writing File : {}'.format(filepath))

    def save_memory(self, only_caching=True):
        """
        Remove some data for saving memory
        :param only_caching: remove only cache
        """
        try:
            self.__CACHING_gbdata = None
            self.__CACHING_gbdata_key = None
            if not only_caching:
                self.df = None
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        try:
            return "\n Raw Data head : \n" + repr(self.df.head())
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        try:
            return self.__repr__()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)
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
            try:
                self.values = pd.read_csv(path_or_file)
                self._gbdata = None
                self._gbdata_key = None
                print('\033[0;32m[INFO]\033[0m Reading %s File' % path_or_file)
            except:
                try:
                    self.values = pd.read_csv(path_or_file, decimal=",", sep=";")
                    print('\033[0;32m[INFO]\033[0m Reading %s File' % path_or_file)
                except Exception as e:
                    print('\033[0;31m[ERROR]\033[0m  Error in reading %s File : ' % path_or_file, e)
        elif isinstance(path_or_file, TCA.InputFile):
            raise NotImplementedError
        else:
            print("\033[0;31m[ERROR]\033[0m")

    def get_feature_list(self):
        """
        Get all features/component in list
        :return: list of feature/component
        """
        try:
            return self.values.columns.tolist()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_raw_data(self, feature=None, well=None, well_idx=False):
        """
        Get Raw data with specified param
        :param feature: defined or not feature
        :param well: defined or not which well you want, in list [] or simple string format
        :param well_idx: add or not well id
        :return: raw data in pandas dataframe
        """
        try:
            if well_idx:
                if not isinstance(feature, list):
                    feature = [feature]
                feature.insert(0, 'Well')
            data = None
            if well is not None:
                if not isinstance(well, list):
                    well = [well]
                datagp = self.get_groupby_data()

            if feature is not None:
                if well is not None:
                    for i in well:
                        if data is None:
                            data = datagp.get_group(i)[feature]
                        data = data.append(datagp.get_group(i)[feature])
                    return data
                else:
                    return self.values[feature]
            else:
                if well is not None:
                    for i in well:
                        if data is None:
                            data = datagp.get_group(i)
                        data = data.append(datagp.get_group(i))
                    return data
                else:
                    return self.values
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def df_to_array(self, feat):
        """

        :param feat:
        :return:
        """
        size = len(self.values)
        if size == 96:
            array = np.zeros((8, 12))
        else:
            array = np.zeros((16, 24))
        for i in range(size):
            array[self.values['Row'][i]][self.values['Column'][i]] = self.values[feat][i]
        return array

    def compute_matrix(self, feature, type_mean='mean'):
        """

        :param feature:
        :param type_mean:
        :return:
        """
        try:
            grouped_data_by_well = self.get_groupby_data()
            if type_mean is 'median':
                tmp = grouped_data_by_well.median()
            elif type_mean is 'mean':
                tmp = grouped_data_by_well.mean()
            feature = tmp[feature]
            dict_mean = feature.to_dict()  # # dict : key = pos and item are mean
            if not len(dict_mean) > 96:
                data = np.zeros((8, 12))
            else:
                data = np.zeros((16, 24))
            for key, elem in dict_mean.items():
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
            if self._gbdata is not None:
                if key is self._gbdata_key:
                    return self._gbdata
                else:
                    return self.values.groupby(key)
            else:
                return self.values.groupby(key)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def save_raw_data(self, path, name=None):
        """
        Save normalized Raw data
        :param name: Give name to file
        :param path: Where to write .csv file
        """
        try:
            if not os.path.isdir(path):
                os.mkdir(path)
            if name is None:
                print(os.path.join(path, name) + ".csv")
                self.values.to_csv(path=os.path.join(path, name) + ".csv", index=False)
                print('\033[0;32m[INFO]\033[0m Writing File')
            else:
                raise Exception("\033[0;33m[WARNING]\033[0m Can't save Data, need name for replicat")
        except Exception as e:
            print(e)

    def __repr__(self):
        try:
            return "\n Raw Data head : \n" + repr(self.values.head())
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        try:
            return "\n Raw Data head : \n" + repr(self.values.head())
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)
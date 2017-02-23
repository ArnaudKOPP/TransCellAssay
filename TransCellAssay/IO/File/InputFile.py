# coding=utf-8
"""
Basic Class for manipulating data into dataframe
"""

import numpy as np
import os
import re
import logging

log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2017 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class InputFile(object):
    """
    InputFile is scaffold for CSV, Excel and txt data
    """

    def __init__(self):
        self.dataframe = None
        self.is1Datawell = False
        self.__col = None
        self.__filepath = None
        self.WellKey = 'WellId'

    def load(self, fpath):
        """
        Load data
        :param fpath: File path
        """
        raise NotImplementedError

    def format_well_format(self):
        """
        Format data by removing some blank space and to have a good well if format
        """
        log.debug('Formatting Well')
        # remove some blank space
        self.dataframe.loc[:, self.WellKey] = self.dataframe.loc[:, self.WellKey].apply(
            lambda x: re.sub('(\s)(?<!$)', '', x))
        # pass to B01 to B1
        self.dataframe.loc[:, self.WellKey] = self.dataframe.loc[:, self.WellKey].apply(
            lambda x: re.sub('(0)(?<!$)', '', x))
        self.rename_col(self.WellKey, 'Well')

    def get_col(self):
        """
        Get all Columns
        """
        if self.__col is None:
            self.__col = self.dataframe.columns.tolist()
        return self.__col

    def remove_col(self, to_remove=[]):
        """
        Remove useless col
        :param to_remove: list of col to remove
        """
        # columns that we can remove because useless
        useless = ['X', 'Y', 'Z', 'Width', 'Height', 'PixelSizeX', 'PixelSizeY', 'PixelSizeZ', 'Row',
                   'Column', 'Status'] + to_remove
        for col in useless:
            if col in self.dataframe.columns.unique():
                try:
                    self.dataframe = self.dataframe.drop([col], axis=1)
                    log.debug("Column {}  removed".format(col))
                except Exception as e:
                    log.warning("Column {} impossible to remove".format(col))
                    log.error(e)

    def replace_nan(self, by=0):
        """
        Replace all NaN by 0 or input choosed
        :param by: by what replace nan
        :return:
        """
        try:
            self.dataframe.fillna(by, inplace=True)
            log.debug("Replace Nan by {0}".format(by))
        except Exception as e:
            log.error(e)
            pass

    def remove_nan(self):
        """
        Remove NaN in dataframe
        :return:
        """
        try:
            self.dataframe = self.dataframe.dropna(axis=0)
            log.debug('Removed Nan on data')
        except Exception as e:
            log.error(e)
            pass

    def rename_col(self, colname, newcolname):
        """
        Rename a column name
        :param colname:
        :param newcolname:
        """
        if colname in self.get_col():
            self.dataframe = self.dataframe.rename(columns={str(colname): str(newcolname)})
            log.debug('Rename colunm {0} to {1}'.format(colname, newcolname))
        else:
            log.warning('Not in dataframe {}'.format(colname))

    def formatting(self):
        """
        Format string into float
        :return:
        """

        def __str_to_flt(x):
            return float(x)

        # # change , to . in float
        for chan in self.get_col():
            self.dataframe[chan].apply(__str_to_flt)
            if self.dataframe[chan].dtypes == 'object':
                self.dataframe[chan] = self.dataframe[chan].str.replace(",", ".")

    def write_raw_data(self, path, name, frmt='csv', **kwargs):
        """
        Write raw data into csv
        :param name: Name of file
        :param path: Directory where to save file
        :param frmt: format of data, csv by default
        """
        log.info("Writing raw data")
        fname = os.path.join(path, name)
        if frmt is 'csv':
            fname += '.csv'
            self.dataframe.to_csv(fname, index=False, index_label=False)
            log.info('Finished  %s' % fname)
        elif frmt is 'txt':
            fname += '.txt'
            self.dataframe.to_csv(fname, sep='\t', index=False, index_label=False, **kwargs)
            log.info('Finished %s' % fname)
        else:
            raise NotImplementedError('Format not supported for the moment')

    def df_to_array(self, channel, size=None):
        """
        Change shape in list from 1Data/well to numpy matrix
        :param channel: which channel to have in matrix format
        :param size: size/len of data 6, 24, 96, 384 or 1536
        :return: numpy array
        """
        if self.is1Datawell:
            if self.dataframe is not None:
                if size is None:
                    size = len(self.dataframe)
                elif size == 6:
                    array = np.zeros((2, 3))
                elif size == 24:
                    array = np.zeros((4, 6))
                elif size == 96:
                    array = np.zeros((8, 12))
                elif size == 384:
                    array = np.zeros((16, 24))
                else:
                    array = np.zeros((24, 48))
                for i in range(size):
                    try:
                        array[self.dataframe['Row'][i]-1][self.dataframe['Column'][i]-1] = self.dataframe[channel][i]
                    except:
                        pass
                return array
            else:
                raise Exception('Empty raw data')
        else:
            raise Exception('Not applicable on this data type')

    def get_file_path(self):
        return self.__filepath

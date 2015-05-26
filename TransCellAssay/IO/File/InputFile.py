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
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class InputFile(object):
    """
    InputFile is scaffold for CSV, Excel and txt data
    """

    def __init__(self):
        self.dataframe = None
        self.is1Datawell = False
        self.__col = None

    def load(self, fpath):
        """
        Load data
        :param fpath: File path
        """
        raise NotImplementedError

    def format_well_format(self, row='Row', col='Column'):
        """
        Format data
        :param col: column name for col id
        :param row: column name for row id
        """
        log.debug('Change row format from int to string')
        self.dataframe = self.dataframe.replace({'Row': {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
                                                         8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
                                                         15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V',
                                                         22: 'W', 23: 'X', 24: 'Y', 25: 'Z',26: 'AA', 27: 'AB',
                                                         28: 'AC', 29: 'AD', 30: 'AE', 31: 'AF'}})
        # # insert Well columns
        self.dataframe.insert(0, "Well", 0)
        # # put Well value from row and col columns
        log.debug('Create Well column with good frmt')
        self.dataframe['Well'] = self.dataframe.apply(lambda x: '%s%.3g' % (x[row], x[col] + 1), axis=1)
        remove = [row, col]
        log.debug('Remove old col and row column')
        self.dataframe = self.dataframe.drop(remove, axis=1)

    def get_col(self):
        """
        Get all Columns
        """
        if self.__col is None:
            self.__col = self.dataframe.columns()
        return self.__col

    def remove_col(self):
        """
        Remove useless col
        """
        # columns that we can remove because useless
        useless = ['PlateNumber', 'FieldNumber', 'CellNumber', 'X', 'Y', 'Z', 'Width', 'Height', 'PixelSizeX',
                   'PixelSizeY', 'PixelSizeZ']
        for col in useless:
            try:
                self.dataframe = self.dataframe.drop([col], axis=1)
            except:
                log.warning("Column {} impossible to remove".format(col))

    def remove_nan(self):
        """
        Remove NaN in dataframe
        :return:
        """
        try:
            self.dataframe = self.dataframe.dropna(axis=0)
            log.debug('Remove Nan on data')
        except:
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

    def formatting(self, cp_format=False):
        """
        Format string into float
        :param cp_format: if cell profiler output, then apply a formatting of well
        :return:
        """

        def __cp_well_format(x):
            """
            format from F05 to F5
            """
            return re.sub('(0)(?<!$)', '', x)

        def __str_to_flt(x):
            return float(x)

        # # change , to . in float
        for chan in self.get_col():
            self.dataframe[chan].apply(__str_to_flt)
            if self.dataframe[chan].dtypes == 'object':
                self.dataframe[chan] = self.dataframe[chan].str.replace(",", ".")

        if cp_format:
            self.dataframe['Well'] = self.dataframe['Well'].apply(__cp_well_format())

    def write_raw_data(self, path, name, frmt='csv', **kwargs):
        """
        Write raw data into csv
        :param name: Name of file
        :param path: Directory where to save file
        :param frmt: format of data, csv by default
        """
        fname = os.path.join(path, name)
        if frmt is 'csv':
            fname += '.csv'
            self.dataframe.to_csv(fname, index=False, index_label=False)
            log.info("Write raw data %s" % fname)
        elif frmt is 'txt':
            fname += '.txt'
            self.dataframe.to_csv(fname, sep='\t', index=False, index_label=False, **kwargs)
            log.info("Write raw data %s" % fname)
        else:
            raise NotImplementedError('Format not supported for the moment')

    def df_to_array(self, channel, size=None):
        """
        Change shape in list from 1Data/well to numpy matrix
        :param channel: whiche channel to have in matrix format
        :param size: size/len of data 96 , 384 or 1526
        :return: numpy array
        """
        if self.is1Datawell:
            if self.dataframe is not None:
                if size is None:
                    size = len(self.dataframe)
                if size == 96:
                    array = np.zeros((8, 12))
                elif size == 384:
                    array = np.zeros((16, 24))
                else:
                    raise NotImplementedError('1526 not yet implemented')
                for i in range(size):
                    array[self.dataframe['Row'][i]][self.dataframe['Column'][i]] = self.dataframe[channel][i]
                return array
            else:
                raise Exception('Empty raw data')
        else:
            raise Exception('Not applicable on this data type')
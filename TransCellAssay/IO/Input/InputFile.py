# coding=utf-8
"""
Basic Class for manipulating data into dataframe
"""
import numpy as np
import pandas as pd
import os


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

DEBUG = 1


class InputFile(object):
    """
    InputFile is scaffold for CSV, Excel and txt data
    """

    def __init__(self):
        self.is1Datawell = False

    def load(self, fpath):
        """
        Load data
        :param fpath: File path
        """
        raise NotImplementedError

    def format_data(self):
        """
        Format data
        """
        self.dataframe = self.dataframe.replace({'Row': {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
                                                         8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
                                                         15: 'P'}})
        try:
            # # insert Well columns
            self.dataframe.insert(0, "Well", 0)
            # # put Well value from row and col columns
            self.dataframe['Well'] = self.dataframe.apply(lambda x: '%s%.3g' % (x['Row'], x['Column'] + 1), axis=1)
            remove = ['Row', 'Column']
            self.dataframe = self.dataframe.drop(remove, axis=1)
        except Exception as e:
            print(e)

    def get_col(self):
        """
        Get all Columns
        """
        return self.dataframe.columns()

    def remove_col(self):
        """
        Remove useless col
        """
        col_in_df = self.dataframe.columns
        # columns that we can remove because useless
        useless = [u'Barcode', u'PlateID', u'UPD', u'TimePoint', u'TimeInterval', u'FieldID', u'CellID',
                   u'Left', u'Top', u'Height', u'Width', u'FieldIndex', u'CellNum', "FieldNumber", "CellNumber", "X",
                   "Y", "Z", "Width", "Height", "PixelSizeX", "PixelSizeY", "PixelSizeZ", 'Status', 'Zposition',
                   'ValidObjectCount', 'PlateNumber']
        for col in useless:
            try:
                self.dataframe = self.dataframe.drop(col, axis=1)
            except:
                if col in col_in_df:
                    print("\033[0;33m[INFO/WARNING]\033[0m Column {} impossible to remove".format(col))

    def remove_nan(self):
        """
        Remove NaN in dataframe
        :return:
        """
        self.dataframe = self.dataframe.dropna(axis=0)

    def formatting(self):
        """
        Format string into float
        :return:
        """

        def str_to_flt(x):
            return float(x)

        # # change , to . in float
        for chan in self.get_col():
            self.dataframe[chan].apply(str_to_flt)
            if self.dataframe[chan].dtypes == 'object':
                self.dataframe[chan] = self.dataframe[chan].str.replace(",", ".")

    def write_raw_data(self, path, name, frmt='csv'):
        """
        Write raw data into csv
        :param name: Name of file
        :param path: Directory where to save file
        :param frmt: format of data, csv by default
        """
        try:
            fname = os.path.join(path, name)
            if frmt is 'csv':
                fname += '.csv'
                self.dataframe.to_csv(fname, index=False, index_label=False)
            else:
                raise NotImplementedError('Only csv for the moment')
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def df_to_array(self, channel, size=None):
        """
        Change shape in list from 1Data/well to numpy matrix
        :param channel: whiche channel to have in matrix format
        :param size: size/len of data 96 , 384 or 1526
        :return: numpy array
        """
        try:
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
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)
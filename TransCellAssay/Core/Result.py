# coding=utf-8
"""
Result is created for store result like score and hit resulting of SSMD or other technics in a tabe-like (numpy array),
channel are column and GeneName/Well are stored at the first col, each row represent a gene/well
We can save the tabe in csv by using pandas Dataframe.

This class store data with dict in input, where key are well and item are data.

"""

import numpy as np
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class Result(object):
    """
    Class for representing record array for result
    """

    def __init__(self, size=None):
        """
        Constructor
        if size is not given, init by 386 plate size, defined size if 96 or 1526 plate well
        :return: none init only dataframe
        """
        if size is None:
            size = 96
        self.values = np.zeros(size, dtype=[('GeneName', object), ('Well', object), ('CellsCount', float),
                                            ('SDCellsCount', float), ('PositiveCells', float),
                                            ('SDPositiveCells', float), ('Mean', float), ('Std', float),
                                            ('Median', float), ('Stdm', float), ('Viability', float),
                                            ('Toxicity', float)])

        self._genename_genepos = {}  # # To save GeneName (key)and  Gene position (value)
        self._genepos_genename = {}  # # To save Well (key) and Gene position (value)

    def get_result_array(self):
        """
        return data array
        :return: array
        """
        try:
            return self.values
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def init_gene_well(self, gene_list):
        """
        Add gene and well into the record Array in the first/second column
        :param gene_list: Dict with key are Well and Value are geneName
        :return:
        """
        try:
            i = 0
            for k, v in gene_list.items():
                self.values['GeneName'][i] = v
                self.values['Well'][i] = k
                self._genename_genepos.setdefault(v, []).append(i)  # # make this because Gene can be in multiple Well
                self._genepos_genename[k] = i
                i += 1
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def add_value(self, gene, channel, value):
        """
        Insert Value at Gene row and channel Col
        If GeneName is contain in multiple Well, it will be
        :param gene:
        :param channel:
        :param value:
        :return:
        """
        try:
            if len(self._genename_genepos[gene]) > 1:  # # loop in case geneName is in multiple Well
                for i in (self._genename_genepos[gene]):
                    self.values[channel][i] = value
            else:
                self.values[channel][self._genename_genepos[gene]] = value
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def add_data(self, datadict, channel, by='Pos'):
        """
        Insert Value from a dict where key = GeneName/pos and Value are value to insert
        Prefer by = pos in case of empty well
        :param datadict: dict that contain value to insert with key are GeneName or Pos/Well
        :param channel:
        :param by: insert by GeneName or Well
        :return:
        """
        try:
            for item, value in datadict.items():
                if by == 'GeneName':
                    print(" !! \033[0;33m[WARNING]\033[0m  !! add_data with by=GeneName is not fully stable in case "
                          "of empty Well \n Prefer by=Pos")
                    if len(self._genename_genepos[item]) > 1:
                        for i in (self._genename_genepos[item]):
                            self.values[channel][i] = value
                    else:
                        self.values[channel][self._genename_genepos[item]] = value
                elif by == 'Pos':
                    self.values[channel][self._genepos_genename[item]] = value
                else:
                    print("\033[0;31m[ERROR]\033[0m")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_result_column(self, col):
        """
        Get col/channel from result array
        :param col:
        :return: return numpy array
        """
        try:
            return self.values[col]
        except ValueError:
            print('\033[0;31m[ERROR]\033[0m  No Valid Column Name')

    def write(self, file_path, frmt='csv'):
        """
        Save Result Array into csv
        :param file_path:
        :param frmt: csv or xlsx format to save
        """
        try:
            if frmt is 'csv':
                pd.DataFrame(self.values).to_csv(file_path, index=False, header=True)
            elif frmt is 'xlsx':
                pd.DataFrame(self.values).to_excel(file_path, sheet_name='Single Cell properties result', index=False, header=True)
            print('\033[0;32m[INFO]\033[0m writing : {}'.format(file_path))
        except:
            try:
                if frmt is 'csv':
                    np.savetxt(fname=file_path, X=self.values, delimiter=';')
                    print('\033[0;32m[INFO]\033[0m writing : {}'.format(file_path))
                else:
                    raise IOError("Can't save data in xlsx format")
            except Exception as e:
                print('\033[0;31m[ERROR]\033[0m Error in saving results data :', e)

    def __add__(self, to_add):
        """
        add result object to other one MERGING Function
        :param to_add: other Result object
        :return:
        """
        try:
            if isinstance(to_add, np.ndarray):
                self.values = np.append(self.values, to_add, axis=0)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        try:
            return "Result of single Cell properties: \n" + repr(pd.DataFrame(self.values))
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        try:
            return self.__repr__()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

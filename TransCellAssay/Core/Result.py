# coding=utf-8
"""
Result is created for store result like score and hit resulting of SSMD or other technics in a tabe-like (numpy array),
feature are column and GeneName/Well are stored at the first col, each row represent a gene/well
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
            size = 384
        self.result_array = np.zeros(size, dtype=[('GeneName', object), ('Well', object), ('CellsCount', float),
                                                  ('SDCellsCount', float), ('PositiveCells', float),
                                                  ('SDPositiveCells', float),
                                                  ('Mean', float), ('Std', float), ('Median', float), ('Stdm', float),
                                                  ('Viability', float), ('Toxicity', float)])

        self.GenePos = {}  # # To save GeneName (key)and  Gene position (value)
        self.GenePosI = {}  # # To save Well (key) and Gene position (value)

    def get_result_array(self):
        """
        return data array
        :return: array
        """
        try:
            return self.result_array
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
                self.result_array['GeneName'][i] = v
                self.result_array['Well'][i] = k
                self.GenePos.setdefault(v, []).append(i)  # # make this form because Gene can be in multiple Well
                self.GenePosI[k] = i
                i += 1
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def add_value(self, gene, feature, value):
        """
        Insert Value at Gene row and Feature Col
        If GeneName is contain in multiple Well, it will be
        :param gene:
        :param feature:
        :param value:
        :return:
        """
        try:
            if len(self.GenePos[gene]) > 1:  # # loop in case geneName is in multiple Well
                for i in (self.GenePos[gene]):
                    self.result_array[feature][i] = value
            else:
                self.result_array[feature][self.GenePos[gene]] = value
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def add_data(self, datadict, feature, by='Pos'):
        """
        Insert Value from a dict where key = GeneName/pos and Value are value to insert
        Prefer by = pos in case of empty well
        :param datadict: dict that contain value to insert with key are GeneName or Pos/Well
        :param feature:
        :param by: insert by GeneName or Well
        :return:
        """
        try:
            for item, value in datadict.items():
                if by == 'GeneName':
                    print(" !! \033[0;33m[WARNING]\033[0m  !! add_data with by=GeneName is not fully stable in case "
                          "of empty Well \n Prefer by=Pos")
                    if len(self.GenePos[item]) > 1:
                        for i in (self.GenePos[item]):
                            self.result_array[feature][i] = value
                    else:
                        self.result_array[feature][self.GenePos[item]] = value
                elif by == 'Pos':
                    self.result_array[feature][self.GenePosI[item]] = value
                else:
                    print("\033[0;31m[ERROR]\033[0m")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_result_column(self, col):
        """
        Get col/feature from result array
        :param col:
        :return: return numpy array
        """
        try:
            return self.result_array[col]
        except ValueError:
            print('\033[0;31m[ERROR]\033[0m  No Valid Column Name')

    def write_csv(self, file_path):
        """
        Save Result Array into csv
        :param file_path:
        :return:
        """
        try:
            tmp = pd.DataFrame(self.result_array)
            tmp.to_csv(file_path, index=False)
        except:
            try:
                np.savetxt(file_path, self.result_array, delimiter=';')
            except Exception as e:
                print('\033[0;31m[ERROR]\033[0m  Error in saving results data', e)

    def __add__(self, to_add):
        """
        add result object to other one MERGING Function
        :param to_add: other Résult object
        :return:
        """
        try:
            if isinstance(to_add, np.ndarray):
                self.result_array = np.append(self.result_array, to_add, axis=0)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        try:
            return "Result object: " + repr(pd.DataFrame(self.result_array))
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        try:
            return "Result Array: \n " + repr(pd.DataFrame(self.result_array))
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

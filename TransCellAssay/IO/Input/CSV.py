# coding=utf-8
"""
Librarie for easy play with HTS csv data file (HCS explorer output style)
"""

import pandas as pd
from TransCellAssay.IO.Input.InputFile import InputFile

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class CSV(InputFile):
    """
    Class specifique for csv file
    """

    def __init__(self):
        super(CSV, self).__init__()

    def load(self, fpath):
        """
        Load csv file
        :param fpath:
        """
        try:
            self.dataframe = pd.read_csv(fpath, engine='c')
            print('\033[0;32m[INFO]\033[0m Reading %s File' % fpath)
        except:
            try:
                self.dataframe = pd.read_csv(fpath, decimal=",", sep=";", engine='c')
                print('\033[0;32m[INFO]\033[0m Reading %s File' % fpath)
            except Exception as e:
                print('\033[0;31m[ERROR]\033[0m  Error in reading %s File' % fpath, e)
# coding=utf-8
"""
Librarie for easy play with HTS txt data file (HCS explorer output style)
"""
from TransCellAssay.IO.Input.InputFile import InputFile
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class TXT(InputFile):
    """
    Class for load TXT file (similar to csv)
    """
    def __init__(self):
        super(TXT, self).__init__()

    def load(self, fpath):
        """
        Load csv file
        :param fpath:
        """
        try:
            self.dataframe = pd.read_table(fpath, engine='c')
            print('\033[0;32m[INFO]\033[0m Reading %s File' % fpath)
        except:
            try:
                self.dataframe = pd.read_table(fpath, decimal=",", engine='c')
                print('\033[0;32m[INFO]\033[0m Reading %s File' % fpath)
            except Exception as e:
                print('\033[0;31m[ERROR]\033[0m  Error in reading %s File' % fpath, e)

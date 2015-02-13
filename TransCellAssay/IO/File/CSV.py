# coding=utf-8
"""
Librarie for easy play with HTS csv data file (HCS explorer output style)
"""

import os
import pandas as pd
from TransCellAssay.IO.File.InputFile import InputFile

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
        if os.path.isfile(fpath):
            self.dataframe = pd.read_csv(fpath, engine='c')
            print('\033[0;32m[INFO]\033[0m Reading %s File' % fpath)
        else:
            raise IOError('File don\'t exist')
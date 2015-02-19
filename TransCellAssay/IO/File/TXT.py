# coding=utf-8
"""
Librarie for easy play with HTS txt data file (HCS explorer output style)
"""
import os
from TransCellAssay.IO.File.InputFile import InputFile
import pandas as pd
import logging
log = logging.getLogger(__name__)

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
        if os.path.isfile(fpath):
            self.dataframe = pd.read_table(fpath, engine='c')
            log.info('Reading %s File' % fpath)
        else:
            raise IOError('File don\'t exist')

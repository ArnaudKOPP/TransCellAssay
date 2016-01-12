# coding=utf-8
"""
Librarie for easy play with HTS txt data file
"""

import os
from TransCellAssay.IO.File.InputFile import InputFile
import pandas as pd
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class TXT(InputFile):
    """
    Class for load TXT file (similar to csv)
    """

    def __init__(self):
        super(TXT, self).__init__()

    def load(self, fpath, sep='\t', **kwargs):
        """
        Load csv file
        :param fpath:
        """
        if os.path.isfile(fpath):
            try:
                log.info('Reading %s File' % fpath)
                self.dataframe = pd.read_table(fpath, engine='c', **kwargs)
                log.info('Finish reading file')
                self.__filepath = fpath
            except Exception as e:
                log.error(e)
                pass
        else:
            msg = 'File don\'t exist'
            log.error(msg)
            raise IOError(msg)

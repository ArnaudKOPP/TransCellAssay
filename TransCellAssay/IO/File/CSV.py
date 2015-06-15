# coding=utf-8
"""
Librarie for easy play with HTS csv data file
"""

import os
import pandas as pd
from TransCellAssay.IO.File.InputFile import InputFile
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class CSV(InputFile):
    """
    Class specifique for csv file
    """

    def __init__(self):
        super(CSV, self).__init__()

    def load(self, fpath, sep=',', **kwargs):
        """
        Load csv file
        :param fpath:
        """
        if os.path.isfile(fpath):
            try:
                log.info('Reading %s File' % fpath)
                self.dataframe = pd.read_csv(fpath, engine='c', **kwargs)
                log.info('Finish reading file')
            except Exception as e:
                log.error(e)
                pass
        else:
            msg = 'File don\'t exist'
            log.error(msg)
            raise IOError(msg)

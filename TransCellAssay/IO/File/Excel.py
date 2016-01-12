# coding=utf-8
"""
Librarie for easy play with HTS excel data file (InCELL 1000)
"""
from TransCellAssay.IO.File.InputFile import InputFile
import os
import pandas as pd
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class EXCEL(InputFile):
    """
    Class for load excel file
    """
    def __init__(self):
        super(EXCEL, self).__init__()

    def load(self, fpath):
        # # obtention des noms de chaque sheet du excel
        """
        Load excel file
        :param fpath:
        """
        if os.path.isfile(fpath):
            xls = pd.ExcelFile(fpath)
            columns_name = xls.sheet_names
            measures = filter(lambda x: 'Cell measures' in x, columns_name)
            data = None
            compt = 0
            for i in measures:
                compt += 1
                print("sheet : %d" % compt)
                if data is None:
                    data = pd.read_excel(fpath, i)
                else:
                    data = data.append(pd.read_excel(fpath, i))
                data.fillna(0)
            self.dataframe = data
            log.info('Reading %s File' % fpath)
            self.dataframe["Well"] = self.dataframe["Well"].str.replace(' - ', '')
            self.dataframe["Well"] = self.dataframe["Well"].str.replace(r"\(.*\)", "")
        else:
            raise IOError('File don\'t exist')

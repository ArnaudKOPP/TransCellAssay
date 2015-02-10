# coding=utf-8
"""
Librarie for easy play with HTS excel data file (InCELL 1000)
"""
from TransCellAssay.IO.Input.InputFile import InputFile
import os
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


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
        else:
            raise IOError('File don\'t exist')
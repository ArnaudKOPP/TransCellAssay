# coding=utf-8
"""
Class for writing data of some well into a excel file
Save for defined reference (Genename/well) some stat like mean, median, std, sem
"""

import os
import xlsxwriter
import pandas as pd
import numpy as np
import TransCellAssay as TCA

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class ReferenceDataWriter(object):
    """
    Class for writing data of reference from plate into file
    """

    def __init__(self, path_file=None, file_name=None):
        try:
            self._excel_file = None
            self._excel_writer = None
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def save_reference(self, *args, ref=None, add_skipped=True, verbose=None):
        try:
            for arg in args:
                if isinstance(arg, list):
                    for elem in arg:
                        if isinstance(elem, TCA.Plate):
                            return 0
                        else:
                            raise TypeError('Put Plate into list')
                elif isinstance(arg, TCA.Plate):
                    return 0
                else:
                    raise TypeError('Take plate in input')
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def _get_plate_reference_data(self, plate, ref):
        try:
            return 0
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def _get_replicat_reference_data(self, replicat, ref):
        try:
            return 0
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)
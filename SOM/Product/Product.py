"""
Class for manipulating Product that are in Well
"""

import SOM
import pandas
import numpy

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "dev"


class Product():
    def __init__(self, Name, Plate):
        try:
            if isinstance(Plate, SOM.Plate):
                assert isinstance(Name, str)
                self.name = Name
                self.WellData = SOM.Product.WellData.__init__()
                self.position = None
                self.RefPlate = Plate
                self.Type = None
        except Exception as e:
            print(e)

    def _search_data_into_replicat(self):
        try:
            return 0
        except Exception as e:
            print(e)

    def _search_position(self):
        try:
            return 0
        except Exception as e:
            print(e)

    def __repr__(self):
        try:
            return 0
        except Exception as e:
            print(e)

    def __str__(self):
        try:
            return 0
        except Exception as e:
            print(e)
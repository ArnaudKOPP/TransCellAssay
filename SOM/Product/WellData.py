"""
Store Data replicat well
"""

import SOM
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = ""
__maintainer__ = ""
__email__ = ""
__status__ = ""


class WellData():
    def __init__(self):
        try:
            self.id = None
            self.data_serie = None
        except Exception as e:
            print(e)
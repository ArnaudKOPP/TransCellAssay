"""
Class derivated from ProductType
"""

import SOM

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = ""
__maintainer__ = ""
__email__ = ""
__status__ = ""


class siRNA(SOM.ProductType):
    def __init__(self):
        try:
            SOM.ProductType.__init__(self)
        except Exception as e:
            print(e)
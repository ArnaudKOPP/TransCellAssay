"""
Encore REST services
REST Documentation : https://www.encodeproject.org/help/rest-api/
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

from TransCellAssay.IO.Rest.Service import REST


class Encode(REST):
    """
    Class for doing REST requests to Encode
    """

    def __init__(self, verbose=False):
        super(Encode, self).__init__(name="Encode", url="https://www.encodeproject.org/", verbose=verbose)
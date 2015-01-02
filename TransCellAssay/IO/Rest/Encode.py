# coding=utf-8
"""
Encore REST services
REST Documentation : https://www.encodeproject.org/help/rest-api/
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
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
    # TODO finish this class
    def __init__(self, verbose=False):
        super(Encode, self).__init__(name="Encode", url="https://www.encodeproject.org/", verbose=verbose)
        # Force return from the server in JSON format
        self.HEADERS = {'accept': 'application/json'}

    def test(self):
        # This URL locates the ENCODE biosample with accession number ENCBS000AAA
        url = "biosample/ENCBS000AAA/?frame=object"

        # GET the object
        response = self.http_get(url, headers=self.HEADERS)
        return response
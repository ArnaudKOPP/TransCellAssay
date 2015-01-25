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
import json


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

    def biosample(self, accession_number):
        """
        Get biosample with accession number like ENCBS000AAA
        :param accession_number:
        :return: json object
        """
        url = "biosample/"+accession_number+"/?frame=object"
        response = self.http_get(url, headers=self.HEADERS)
        return response

    def response_keys(self, response, first_level=True):
        """
        Get all keys from response
        :param response: reponse object from request
        :param first_level: only first level or with sublevel
        :return: list of keys
        """
        if first_level:
            keys = response.keys()
        else:
            keys = [key for key, value in response.iteritems()]
        return keys

    def show_response(self, response):
        """
        Print the response in pretty format
        :param response:
        :return:
        """
        print(json.dumps(response, indent=4, separators=(',', ': ')))

    _valid_search_type = ['file', 'replicate', 'biosample']

    def search(self, searchterm=None, limit=False, format='json', full=False, embedded=False, data_type=None, md5=None, fastq_file=False, experiment_id=None, dataset=None):
        url = "search/"
        search = "?searchTerm="+str(searchterm)
        fastq = "&file_format=fastq"
        experiment = "&experiment=/experiments/"+experiment_id+"/"
        data_set = "&dataset==/experiments/"+dataset+"/"

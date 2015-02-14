# coding=utf-8
"""
http://togows.dbcls.jp/site/en/rest.html
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
import requests


class TogoWS(REST):
    """
    TogoWS rest service
    """

    def __init__(self, verbose=False):
        """
        **Constructor** TogoWS

        :param verbose: set to False to prevent informative messages
        """
        super(TogoWS, self).__init__(name="TogoWS", url="http://togows.dbcls.jp", verbose=verbose)
        try:
            self.valid_entry_db = requests.get("http://togows.dbcls.jp/entry/").text.replace('\n', '\t').split('\t')
            self.valid_search_db = requests.get("http://togows.dbcls.jp/search/").text.replace('\n', '\t').split('\t')
            self.valid_conv_src = requests.get("http://togows.dbcls.jp/convert/").text.replace('\n', '\t').split('\t')
        except:
            pass

    def EntryRetrieval(self):
        raise NotImplementedError

    def DatabaseSearch(self):
        raise NotImplementedError

    def DataFormatConversion(self):
        raise NotImplementedError
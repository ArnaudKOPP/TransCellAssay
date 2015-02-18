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
import logging
log = logging.getLogger(__name__)


class TogoWS(REST):
    """
    TogoWS rest service
    """

    def __init__(self):
        """
        **Constructor** TogoWS

        :param verbose: set to False to prevent informative messages
        """
        super(TogoWS, self).__init__(name="TogoWS", url="http://togows.dbcls.jp")
        try:
            self.valid_entry_db = requests.get("http://togows.dbcls.jp/entry/").text.replace('\n', '\t').split('\t')
            self.valid_search_db = requests.get("http://togows.dbcls.jp/search/").text.replace('\n', '\t').split('\t')
            self.valid_conv_src = requests.get("http://togows.dbcls.jp/convert/").text.replace('\n', '\t').split('\t')
        except:
            pass

    @staticmethod
    def EntryDBField(db):
        """
        Search Fields for specified database
        :param db: entry database
        :return: list of fields
        """
        flds = requests.get("http://togows.dbcls.jp/entry/"+str(db)+"?fields").text.replace('\n', '\t').split('\t')
        return flds

    @staticmethod
    def EntryDBFormat(db):
        """
        Search format for specified database
        :param db: entry database
        :return: list of format
        """
        frmt = requests.get("http://togows.dbcls.jp/entry/"+str(db)+"?formats").text.replace('\n', '\t').split('\t')
        return frmt

    def EntryRetrieval(self, database, query, field=None, format=None):
        if database not in self.valid_entry_db:
            raise ValueError('Not valid Database')

        query = "entry/"+str(database)+"/"+str(query)

        if field is not None:
            query += "/"+str(field)

        if format is not None:
            query += "."+str(format)

        res = self.http_get(query, frmt='txt')
        return res

    def DatabaseSearch(self, database, query):
        """
        Search on multiple databse
        :param database: database to seach
        :param query: word for search
        :return:
        """
        if database not in self.valid_search_db:
            raise ValueError('Not valid Database')

        query = "search/"+str(database)+"/"+str(query)

        res = self.http_get(query, frmt='txt')
        return res

    def DataFormatConversion(self):
        raise NotImplementedError
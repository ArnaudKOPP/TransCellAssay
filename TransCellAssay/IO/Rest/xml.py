"""
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import xml.etree.ElementTree as ET
import bs4
from urllib.request import urlopen


__all__ = ["easyXML", "readXML"]


class easyXML(object):
    """
    class to ease the introspection of XML documents.
    This class uses the standard xml module as well as the package BeautifulSoup
    to help introspecting the XML documents.
    """

    def __init__(self, data, encoding="utf-8"):
        """
        :param data: an XML document format
        :param fixing_unicode: use only with HGNC service to fix issue with the
            XML returned by that particular service. No need to use otherwise.
            See :class:`~bioservices.hgnc.HGNC` documentation for details.
        :param encoding: default is utf-8 used. Used to fix the HGNC XML only.


        The data parameter must be a string containing the XML document. If you
        have an URL instead, use :class:`readXML`

        """
        # if fixing_unicode:
        #    x = unicodefix.FixingUnicode(data, verbose=False, encoding=encoding)
        #    self.data = x.fixed_string.encode("utf-8")
        #else:
        self.data = data[:]

        try:
            self.root = ET.fromstring(self.data)
        except:
            self.root = self.data[:]
        self._soup = None
        self.prettify = self.soup.prettify
        self.findAll = self.soup.findAll

    def getchildren(self):
        """
        returns all children of the root XML document
        This is just an alias to self.soup.getchildren()
        """
        return self.root.getchildren()

    def _get_soup(self):
        if self._soup is None:
            self._soup = bs4.BeautifulSoup(self.data)
        return self._soup

    soup = property(_get_soup, doc="Returns the beautiful soup instance")

    def __str__(self):
        txt = self.soup.prettify()
        return txt

    def __getitem__(self, i):
        return self.findAll(i)


class readXML(easyXML):
    """
    Read XML and converts to beautifulsoup data structure
    easyXML accepts as input a string. This class accepts a filename instead
    inherits from easyXML
    """

    def __init__(self, filename, fixing_unicode=False, encoding="utf-8"):
        url = urlopen(filename, "r")
        self.data = url.read()
        super(readXML, self).__init__(self.data, fixing_unicode, encoding)
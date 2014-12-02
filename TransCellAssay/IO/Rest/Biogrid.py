"""
This module provides a class :class:`~BioGrid`.

.. topic:: What is BioGrid ?

    :URL: http://thebiogrid.org/
    :Service: Via the PSICQUIC class

    .. highlights::

        BioGRID is an online interaction repository with data compiled through
        comprehensive curation efforts. Our current index is version 3.2.97 and searches
        37,954 publications for 638,453 raw protein and genetic interactions from major
        model organism species. All interaction data are freely provided through our
        search index and available via download in a wide variety of standardized
        formats.

        -- From BioGrid website, Feb. 2013

"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

from TransCellAssay.IO.Rest.Psicquic import PSICQUIC
import re

__all__ = ["BioGRID"]


class Search(PSICQUIC):
    """
    Class that carries out the actual search via psicquic.

    .. todo:: to be removed
    """

    def __init__(self, data, verbose=False):
        super(Search, self).__init__(verbose=verbose)
        self.data = data
        if "biogrid" in self.activeDBs:
            self.output = self.query("biogrid", self.data)
        else:
            print("\033[0;33m[WARNING]\033[0m BioGrid is not active")
            self.output = []
        self.interactors = self.get_interactors()

    def get_interactors(self):
        out = []
        for element in self.output:
            x = (re.sub(".*:", "", element[2:4][0]), re.sub(".*:", "", element[2:4][1]))
            out.append(tuple(sorted(x)))
        return list(set(out))


class BioGRID(object):
    """
    Interface to BioGRID.
    """

    def __init__(self, query=None, taxId=None, exP=None):

        self.query = query
        self.taxId = taxId
        self.exP = exP
        self.searchString = self._biogridSearch()
        self.biogrid = Search(self.searchString)

    def _biogridSearch(self, query=None, taxid=None, exp=None):
        """
        Creates a search string for the biogrid database.

        :param str query: the gene name(s). Can be a string or a list of strings.
        :param str taxid: the taxid for the organism of relevance. If None,
            all organisms are choosen.
        :param str exp: the experimental protocol used to identify the interactions.
        :return: a search string for biogrid.
        """

        if query is None:
            query = self.query
        if taxid is None:
            taxid = self.taxId
        if exp is None:
            exp = self.exP

        asepNone = "%20AND%20None"
        if exp is not None:
            exp = exp.replace(" ", asepNone[:-4])
        if isinstance(query, str):
            conStr = "%s%s" % (query, asepNone)
        else:
            conStr = "%s" % ("%20OR%20".join(query))
        if taxid is not None or exp is not None:
            if isinstance(query, list):
                conStr = "(%s)" % conStr
        conStr = "%s%s%s%s%s" % (conStr, asepNone[:-4], taxid, asepNone[:-4], exp)
        conStr = conStr.replace(asepNone, "")
        return conStr


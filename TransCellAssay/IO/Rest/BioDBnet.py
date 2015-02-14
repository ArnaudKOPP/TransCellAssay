# coding=utf-8
"""
http://biodbnet.abcc.ncifcrf.gov/webServices/RestWebService.php
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


class BioDBnet(REST):
    """
    BioDBnet rest service
    """

    def __init__(self, verbose=False):
        """
        **Constructor** bioDbnet

        :param verbose: set to False to prevent informative messages
        """
        super(BioDBnet, self).__init__(name="BioDBnet",
                                       url="http://biodbnet.abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi",
                                       verbose=verbose)

    def getInputs(self):
        raise NotImplementedError

    def getOutputsForInput(self):
        raise NotImplementedError

    def getDirectOutptsForInput(self):
        raise NotImplementedError

    def getPathways(self):
        raise NotImplementedError

    def db2db(self):
        raise NotImplementedError

    def dbReport(self):
        raise NotImplementedError

    def dbWalk(self):
        raise NotImplementedError

    def dbFind(self):
        raise NotImplementedError

    def dbOrtho(self):
        raise NotImplementedError

    def dbAnnot(self):
        raise NotImplementedError
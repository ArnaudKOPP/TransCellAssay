"""
Panther interface using REST
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


class Panther(REST):
    """
    interface to panther web services
    """
    _url = "http://www.pantherdb.org/"

    def __init__(self, verbose=True):
        """

        :param verbose:
        :return:
        """
        super(Panther, self).__init__(name="Panter", url=Panther._url, verbose=verbose)

        self._allPathWaysURL = "http://www.pantherdb.org/pathway/pathwayList.jsp"

    def get_pathways_names(self, startwith=""):
        """
        return pathways from biocarta
        all human and mouse, can perform a selection
        :param startwith:
        :return:
        """
        raise NotImplementedError
        allx = readXML(self._allPathwaysURL)
        pathways = [this.get("href") for this in allx.findAll("a") if "pathfiles" in this.get("href")]
        pathways = [str(x.split("/")[-1]) for x in pathways]  # split the drive
        pathways = sorted(list(set(pathways)))
        pathways = [x for x in pathways if x.startswith(startswith)]
        return pathways

    def get_biopax_pathways(self, name):
        """

        :param name:
        :return:
        """
        raise NotImplementedError
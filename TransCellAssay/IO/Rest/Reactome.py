"""
Reactome interface using REST
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import logging

from TransCellAssay.IO.Rest.Service import REST
from TransCellAssay.IO.Rest.misc import list2string, check_param_in_list


__all__ = ["Reactome"]


class Reactome(REST):
    """
    Reactome interface
    """

    _url = "http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/RESTfulWS"

    def __init__(self, verbose=True):
        super(Reactome, self).__init__("Reactome(URL)", url=Reactome._url, verbose="ERROR")
        self.debugLevel = verbose

        # buffer
        self._list_pathways = None

    def _download_list_pathways(self):
        if self._list_pathways is None:
            res = self.session.get("http://www.reactome.org/download/current/ReactomePathways.txt")
            if res.status_code == 200:
                res = res.text
                res = res.strip()
                self._list_pathways = [x.split("\t") for x in res.split("\n")]
            else:
                print("\033[0;31m[ERROR]\033[0m could not fetch the pathways")
                raise IOError
        return self._list_pathways

    def get_list_pathways(self):
        res = self._download_list_pathways()
        return res

    def biopax_exporter(self, identifier, level=2):
        res = self.http_get("biopaxExporter/Level{0}/{1}".format(level, identifier), frmt=None)
        return res

    def front_page_items(self, species):
        species = species.replace("+", " ")
        res = self.http_get("frontPageItems/{0}".format(species), frmt="json")
        return res

    def highlight_pathway_diagram(self, identifier, genes, frmt="PNG"):
        check_param_in_list(frmt, ['PDF', 'PNG'])
        url = "highlightPathwayDiagram/{0}/{1}"
        genes = list2string(genes)
        res = self.http_post(url.format(identifier, frmt), frmt="txt", data=genes)
        return res

    def list_by_query(self, classname, **kargs):
        url = "listByQuery/{0}".format(classname)
        # NOTE: without the content-type this request fails with error 415
        # fixed by
        res = self.http_post(url, frmt='json', data=kargs,
                             headers={'Content-Type': "application/json;odata=verbose"})
        return res

    def pathway_diagram(self, identifier, frmt="PNG"):
        check_param_in_list(frmt, ['PDF', 'PNG', 'XML'])
        url = 'pathwayDiagram/{0}/{1}'.format(identifier, frmt)
        res = self.http_get(url, frmt=frmt)
        return res

    def pathway_hierarchy(self, species):
        species = species.replace("+", " ")
        res = self.http_get("pathwayHierarchy/{0}".format(species), frmt="xml")
        return res

    def pathway_participantes(self, identifier):
        res = self.http_get("pathwayParticipants/{0}".format(identifier), frmt='json')
        return res

    def pathway_complexes(self, identifier):
        res = self.http_get("pathwayComplexes/{0}".format(identifier), frmt="json")
        return res

    def query_by_id(self, classname, identifier):
        url = "queryById/{0}/{1}".format(classname, identifier)
        res = self.http_get(url, frmt='json')
        return res

    def query_by_ids(self, classname, identifiers):
        identifiers = list2string(identifiers)
        url = "queryByIds/{0}".format(classname)
        res = self.http_post(url, frmt="json", data=identifiers)
        # headers={'Content-Type': "application/json"})
        return res

    def query_hit_pathways(self, query):
        identifiers = list2string(query)
        res = self.http_post("queryHitPathways", frmt='json', data=identifiers)
        return res

    def query_pathway_for_entities(self, identifiers):
        identifiers = list2string(identifiers, space=False)
        url = "pathwayForEntities"
        res = self.http_post(url, frmt='json', data={'ID': identifiers})
        return res

    def species_list(self):
        url = "speciesList"
        res = self.http_get(url, frmt='json')
        return res

    def SMBL_exporter(self, identifier):
        url = "smblExproter/{0}".format(identifier)
        res = self.http_get(url, frmt='xml')
        return res


class ReactomeAnalysis(REST):
    _url = "http://www.reactome.org:80/AnalysisService"
    # "identifiers/projection?pageSize=8000&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL",
    def __init__(self, verbose=True, cache=False):
        super(ReactomeAnalysis, self).__init__("Reactome(URL)", url=ReactomeAnalysis._url, verbose=verbose, cache=False)
        logging.warning(
            "Class in development. Some methods are already working but those required POST do not. Coming soon ")

    def identifiers(self, genes):
        """
        s.identfiers("TP53")
        .. warning:: works for oe gene only for now
        """
        url = "identifiers/projection?pageSize=8000&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL"
        genes = list2string(genes)
        genes = genes.replace(" ", "")
        print(genes)
        res = self.http_post(url, frmt="json", data=genes,
                             headers={"Content-Type": "text/plain;charset=UTF-8",
                                      "Accept": "application/json"})
        return res


"""
class ReactomePathway(object):

    def __init__(self, entry):
        self.raw_data = copy.deepcopy(entry)
        # just adding the attributes to make life easier
        for k in self.raw_data._keyord:
            setattr(self, k, getattr(self.raw_data, k))

    def __str__(self):

        txt = "id: " + str(self.id)
        txt += "\nname: " + str(self.name)

        txt += "\nhasComponent:"
        if self.hasComponent:
            txt += str(len(self.hasComponent))

        if self.raw_data.compartment:
            txt += "\ncompartment:" + str(len(self.raw_data.compartment))
        else:
            txt += "\ncompartment: " + str(self.raw_data.compartment)

        txt += "\nliteratureReference:"
        this = self.raw_data.literatureReference
        if this:
            for i,x in enumerate(this):
                txt += " --- %s: %s %s\n" % (i, x.id, x.name)

        txt += "\nspecies:"
        this = self.raw_data.species
        if this:
            txt += "  %s (%s)" % (this.scientificName, this.id)

        txt += "\nsummation:"
        this = self.raw_data.summation
        if this:
            for x in this:
                txt += " - %s \n" % (self.raw_data.id)

        txt += "\ngoBiologicalProcess:"
        this = self.raw_data.goBiologicalProcess
        if this: txt += "\n - %s %s\n" % (this.id, this.name)

        txt += "\ninferredFrom:" + str(self.raw_data.inferredFrom)
        txt += "\northologousEvent: "
        this = self.raw_data.orthologousEvent
        if this:
            txt += str(len(this))

        txt += "\nprecedingEvent: " + str(self.raw_data.precedingEvent)
        txt += "\nevidence Type: " + str(self.raw_data.evidenceType) + "\n"

        return txt
"""
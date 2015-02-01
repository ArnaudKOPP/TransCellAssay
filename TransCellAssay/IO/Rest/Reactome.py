# coding=utf-8
"""
Reactome interface using REST
REACTOME is an open-source, open access, manually curated and peer-reviewed
pathway database. Pathway annotations are authored by expert biologists, in
collaboration with Reactome editorial staff and cross-referenced to many
bioinformatics databases. These include NCBI Entrez Gene, Ensembl and UniProt
databases, the UCSC and HapMap Genome Browsers, the KEGG Compound and ChEBI
small molecule databases, PubMed, and Gene Ontology
URL: http://www.reactome.org/ReactomeGWT/entrypoint.html
REST: http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/ReactomeRESTFulAPI.html
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

from TransCellAssay.IO.Rest.Service import REST, list2string, check_param_in_list


__all__ = ["Reactome"]


class Reactome(REST):
    """
    Reactome interface
    """

    _url = "http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/RESTfulWS"

    def __init__(self, verbose=True):
        super(Reactome, self).__init__("Reactome(URL)", url=Reactome._url, verbose="ERROR")
        self.debugLevel = verbose
        self._verbose = verbose
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
        """
        Return list of pathways from reactome website
        """
        res = self._download_list_pathways()
        return res

    def get_species(self):
        """
        Return list of species from all pathways
        """
        res = self._download_list_pathways()
        res = set([x[2] for x in self.get_list_pathways()])
        return res

    def biopax_exporter(self, identifier, level=2):
        """
        Get BioPAX file
        The passed identifier has to be a valid evend identifier. If there is no matching ID in the database,it will
        return an empty string

        s = Reactome()
        res = s.biopax_exporter(109581)
        """
        res = self.http_get("biopaxExporter/Level{0}/{1}".format(level, identifier), frmt=None)
        return res

    def front_page_items(self, species):
        """
        Get list of front page items listed in the Reactome Pathways Browser

        s = Reactome()
        res = s.front_page_items("homo sapiens")

        Pathway Browser <http://www.reactome.org/PathwayBrowser/>
        """
        species = species.replace("+", " ")
        res = self.http_get("frontPageItems/{0}".format(species), frmt="json")
        return res

    def highlight_pathway_diagram(self, identifier, genes, frmt="PNG"):
        """
        Highlight a diagram for a specified pathways based on its identifier
        """
        check_param_in_list(frmt, ['PDF', 'PNG'])
        url = "highlightPathwayDiagram/{0}/{1}"
        genes = list2string(genes)
        res = self.http_post(url.format(identifier, frmt), frmt="txt", data=genes)
        return res

    def list_by_query(self, classname, **kargs):
        """
        Get list of objects from Reactome database
        To query a list of pathways with names as 'Apoptosis'

        s = Reactome()
        res = list_by_query("Pathway", name='Apoptosis')
        identifiers = [x['dbId'] for x in res]
        """
        url = "listByQuery/{0}".format(classname)
        # NOTE: without the content-type this request fails with error 415
        # fixed by
        res = self.http_post(url, frmt='json', data=kargs, headers={'Content-Type': "application/json;odata=verbose"})
        return res

    def pathway_diagram(self, identifier, frmt="PNG"):
        """
        Retrieve pathway diagram

        s = Reactome()
        s.pathway_diagram('109581', 'PNG', view=True)
        s.pathway_diagram('109584', 'PNG', save=True)

        if PNG or PDF, the output is base64 but there is no facility to easily save the results in a file for now
        """
        check_param_in_list(frmt, ['PDF', 'PNG', 'XML'])
        url = 'pathwayDiagram/{0}/{1}'.format(identifier, frmt)
        res = self.http_get(url, frmt=frmt)
        return res

    def pathway_hierarchy(self, species):
        """
        Get the pathways hierarchy for a species as displayed in Reactome pathway browser

        s = Reactome()
        s.pathway_hierarchy("homo sapiens")
        """
        species = species.replace("+", " ")
        res = self.http_get("pathwayHierarchy/{0}".format(species), frmt="xml")
        return res

    def pathway_participantes(self, identifier):
        """
        Get list of pathway participants for a pathway

        s = Reactome()
        s.pathway_participantes(109581)
        """
        res = self.http_get("pathwayParticipants/{0}".format(identifier), frmt='json')
        return res

    def pathway_complexes(self, identifier):
        """
        Get complexes belonging to a patway

        s = Reactome()
        s.pathway_complexes(109581)
        """
        res = self.http_get("pathwayComplexes/{0}".format(identifier), frmt="json")
        return res

    def query_by_id(self, classname, identifier):
        """
        Get Reactome Database for a specific object

        s = Reactome()
        s.query_by_id("Pathway", "109581")
        """
        url = "queryById/{0}/{1}".format(classname, identifier)
        res = self.http_get(url, frmt='json')
        return res

    def query_by_ids(self, classname, identifiers):
        """
        Get Reactome Database for a specific object

        s = Reactome()
        s.query_by_ids("Pathway", "CDC2")

        not sure if wrapping is correct
        """
        identifiers = list2string(identifiers)
        url = "queryByIds/{0}".format(classname)
        res = self.http_post(url, frmt="json", data=identifiers)
        # headers={'Content-Type': "application/json"})
        return res

    def query_hit_pathways(self, query):
        """
        Get pathways that contain one or more genes passed in the query list.
        In the Reactome data model, pathways are organized in a
        hierarchical structure. The returned pathways in this method are pathways
        having detailed manually drawn pathway diagrams. Currently only human
        pathways will be returned from this method.

        s.query_hit_pathways('CDC2')
        s.query_hit_pathways(['CDC2'])
        """
        identifiers = list2string(query)
        res = self.http_post("queryHitPathways", frmt='json', data=identifiers)
        return res

    def query_pathway_for_entities(self, identifiers):
        """
        Get pathway objects by specifying an array of PhysicalEntity database identifiers.
        The returned Pathways should
        contain the passed EventEntity objects. All passed EventEntity database
        identifiers should be in the database.
        """
        identifiers = list2string(identifiers, space=False)
        url = "pathwayForEntities"
        res = self.http_post(url, frmt='json', data={'ID': identifiers})
        return res

    def species_list(self):
        """
        Get the list of species used in the Swithc Species box in Reactome pathway browser
        """
        url = "speciesList"
        res = self.http_get(url, frmt='json')
        return res

    def SBML_exporter(self, identifier):
        """
        Get the SBML XML text of a pathway identifier

        s = Reactome()
        xml = s.SBML_exporter(109581)
        """
        url = "sbmlExporter/{0}".format(identifier)
        res = self.http_get(url, frmt='xml')
        return res


class ReactomeAnalysis(REST):
    _url = "http://www.reactome.org:80/AnalysisService"
    # "identifiers/projection?pageSize=8000&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL",

    def __init__(self, verbose=True, cache=False):
        super(ReactomeAnalysis, self).__init__("Reactome(URL)", url=ReactomeAnalysis._url, verbose=verbose)
        print("\033[0;33m[WARNING]\033[0m Class in development. Some methods are already working but those required "
              "POST do not. Coming soon ")

    def identifiers(self, genes):
        """
        s.identfiers("TP53")
        .. warning:: works for oe gene only for now
        """
        url = "identifiers/projection?pageSize=8000&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL"
        genes = list2string(genes)
        genes = genes.replace(" ", "")
        print(genes)
        res = self.http_post(url, frmt="json", data=genes, headers={"Content-Type": "text/plain;charset=UTF-8",
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
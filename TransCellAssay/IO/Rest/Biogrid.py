# coding=utf-8
"""
This module provides a class :class:`~BioGrid`.

.. topic:: What is BioGrid ?

    :URL: http://thebiogrid.org/
    :REST: http://wiki.thebiogrid.org/doku.php/biogridrest

    .. highlights::

        BioGRID is an online interaction repository with data compiled through
        comprehensive curation efforts. Our current index is version 3.2.97 and searches
        37,954 publications for 638,453 raw protein and genetic interactions from major
        model organism species. All interaction data are freely provided through our
        search index and available via download in a wide variety of standardized
        formats.

        -- From BioGrid website, Feb. 2013

http://webservice.thebiogrid.org/interactions/?pubmedList=18316726|17662948&accessKey=dc589cabccb374194e060d3586b31349

http://webservice.thebiogrid.org/version/?accessKey=dc589cabccb374194e060d3586b31349

http://webservice.thebiogrid.org/interactions/?geneList=31623&searchbiogridids=true&includeInteractors=true&accessKey=dc589cabccb374194e060d3586b31349

http://webservice.thebiogrid.org/interaction/102009/?format=json&accessKey=dc589cabccb374194e060d3586b31349

http://webservice.thebiogrid.org/interactions/?additionalIdentifierTypes=ENTREZ_GENE&evidenceList=Affinity Capture-MS&includeEvidence=true&geneList=851076|853506&accessKey=dc589cabccb374194e060d3586b31349

=====================================================================================================================================
Parameter	                    Type	    Default	    Valid Values	                                                Description
=====================================================================================================================================
accessKey	                    string	    NONE	    Only 32 character Alphanumeric strings	                        All rest access must supply a valid accessKey to prevent spamming of the service. Access Keys are free and openly available here.
start	                        int	        0       	0-2147483647	                                                Query results are numbered from 0. Results fetched will start at this value e.g. start = 50 will skip the the first 50 results. Ignored if using “count” in the format parameter.
max	                            int	        10000	    1-10000	                                                        Number of results to fetch; this will be ignored if greater than 10,000, i.e. pagination using several requests is required to retrieve more than 10,000 interactions. Ignored if using “count” in the format parameter.
interSpeciesExcluded	        boolean	    FALSE	    true, false	                                                    If ‘true’, interactions with interactors from different species will be excluded.
selfInteractionsExcluded	    boolean	    FALSE	    true, false	                                                    If ‘true’, interactions with one interactor will be excluded.
evidenceList	                string	    empty	    Pipe-separated list of evidence codes  	                        Any interaction evidence with its Experimental System in the list will be excluded from the results unless includeEvidence is set to true.
includeEvidence	                boolean	    FALSE	    true, false	                                                    If set to true, any interaction evidence with its Experimental System in the evidenceList will be included in the result
geneList	                    string	    empty	    Pipe-separated list of gene names or identifiers.	            Interactions between genes in this list will be fetched. This parameter is ignored if one of searchIds, searchNames, searchSynonyms is not ‘true’ and additionalIdentifierTypes is empty.
searchIds	                    boolean	    FALSE	    true, false	                                                    If ‘true’, the interactor ENTREZ_GENE and SYSTEMATIC_NAME (orf) will be examined for a match with the geneList .
searchNames	                    boolean	    FALSE	    true, false	                                                    If ‘true’, the interactor OFFICIAL_SYMBOL will be examined for a match with the geneList.
searchSynonyms	                boolean	    FALSE	    true, false	                                                    If ‘true’, the interactor SYNONYM will be examined for a match with the geneList.
searchBiogridIds	            boolean	    FALSE	    true, false	                                                    If ‘true’, the entries in 'GENELIST' will be compared to BIOGRID internal IDS which are provided in all Tab2 formatted files.
additionalIdentifierTypes	    string	    empty	    Pipe-separated list of identifier types 	                    Identifier types on this list are examined for a match with the geneList.
excludeGenes	                boolean	    FALSE	    true, false	                                                    If ‘true’, interactions containing genes in the geneList will be excluded from the results. Ignored if one of searchIds, searchNames, searchSynonyms is not ‘true’ and additionalIdentifierTypes is empty.
includeInteractors	            boolean	    TRUE	    true, false	                                                    If ‘true’, in addition to interactions between genes on the geneList, interactions will also be fetched which have only one interactor on the geneList i.e. the geneList’s first order interactors will be included
includeInteractorInteractions	boolean	    FALSE	    true, false	                                                    If ‘true’ interactions between the geneList’s first order interactors will be included. Ignored if includeInteractors is ‘false’ or if excludeGenes is set to ‘true’.
pubmedList	                    string	    empty       string	Pipe-separated list of pubmed IDs	                    Interactions will be fetched whose Pubmed Id is/ is not in this list, depending on the value of excludePubmeds.
excludePubmeds	                boolean	    FALSE	    true, false	                                                    If ‘false’, interactions with Pubmed ID in pubmedList will be included in the results; if ‘true’ they will be excluded.
htpThreshold	                int	        2147483647 (maximum 32-bit integer)	0-2147483647	                        Interactions whose Pubmed ID has more than this number of interactions will be excluded from the results. Ignored if excludePubmeds is ‘false’.
throughputTag	                string	    “any”	    “any”,”low”,”high”	                                            If set to 'low or 'high', only interactions with 'Low throughput' or 'High throughput' in the 'throughput' field will be returned. Interactions with both 'Low throughput' and 'High throughput' will be returned by either value.
taxId	                        string	    “All”	    Any NCBI taxonomy identifier or “All”	                        Only genes from this organism will be searched with reference to gene identifiers or names.
includeHeader	                boolean	    FALSE	    true, false	                                                    If ‘true’, the first line of the result will be a BioGRID column header, appropriate for the format parameter (‘count’ format has no header).
format	                        string	    “tab2”	    “tab1”,”tab2,”extendedTab2”,”count”, “json”, “jsonExtended”	    ‘tab1’ and ‘tab2’ will return data in .tab or .tab2 format respectively. 'json' will return data in json a json formatted object. ‘extendedTab2’ and 'jsonExtended' will return data in .tab2 and json file formats respectively with extra fields for “Source Database Identifiers”, “Number of Interactions per Publication” and “Additional Identifiers”. For more information on file formats, visit our file format listing.
translate	                    boolean	    FALSE	    true,false	                                                    If 'true', the rest service will show a small snippet above your results detailing how your input parameters were translated for use in returning your data. This is helpful in troubleshooting why you may or may not be getting back the results expected. For example, if you enter a typo for a field such as “searchNamez”, no result will be translated, and thus this parameter will be ignored.


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
import webbrowser
import pandas as pd
from io import StringIO


class Biogrid(REST):
    """
    Interface to the biogrid REST api
    """
    _valid_parameters = [x.lower() for x in ["start", "max", "interSpeciesExcluded", "selfInteractionsExcluded",
                                             "evidenceList", "includeEvidence", "geneList", "searchIds",
                                             "searchSynonyms", "searchBiogridIds", "additionalIdentifierTypes",
                                             "excludeGenes", "includeInteractors", "includeInteractorInteractions",
                                             "pubmedList", "excludePubmeds", "htpThreshold", "throughputTag", "taxId",
                                             "includeHeader", "translate"]]

    def __init__(self, accesKey="dc589cabccb374194e060d3586b31349", verbose=False):
        super(Biogrid, self).__init__(name="Biogrid", url="http://webservice.thebiogrid.org", verbose=verbose)
        self.AccesKey = accesKey
        self.SupportedOrganismId = self._supported_organism_list(json=True)

    def interaction(self, **kwargs):
        """
        Parse request
        :param kwargs:
        :return:
        """
        query = "interactions/?"
        if kwargs is not None:
            for key, value in kwargs.items():
                if key.lower() in self._valid_parameters:
                    query += key + "=" + value + "&"
                else:
                    print("\033[0;33m[WARNING]\033[0m %s is not a valid paramenters" % key)
        query += self._add_acces_key()
        res = self.http_get(query)
        return res

    def get_biogrid_version(self):
        """
        Get the biogrid Version
        :return:
        """
        query = "version/?" + self._add_acces_key()
        res = self.http_get(query, frmt='xml')
        return res

    def _add_acces_key(self):
        """
        Generate acces Key for url
        :return:
        """
        return "accesskey=%s" % self.AccesKey

    def _supported_organism_list(self, json=False):
        """
        Get list of organism id and names supported by the REST taxId option
        :return:
        """
        query = "organisms/?" + self._add_acces_key()
        if json:
            query += "&format=json"
            res = self.http_get(query, frmt='json')
            return res
        res = self.http_get(query)
        return res

    def open_documentation(self):
        """
        Open a brower tab with documentation for filling requests
        """
        tab = webbrowser.open("http://wiki.thebiogrid.org/doku.php/biogridrest")
        return tab


class BiogridParser():
    """
    Class for parsing result from Biogrid requests

    Documentation
    http://wiki.thebiogrid.org/doku.php/biogrid_tab_version_2.0
    """

    def __int__(self, res):
        """
        Constructor
        """
        self.Data = pd.read_table(StringIO(res), header=None)
        self.Data.columns = ['Biogrid Interaction ID', "Entrez Gene Id A", "Entrez Gene Id B", "Biogrid Id A",
                             "Biogrid Id B", "A", "B", "A Off", "B Off", "A Syn", "B Syn", "Experimental System Name",
                             "Experimental System Type", "Author", "Pubmed Id", "NCBI Tax Id A", "NCBI Tax Id B",
                             "Interaction Throughput", "Quantitative Score", "Post Translational Modification",
                             "Phenotypes", "Qualifications", "Tags", "Source Database"]
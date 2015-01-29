# coding=utf-8
"""
String-db REST services
Website : www.http://string-db.org
REST Documentation : http://string-db.org/help/index.jsp?topic=/org.string-db.docs/api.html
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


class String(REST):
    """
    Class for doing REST requests to String-db
    """
    # TODO finish this class

    def __init__(self, verbose=False, alt=False, stitch=False):
        self._verbose = verbose
        if alt:
            super(String, self).__init__(name="String", url="string.embl.de", verbose=verbose)
        if stitch:
            super(String, self).__init__(name="String", url="stitch.embl.de", verbose=verbose)
        if not alt and not stitch:
            super(String, self).__init__(name="String", url="http://string-db.org/", verbose=verbose)

    _list_format = ['json', 'tsv', 'tsv-no-header', 'psi-mi', 'psi-mi-tab', 'image']
    _list_requests = ['resolve', 'resolveList', 'abstracts', 'abstractsList', 'interactors', 'interactorsList',
                      'actions', 'actionsList', 'interactions', 'interactionsList', 'network', 'networkList']
    _list_parameters = ["parameters", "identifier", "identifiers", "format", "species", "limit", "required_score,"
                        "additional_network_nodes", "network_flavor", "caller_identity"]

    def print_doc_requests(self):
        """
        print doc
        """
        webbrowser.open(url='http://string-db.org/help/index.jsp?topic=/org.string-db.docs/api.html')
        print('''
                database	    Description
                -------------------------------------------------
                string-db.org	Main entry point of STRING
                string.embl.de 	Alternative entry point of STRING
                stitch.embl.de 	The sister database of STRING


                access	    Description
                ----------------------------------------------
                api 	    Application programming interface
                services	Other services to access data


                format 	        Return value
                -------------------------------------------------------------------------------------------------------
                json	        JSON format either as a list of hashes/dictionaries, or as a plain list (if there is
                                    only one value to be returned per record)
                tsv	Tab         separated values, with a header line
                tsv-no-header	Tab separated values, without header line
                psi-mi	        The interaction network in PSI-MI 2.5 XML format
                psi-mi-tab	    Tab-delimited form of PSI-MI (similar to tsv, modeled after the IntAct specification.
                                    (Easier to parse, but contains less information than the XML format.)
                image	        The network image


                List of requests
                -------------------------------------------------------------------------------------------------------
                request	            Return value
                resolve	            List of items that match (in name or identifier) the query item
                resolveList	        List of items that match (in name or identifier) the query items
                abstracts	        List of abstracts that contain the query item
                abstractsList	    List of abstracts that contain any of the query items
                interactors	        List of interaction partners for the query item
                interactorsList	    List of interaction partners for any of the query items
                actions	            Action partners for the query item
                actionsList	        Action partners for any of the query items
                interactions	    Interaction network in PSI-MI 2.5 format or PSI-MI-TAB format (similar to tsv)
                interactionsList	Interaction network as above, but for a list of identifiers
                network	            The network image for the query item
                networkList	        The network image for the query items


                List of parameters and values
                -------------------------------------------------------------------------------------------------------
                parameters	                Descriptions, value
                identifier	                required parameter for single item, e.g. DRD1_HUMAN
                identifiers	                required parameter for multiple items, e.g.DRD1_HUMAN%0DDRD2_HUMAN
                format	                    For resolve requests: only-ids get the list of only the STRING identifiers
                                                (full by default) For abstract requests: use colon pmids for alternative
                                                shapes of the pubmed identifier
                species	                    Taxon identifiers (e.g. Human 9606, see: http://www.uniprot.org/taxonomy)
                limit	                    Maximum number of nodes to return, e.g 10.
                required_score	T           Threshold of significance to include a interaction, a number between 0 & 1000
                additional_network_nodes	Number of additional nodes in network (ordered by score), e.g./ 10
                network_flavor	            The style of edges in the network. evidence for colored multilines.
                                                confidence for singled lines where hue correspond to confidence score.
                                                (actions for stitch only)
                caller_identity	            Your identifier for us.
        ''')

    def test(self):
        # test url
        url = "api/tsv/abstractsList?identifiers=4932.YML115C%0D4932.YJR075W%0D4932.YEL036"

        # GET the object
        response = self.http_get(url)
        return response

    def resolve(self):
        return 0

    def abstracts(self):
        return 0

    def actions(self):
        return 0

    def interactors(self):
        return 0

    def interactions(self):
        return 0

    def network(self):
        return 0
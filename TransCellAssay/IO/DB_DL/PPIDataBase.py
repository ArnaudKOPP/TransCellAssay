__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"


class PPIDatabase(object):
    """
    A general interface for protein-protein interaction database access.
    An example::
    ppidb = MySuperPPIDatabase()
    ppidb.organisms() # List all organisms (taxids)
    ppidb.ids() # List all protein ids
    ppidb.ids(taxid="9606") # List all human protein ids.
    ppidb.links() # List all links
    """

    def __init__(self):
        pass

    def organisms(self):
        """
        Return all organism ncbi taxonomy ids contained in this database.
        """
        raise NotImplementedError

    def ids(self, taxid=None):
        """
        Return a list of all protein ids. If `taxid` (as returned by
        `organisms()`) is not ``None`` limit the results to ids to
        this organism only.

        """
        raise NotImplementedError

    def synonyms(self, id):
        """
        Return a list of synonyms for primary `id` (as returned by `ids`).
        """
        raise NotImplementedError

    def all_edges(self, taxid=None):
        """
        Return a list of all edges. If `taxid` is not ``None`` return the
        edges for this organism only.

        """
        raise NotImplementedError

    def edges(self, id1, id2=None):
        """
        Return a list of all edges (a list of 3-tuples (id1, id2, score)).
        """
        raise NotImplementedError

    def all_edges_annotated(self, taxid=None):
        """
        Return a list of all edges annotated. If taxid is not None
        return the edges for this organism only.
        """
        res = []
        for id in self.ids(taxid):
            res.extend(self.edges_annotated(id))
        return res

    def edges_annotated(self, id=None):
        """
        Return a list of all edges annotated.
        """
        raise NotImplementedError

    def search_id(self, name, taxid=None):
        """
        Search the database for protein name. Return a list of matching
        primary ids. Use `taxid` to limit the results to a single organism.
        """
        raise NotImplementedError

    @classmethod
    def download_data(self):
        """
        Download the latest PPI data for local work.
        """
        raise NotImplementedError


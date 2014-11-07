"""
This class is for Kegg REST api

Documentation : http://www.kegg.jp/kegg/rest/keggapi.html
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

from TransCellAssay.IO.Rest.Service import REST, ServiceError
from functools import reduce
import webbrowser
import copy

__all__ = ['KEGG', 'KEGGParser']
DEBUG = True


class KEGG(REST):
    """
    Interface to Kegg REST api
    """
    # : valid databases
    _valid_DB_base = ["module", "disease", "drug", "environ", "ko", "genome", "compound", "glycan", "reaction", "rpair",
                      "rclass", "enzyme"]
    _valid_DB = _valid_DB_base + ["pathway", "brite", "genes", "ligand", "organism", "genomes", "orthology"]
    _valid_databases_info = _valid_DB_base + ["pathway", "brite", "genes", 'ligand', "genomes", "kegg"]
    _valid_databases_list = _valid_DB_base + ["pathway", "brite", "organism"]
    _valid_databases_find = _valid_DB_base + ["pathway", "genes", "ligand"]
    _valid_databases_link = _valid_DB_base + ["pathway", "brite"]

    _docIds = "\n\n.. seealso:: :meth:`list`\n"

    def __init__(self, verbose=False):
        super(KEGG, self).__init__(name="KEGG", url="http://rest.kegg.jp", verbose=verbose)
        self.easyXMLConversion = False
        self._organism = None
        self._organisms = None
        self._pathway = None
        self._glycan = None
        self._compound = None
        self._ko = None
        self._enzyme = None
        self._reaction = None
        self._brite = None
        self._buffer = {}

    def __getattr__(self, req):
        if req.endswith("Ids"):
            db = req[0:-3]
            res = self.list(db)
            if db in [","]:
                Ids = [x.split()[1] for x in res.split("\n") if len(x)]
            else:
                Ids = [x.split()[0] for x in res.split("\n") if len(x)]
            return Ids
        elif req in self.databases:
            res = self.list(req)
            return res

    def code2Tnumber(self, code):
        """
        Converts organism code to its T number
        """
        index = self.organismIds.index(code)
        return self.organismTnumbers[index]

    def Tnumber2code(self, Tnumber):
        """
        Converts organism T number to its code
        """
        index = self.organismTnumbers.index(Tnumber)
        return self.organismIds[index]

    def isOrganism(self, orgId):
        """
        Check if orgId is a Kegg organism
        """
        if orgId in self.organismIds:
            return True
        if orgId in self.organismTnumbers:
            return True
        else:
            return False

    def _checkDB(self, database=None, mode=None):
        if DEBUG:
            print("Checking database %s (mode %s)" % (database, mode))
        isOrg = self.isOrganism(database)

        if mode == "info":
            if database not in KEGG._valid_databases_info and isOrg is False:
                print("\033[0;31m[ERROR]\033[0m Database or organism provided is not correct (mode=info)")
                raise ValueError
        elif mode == "list":
            if database not in KEGG._valid_databases_list and isOrg is False:
                print("\033[0;31m[ERROR]\033[0m Database is not correct (mode=list)")
                raise ValueError
        elif mode == "find":
            if database not in KEGG._valid_databases_find and isOrg is False:
                print("\033[0;31m[ERROR]\033[0m Database is not correct (mode=find)")
                raise ValueError
        elif mode == "link":
            if database not in KEGG._valid_databases_link and isOrg is False:
                print("\033[0;31m[ERROR]\033[0m Database is not correct (mode=link)")
                raise ValueError
        else:
            raise ValueError("Mode must be : info, list, find, link")

    def info(self, database="kegg"):
        """
        Display current statistics of given database
        :param database: can be one of: kegg (default), brite, module,
            disease, drug, environ, ko, genome, compound, glycan, reaction,
            rpair, rclass, enzyme, genomes, genes, ligand or any
            :attr:`organismIds`
        """
        self._checkDB(database, mode="info")
        res = self.http_get(database, frmt="txt")
        return res

    def list(self, query, organism=None):
        """
        Returns a list of entry identifiers and associated definition for a given database or a given set of
        database entries
        :param query:can be one of pathway, brite, module,
            disease, drug, environ, ko, genome, compound,
            glycan, reaction, rpair, rclass, enzyme, organism
            **or** an organism from the :attr:`organismIds` attribute **or** a valid
            dbentry (see below). If a dbentry query is provided, organism
            should not be used!
        :param organism: a valid organism identifier that can be
            provided. If so, database can be only "pathway" or "module". If
            not provided, the default value is chosen (:attr:`organism`)
        :return: A string with a structure that depends on the query

        Here is an example that shows how to extract the pathways IDs related to
        the hsa organism::
        s = KEGG()
        res = s.list("pathway", organism="hsa")
        pathways = [x.split()[0] for x in res.strip().split("\\n")]
        len(pathways)
        261

        Note, however, that there are convenient aliases to some of the databases.
        For instance, the pathway Ids can also be retrieved as a list from the
        :attr:`pathwayIds` attribute (after defining the :attr:`organism` attribute).

        .. note:: If you set the query to a valid organism, then the second
        argument rganism is irrelevant and ignored.

        .. note:: If the query is not a database or an organism, it is supposed
        to be a valid dbentries string and the maximum number of entries is 100.

        Other examples::
        s.list("pathway") # returns the list of reference pathways
        s.list("pathway", "hsa") # returns the list of human pathways
        s.list("organism") # returns the list of KEGG organisms with taxonomic classification
        s.list("hsa") # returns the entire list of human genes
        s.list("T01001") # same as above
        s.list("hsa:10458+ece:Z5100") # returns the list of a human gene and an E.coli O157 gene
        s.list("cpd:C01290+gl:G00092")# returns the list of a compound entry and a glycan entry
        s.list("C01290+G00092") # same as above
        """
        url = "list"
        if query:
            # can be something else than a database, so we can't use checkdb
            url += "/" + query

        if organism:
            if organism not in self.organismIds:
                raise ServiceError(
                    "Not a valid organism Invalid organism provided (%s). See the organismIds attribute" % organism)
            if query not in ["pathways", "module"]:
                print("""\033[0;31m[ERROR]\033[0m If organism is set, then the first argument (database) must be
                either 'pathways' or 'module', you provided %s""" % query)
            url += "/" + organism

        res = self.http_get(url, "txt")
        return res

    def find(self, database, query, option=None):
        """finds entries with matching query keywords or other query data in a given database

        :param str database: can be one of pathway, module, disease, drug,
                environ, ko, genome, compound, glycan, reaction, rpair, rclass,
                enzyme, genes, ligand or an organism code (see :attr:`organismIds`
                attributes) or T number (see :attr:`organismTnumbers` attribute).
        :param str query: See examples
        :param str option: If option provided, database can be only 'compound'
                or 'drug'. Option can be 'formula', 'exact_mass' or 'mol_weight'

        .. note:: Keyword search against brite is not supported. Use /list/brite to
        retrieve a short list.

        # search for pathways that contain Viral in the definition
        s.find("pathway", "Viral")
        # for keywords "shiga" and "toxin"
        s.find("genes", "shiga+toxin")
        # for keywords "shiga toxin"
        s.find("genes", ""shiga toxin")
        # for chemical formula "C7H10O5"
        s.find("compound", "C7H10O5", "formula")
        # for chemical formula containing "O5" and "C7"
        s.find("compound", "O5C7","formula")
        # for 174.045 =< exact mass < 174.055
        s.find("compound", "174.05","exact_mass")
        # for 300 =< molecular weight =< 310
        s.find("compound", "300-310","mol_weight")
        """
        _valid_options = ['formula', "exact_mass", "mol_weight"]
        _valid_db_options = ["compound", "drug"]

        self._checkDB(database, mode="find")
        url = "find/" + database + "/" + query

        if option:
            if database not in _valid_db_options:
                raise ValueError("\033[0;31m[ERROR]\033[0m invalid database. Since option was provided, database must "
                                 "be in %s" % _valid_db_options)
            if option not in _valid_options:
                raise ValueError("\033[0;31m[ERROR]\033[0m invalid option. Must be in %s " % _valid_options)
            url += "/" + option

        res = self.http_get(url, frmt="txt")
        return res

    def show_entry(self, entry):
        """
        open url that correspond to a valid entry
        :param entry: valid entry
        :return: open tab
        """
        url = "http://www/kegg.jp/dbget-bin/www_bget?" + entry
        webbrowser.open(url)

    def get(self, dbentries, option=None):
        """
        Retrieves given database entrie
        :param dbentries:  KEGG database entries involving the following
            database: pathway, brite, module, disease, drug, environ, ko, genome
            compound, glycan, reaction, rpair, rclass, enzyme **or** any organism
            using the KEGG organism code (see :attr:`organismIds`
            attributes) or T number (see :attr:`organismTnumbers` attribute).
        :param option: aaseq, ntseq, mol, kcf, image, kgml

        s = KEGG()
        # retrieves a compound entry and a glycan entry
        s.get("cpd:C01290+gl:G00092")
        # same as above
        s.get("C01290+G00092")
        # retrieves a human gene entry and an E.coli O157 gene entry
        s.get("hsa:10458+ece:Z5100")
        # retrieves amino acid sequences of a human gene and an E.coli O157 gene
        s.get("hsa:10458+ece:Z5100/aaseq")
        # retrieves the image file of a pathway map
        s.get("hsa05130/image")
        # same as above
        s.get("hsa05130", "image")
        Another example here below shows how to save the image of a given pathway::
        res = s.get("hsa05130/image")
        # same as : res = s.get("hsa05130","image")
        f = open("test.png", "w")
        f.write(res)
        f.close()
        .. note:: The input is limited up to 10 entries (KEGG restriction).
        """
        _valid_options = ["aaseq", "ntseq", "mol", "kcf", "image", "kgml"]
        _valid_db_options = ["compound", "drug"]

        url = "get/" + dbentries

        if option:
            if option not in _valid_options:
                raise ValueError("\033[0;31m[ERROR]\033[0m Invalid Option. Must be in %s" % _valid_options)
            url += "/" + option

        res = self.http_get(url, frmt="txt")
        return res

    def conv(self, target, source):
        """
        Convert KEGG identifiers to/from outside identifiers
        :param target: target database (kegg orga)
        :param source: source database (uniprot or valid dbentries
        :return: dict with keys being the source and value being the target
        Here are the rules to set the target and source parameters.
        If the second argument is not a **dbentries**, source and target
        parameters can be of two types:
        #. gene identifiers. If the target is a KEGG Id, then the source
        must be one of *ncbi-gi*, *ncbi-geneid* or *uniprot*.
        .. note:: source and target can be swapped.
        #. chemical substance identifiers. If the target is one of the
        following kegg database: drug, compound, glycan then the source
        must be one of *pubchem* or *chebi*.
        .. note:: again, source and target can be swapped
        If the second argument is a **dbentries**, it can be again of two types:
        #. gene identifiers. The database used can be one ncbi-gi,
        ncbi-geneid, uniprot or any KEGG organism
        #. chemical substance identifiers. The database used can be one of
        drug, compound, glycan, pubchem or chebi only.
        .. note:: if the second argument is a dbentries, target and dbentries
        cannot be swapped.
        ::
        # conversion from NCBI GeneID to KEGG ID for E. coli genes
        conv("eco","ncbi-geneid")
        # inverse of the above example
        conv("eco","ncbi-geneid")
        #conversion from KEGG ID to NCBI GI
        conv("ncbi-gi","hsa:10458+ece:Z5100")
        To make it clear by taking another example, you can either convert an
        entire database to another (e.g., from uniprot to KEGG Id all human gene
        IDs)::
        uniprot_ids, kegg_ids = s.conv("hsa", "uniprot")
        or a subset by providing a valid **dbentries**::
        s.conv("hsa","up:Q9BV86+")
        .. warning:: dbentries are not check and are supposed to be correct.
        See :meth:`check_idbentries` to help you checking a dbentries.
        """
        isOrg = self.isOrganism(target)
        if isOrg is False and target not in ['ncbi-gi', 'ncbi-geneid', 'uniprot', 'pubchem', 'chebi', 'drug',
                                             'compound', 'glycan']:
            raise ValueError(
                "\033[0;31m[ERROR]\033[0m Invalid syntax, target must be a KEGG id or one of the allowed database")

        url = "conv/" + target + "/" + source
        res = self.http_get(url, frmt="txt")

        try:
            t = [x.split("\t")[0] for x in res.strip().split("\n")]
            s = [x.split("\t")[1] for x in res.strip().split("\n")]
            return dict([(x, y) for x, y in zip(t, s)])
        except:
            return res
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

    def link(self, target, source):
        """
        find related entries by using database cross-reference
        :param target: kegg database target or organism
        :param source: kegg database target or organism or a valid dbentries involving one of the database

        the valid list of db is pathway, brite, module, disease, drug, environ, ko, genome, compound, glycan, reaction
        rpair, rclass, enzyme
        """
        self._checkDB(target, mode="link")
        url = "link/" + target + "/" + source
        res = self.http_get(url, frmt="txt")
        return res

    def entry(self, dbentries):
        """
        retrieve entry
        equivalent to .get
        """
        raise NotImplementedError("Use .get instead")

    def show_pathway(self, pathId, scale=None, dcolor="pink", keggid={}):
        """
        show a given path into webbrower
        :param pathId: valid path id
        :param scale: scale image between 0 and 100
        :param dcolor: default background color of nodes
        :param keggid: set color of entries contained in the pathways

        if scale is provided, keggid and dcolor is ignored

        """
        if pathId.startswith("path:"):
            pathId = pathId.split(":")[1]

        if scale:
            scale = int(scale / 100. * 100) / 100.  # just need 2 digits and a value in [0,1]
            url = "http://www.kegg.jp/kegg-bin/show_pathway?scale=" + str(scale)
            url += "&query=&map=" + pathId
        else:
            url = "http://www.kegg.jp/kegg-bin/show_pathway?" + pathId
            if dcolor:
                url += "/default%%3d%s/" % dcolor
            if isinstance(keggid, dict):
                if len(keggid.keys()) > 0:
                    for k, v in keggid.items():
                        if "," in v:
                            url += "/%s%%09%s/" % (k, v)
                        else:
                            url += "/%s%%09,%s/" % (k, v)
            elif isinstance(keggid, list):
                for k in keggid:
                    url += "/%s%%09,%s/" % (k, "red")

        self.logging.info(url)
        res = webbrowser.open(url)
        return res

    def show_module(self, modId):
        """Show a given module inside a web browser
        :param str modId: a valid module Id. See :meth:`moduleIds`
        Validity of modId is not checked but if wrong the URL will not open a
        proper web page.
        """
        if modId.startswith("md:"):
            modId = modId.split(":")[1]
        url = "http://www.kegg.jp/module/" + modId
        self.logging.info(url)
        res = webbrowser.open(url)
        return res

    def check_dbentries(self, dbentries, checkAll=True):
        """Checks that all entries provided exist in the KEGG database
        :param str dbentries: a dbentries list. entries are separated by the +'
            sign (e.g., "hsa:10458+ece:Z5100")
        :param bool checkAll: checks all entries (Default) or stop as soon as an
            entry is not well formed.
        :return: True if all entries are correct. False otherwise
        ::
            s = KEGG()
            s.check_dbentries("hsa:10458+ece:Z5100")
        """
        from urllib.error import HTTPError

        entries = dbentries.split("+")
        # we do not want logging here
        debugLevel = self.debugLevel
        self.debugLevel = "CRITICAL"
        allStatus = True
        for entry in entries:
            try:
                self.get(entry)
                status = True
            # if ill-formed, an entry will raise the 404 error.
            except HTTPError as e:
                if e.code == 404:
                    status = False
                    allStatus = False
                    if checkAll is False:
                        print(entry, status)
                        return False
                else:
                    print(e)
                    raise
            except:
                self.debugLevel = debugLevel
                raise
            print(entry, status)
        # retrieve logging level
        self.debugLevel = debugLevel
        return allStatus

    # wrapper of all databases to ease access to them (buffered)

    def _get_db(self):
        return KEGG._valid_DB

    databases = property(_get_db, doc="Returns list of valid KEGG databases.")

    def _get_database(self, dbname, mode=0):
        res = self.list(dbname)
        assert mode in [0, 1]
        return [x.split()[mode] for x in res.split("\n") if len(x)]

    def _get_organisms(self):
        if self._organisms is None:
            self._organisms = self._get_database("organism", 1)
        return self._organisms

    organismIds = property(_get_organisms, doc="Returns list of organism Ids")

    def _get_reactions(self):
        if self._reaction is None:
            self._reaction = self._get_database("reaction", 0)
        return self._reaction

    reactionIds = property(_get_reactions, doc="returns list of reaction Ids")

    def _get_enzyme(self):
        if self._enzyme is None:
            self._enzyme = self._get_database("enzyme", 0)
        return self._enzyme

    enzymeIds = property(_get_enzyme,
                         doc="returns list of enzyme Ids" + _docIds)

    def _get_organisms_tnumbers(self):
        if self._organisms_tnumbers is None:
            self._organisms_tnumbers = self._get_database("organism", 0)
        return self._organisms_tnumbers

    organismTnumbers = property(_get_organisms_tnumbers,
                                doc="returns list of organisms (T numbers)" + _docIds)

    def _get_glycans(self):
        if self._glycan is None:
            self._glycan = self._get_database("glycan", 0)
        return self._glycan

    glycanIds = property(_get_glycans,
                         doc="Returns list of glycan Ids" + _docIds)

    def _get_brite(self):
        if self._brite is None:
            self._brite = self._get_database("brite", 0)
        return self._brite

    briteIds = property(_get_brite,
                        doc="returns list of brite Ids." + _docIds)

    def _get_kos(self):
        if self._ko is None:
            self._ko = self._get_database("ko", 0)
        return self._ko

    koIds = property(_get_kos, doc="returns list of ko Ids" + _docIds)

    def _get_compound(self):
        if self._compound is None:
            self._compound = self._get_database("compound", 0)
        return self._compound

    compoundIds = property(_get_compound,
                           doc="returns list of compound Ids" + _docIds)

    def _get_drug(self):
        if self._drug is None:
            self._drug = self._get_database("drug", 0)
        return self._drug

    drugIds = property(_get_drug, doc="returns list of drug Ids" + _docIds)

    # set the default organism used by pathways retrieval
    def _get_organism(self):
        return self._organism

    def _set_organism(self, organism):
        if organism in self.organismIds:
            self._organism = organism
            self._pathway = None
            self._module = None
            self._ko = None
            self._glycan = None
            self._compound = None
            self._enzyme = None
            self._drug = None
            self._reaction = None
            self._brite = None
        else:
            raise ValueError("Invalid organism. Check the list in :attr:`organismIds` attribute")

    organism = property(_get_organism, _set_organism, doc="returns the current default organism ")

    def _get_pathways(self):
        if self._organism is None:
            print("You must set the organism first (e.g., self.organism = 'hsa')")
            return

        if self._pathway is None:
            res = self.http_get("list/pathway/%s" % self.organism, frmt="txt")
            orgs = [x.split()[0] for x in res.split("\n") if len(x)]
            self._pathway = orgs[:]
        return self._pathway

    pathwayIds = property(_get_pathways, doc="""returns list of pathway Ids for the default organism.
    :attr:`organism` must be set.
    ::
        s = KEGG()
        s.organism = "hsa"
        s.pathwayIds
    """)

    def _get_modules(self):
        if self._organism is None:
            print("You must set the organism first (e.g., self.organism = 'hsa')")
            return

        if self._module is None:
            res = self.http_get("list/module/%s" % self.organism)
            orgs = [x.split()[0] for x in res.split("\n") if len(x)]
            self._module = orgs[:]
        return self._module

    moduleIds = property(_get_modules, doc="""returns list of module Ids for the default organism.
    :attr:`organism` must be set.
    ::
        s = KEGG()
        s.organism = "hsa"
        s.moduleIds
    """)

    def lookfor_organism(self, query):
        """Look for a specific organism
        :param str query: your search term. upper and lower cases are ignored
        :return: a list of definition that matches the query
        """
        matches = []
        definitions = [" ".join(x.split()) for x in self.list("organism").split("\n")]
        for i, item in enumerate(definitions):
            if query.lower() in item.lower():
                matches.append(i)
        return [definitions[i] for i in matches]

    def lookfor_pathway(self, query):
        """Look for a specific pathway
        :param str query: your search term. upper and lower cases are ignored
        :return: a list of definition that matches the query
        """
        matches = []
        definitions = [" ".join(x.split()) for x in self.list("pathway").split("\n")]
        for i, item in enumerate(definitions):
            if query.lower() in item.lower():
                matches.append(i)
        return [definitions[i] for i in matches]

    def get_pathway_by_gene(self, gene, organism):
        """Search for pathways that contain a specific gene
        :param str gene: a valid gene Id
        :param str organism: a valid organism (e.g., hsa)
        :return: list of pathway Ids that contain the gene
        ::
            >>> s.get_pathway_by_gene("7535", "hsa")
            ['path:hsa04064', 'path:hsa04650', 'path:hsa04660', 'path:hsa05340']
        """
        p = KEGGParser(verbose=False)
        p.organism = organism
        res = self.get(":".join([organism, gene]))
        dic = p.parse(res)
        if 'pathway' in dic.keys():
            return dic['pathway']
        else:
            print("No pathway found ?")


    def _old_get_pathway_by_gene(self, gene, organism):
        matches = []
        p = KEGGParser()
        # using existing buffered list if same organism are used
        if self.organism == organism:
            Ids = self.pathwayIds
        else:
            p.organism = organism
            Ids = p.pathwayIds

        for i, Id in enumerate(Ids):
            print("scanning %s (%s/%s)" % (Id, i, len(Ids)))
            if Id not in self._buffer.keys():
                res = p.get(Id)
                self._buffer[Id] = res
            else:
                res = self._buffer[Id]

            parsed = p.parse(res)
            if 'gene' in parsed.keys() and gene in parsed['gene']:
                print("Found %s in pathway Ids %s" % (gene, Id))
                matches.append(Id)
        return matches

    def parse_kgml_pathway(self, pathwayId, res=None):
        """Parse the pathway in KGML format and returns a dictionary (relations and entries)
        :param str pathwayId: a valid pathwayId e.g. hsa04660
        :param str res: if you already have the output of the query
            get(pathwayId), you can provide it, otherwise it is queried.
        :return: a tuple with the first item being a list of relations. Each
            relations is a dictionary with id2, id2, link, value, name. The
            second item is a dictionary that maps the Ids to
        ::
            res = s.parse_kgml_pathway("hsa04660")
            set([x['name'] for x in res['relations']])
            res['relations'][-1]
            {'entry1': u'15',
             'entry2': u'13',
             'link': u'PPrel',
             'name': u'phosphorylation',
             'value': u'+p'}
            >>> set([x['link'] for x in res['relations']])
            set([u'PPrel', u'PCrel'])
            >>> res['entries'][4]
        ret = s.get("hsa04660", "kgml")
        .. seealso:: `KEGG API <http://www.kegg.jp/kegg/xml/docs/>`_
        """
        output = {'relations': [], 'entries': []}
        # Fixing bug #24 assembla
        if res is None:
            res = self.easyXML(self.get(pathwayId, "kgml"))
        else:
            res = self.easyXML(res)
        # here entry1 and 2 are Id related to the kgml file

        # read and parse the entries
        entries = [x for x in res.findAll("entry")]
        for entry in entries:
            output['entries'].append({
                'id': entry.get("id"),
                'name': entry.get("name"),
                'type': entry.get("type"),
                'link': entry.get("link"),
                'gene_names': entry.find("graphics").get("name")
            })

        relations = [(x.get("entry1"), x.get("entry2"), x.get("type")) for x in res.findAll("relation")]
        subtypes = [x.findAll("subtype") for x in res.findAll("relation")]

        assert len(subtypes) == len(relations)

        for relation, subtype in zip(relations, subtypes):
            if len(subtype) == 0:  # nothing to do with the species ??? TODO
                pass
            else:
                for this in subtype:
                    value = this.get("value")
                    name = this.get("name")
                    output['relations'].append({
                        'entry1': relation[0],
                        'entry2': relation[1],
                        'link': relation[2],
                        'value': value,
                        'name': name})
        # we need to map back to KEgg IDs...
        return output

    def pathway2sif(self, pathwayId, uniprot=True):
        """Extract protein-protein interaction from KEGG pathway to a SIF format
        .. warning:: experimental Not tested on all pathway. should be move to
            another package such as cellnopt
        :param str pathwayId: a valid pathway Id
        :param bool uniprot: convert to uniprot Id or not (default is True)
        :return: a list of relations (A 1 B) for activation and (A -1 B) for
            inhibitions
        This is longish due to the conversion from KEGGIds to UniProt.
        This method can be useful to provide prior knowledge network to software
        such as CellNOpt (see http://www.cellnopt.org)
        """
        res = self.parse_kgml_pathway(pathwayId)
        sif = []
        for rel in res['relations']:
            # types can be PPrel (protein-protein interaction only
            if rel['link'] != 'PPrel':
                continue
            if rel['name'] == 'activation':
                Id1 = rel['entry1']
                Id2 = rel['entry2']
                name1 = res['entries'][[x['id'] for x in res['entries']].index(Id1)]['name']
                name2 = res['entries'][[x['id'] for x in res['entries']].index(Id2)]['name']
                type1 = res['entries'][[x['id'] for x in res['entries']].index(Id1)]['type']
                type2 = res['entries'][[x['id'] for x in res['entries']].index(Id2)]['type']
                # print("names:", rel, name1, name2)
                # print(type1, type2)
                if type1 != 'gene' or type2 != 'gene':
                    continue
                if uniprot:
                    try:
                        # FIXME  sometimes, there are more than one name
                        name1 = name1.split()[0]
                        name2 = name2.split()[0]
                        name1 = self.conv("uniprot", name1)[name1]
                        name2 = self.conv("uniprot", name2)[name2]
                    except Exception:
                        print(name1)
                        print(name2)
                        raise Exception
                #print(name1, 1, name2)
                sif.append([name1, 1, name2])
            elif rel['name'] == 'inhibition':
                Id1 = rel['entry1']
                Id2 = rel['entry2']
                name1 = res['entries'][[x['id'] for x in res['entries']].index(Id1)]['name']
                name2 = res['entries'][[x['id'] for x in res['entries']].index(Id2)]['name']
                type1 = res['entries'][[x['id'] for x in res['entries']].index(Id1)]['type']
                type2 = res['entries'][[x['id'] for x in res['entries']].index(Id2)]['type']
                # print("names:", rel, name1, name2)
                # print(type1, type2)
                if type1 != 'gene' or type2 != 'gene':
                    continue
                if uniprot:
                    name1 = name1.split()[0]
                    name2 = name2.split()[0]
                    name1 = self.conv("uniprot", name1)[name1]
                    name2 = self.conv("uniprot", name2)[name2]
                #print(name1, -1, name2)
                sif.append([name1, -1, name2])
            else:
                pass
                # print("#", rel['entry1'], rel['name'], rel['entry2'])

        return sif

    def __str__(self):
        txt = self.info()
        return txt


class KEGGParser(KEGG):
    """This is an extension of the :class:`KEGG` class to ease parsing of dbentries
    This class provides a generic method :meth:`parse` that will read the output
    of a dbentry returned by :meth:`KEGG.get` and converts it into a dictionary ready to use.
    The :meth:`parse` method is a dispatcher so you do not have to worry about the
    type of entry you are using. It can be a pathway, a gene, a compound...
    ::
        from bioservices import *
        s = KEGGParser()
        # Retrieve a KEGG entry
        res = s.get("hsa04150")
        # parse it
        d = s.parse(res)
    As a pedagogical example, you can then further process this dictionary. Here below, we convert
    the gene Ids found in the pathway into UniProt Ids::
        # Get the KEGG Ids in the pathway
        kegg_geneIds = [x for x in d['gene']]
        # Convert them
        db_up, db_kegg = s.conv("hsa", "uniprot")
        # Get the corresponding uniprot Ids
        indices = [db_kegg.index("hsa:%s" % x ) for x in kegg_geneIds]
        uniprot_geneIds = [db_up[x] for x in indices]
    However, you could also have done it simply as follows::
        kegg_geneIds = [x for x in d['gene']]
        uprot_geneIds = [s.parse(s.get("hsa:"+str(e)))['dblinks']["UniProt:"] for e in d['gene']]
    .. note:: The 2 outputs are slightly different.
    .. seealso:: http://www.kegg.jp/kegg/rest/dbentry.html
    """

    def __init__(self, verbose=False):
        super(KEGGParser, self).__init__(verbose=verbose)

    def parse(self, res):
        """A dispatcher to parse all outputs returned by :meth:`KEGG.get`
        :param str res: output of a :meth:`KEGG.get`.
        :return: a dictionary
        ::
            res = s.get("md:hsa_M00554")
            d = s.parse(res)
        """
        entry = res.split("\n")[0].split()[0]
        if entry == "ENTRY":
            dbentry = res.split("\n")[0].split(None, 2)[2]

        if "Pathway" in dbentry and "Module" not in dbentry:
            parser = self.parsePathway(res)
        elif dbentry.lower() == "pathway   module":
            parser = self.parseModule(res)
        elif "Drug" in dbentry:  # can be Drug or "Mixture Drug"
            parser = self.parseDrug(res)
        elif "Disease" in dbentry:
            parser = self.parseDisease(res)
        elif "Environ" in dbentry:
            parser = self.parseEnviron(res)
        elif "Orthology" in dbentry:
            parser = self.parseOrthology(res)
        elif "KO" in dbentry:
            parser = self.parseOrthology(res)
        elif "Genome" in dbentry:
            parser = self.parseGenome(res)
        elif "gene" in dbentry:
            parser = self.parseGene(res)
        elif "CDS" in dbentry:
            parser = self.parseGene(res)
        elif "Compound" in dbentry:
            parser = self.parseCompound(res)
        elif "Glycan" in dbentry:
            parser = self.parseGlycan(res)
        elif "Reaction" in dbentry:
            parser = self.parseReaction(res)
        elif "RPair" in dbentry:
            parser = self.parseRpair(res)
        elif "RClass" in dbentry:
            parser = self.parseRclass(res)
        elif "Enzyme" in dbentry:
            parser = self.parseEnzyme(res)
        elif "tRNA" in dbentry:
            parser = self.parsetRNA(res)
        else:
            raise NotImplementedError("Entry %s not yet implemented" % dbentry)
        return parser

    def parsetRNA(self, res):
        """parse a tRNA entry
        .. versionadded:: 1.2.0
        """
        flatfile = ["ENTRY", "NAME", "DEFINITION", "ORTHOLOGY", "ORGANISM", "PATHWAY",
                    "CLASS", "POSITION", "DBLINKS", "NTSEQ"]
        parser = self._parse(res, flatfile)
        return parser

    def parseDrug(self, res):
        """Parses a drug entry
        ::
            res = s.get("dr:D00001")
            d = s.parseDrug(res)
        """
        flatfile = ["ENTRY", "NAME", "PRODUCTS", "FORMULA", "EXACT_MASS",
                    "MOL_WEIGHT", "COMPONENT", "SEQUENCE", "SOURCE", "ACTIVITY",
                    "REMARK", "COMMENT", "TARGET", "METABOLISM", "INTERACTION",
                    "PATHWAY", "STR_MAP", "BRITE", "DBLINKS", "ATOM", "BOND", "BRACKET"]
        parser = self._parse(res, flatfile)
        return parser

    def parsePathway(self, res):
        """Parses a pathway entry
        ::
            res = s.get("path:hsa10584")
            d = s.parsePathway(res)
        """
        flatfile = ["ENTRY", "NAME", "DESCRIPTION", "CLASS", "PATHWAY_MAP",
                    "MODULE", "DISEASE", "DRUG", "DBLINKS", "ORGANISM", "ORTHOLOGY",
                    "GENE", "ENZYME", "REACTION", "COMPOUND", "REFERENCE",
                    "REL_PATHWAY", "KO_PATHWAY"]
        parser = self._parse(res, flatfile)
        return parser

    def parseModule(self, res):
        """Parses a module entry
        ::
            res = s.get("md:hsa_M00554")
            d = s.parseModule(res)
        """
        flatfile = ["ENTRY", "NAME", "DEFINITION", "PATHWAY",
                    "ORTHOLOGY", "CLASS", "BRITE", "ORGANISM", "GENE", "REACTION",
                    "COMPOUND", "COMMENT", "DBLINKS", "REFERENCE", "REF_MODULE"]
        parser = self._parse(res, flatfile)
        return parser

    def parseDisease(self, res):
        """Parses a disease entry
        ::
            res = s.get("ds:H00001")
            d = s.parseDisease(res)
        """
        flatfile = ["ENTRY", "NAME", "DESCRIPTION", "CATEGORY", "PATHWAY", "GENE",
                    "ENV_FACTOR", "MARKER", "DRUG", "COMMENT", "DBLINKS", "REFERENCE"]
        parser = self._parse(res, flatfile)
        return parser

    def parseEnviron(self, res):
        """Parses a environ entry
        ::
            res = s.get("ev:E00001")
            d = s.parseEnviron(res)
        """
        flatfile = ['ENTRY', "NAME", "CATEGORY", "COMPONENT", "SOURCE",
                    "REMARK", "COMMENT", "BRITE", "DBLINKS"]
        parser = self._parse(res, flatfile)
        return parser

    def parseOrthology(self, res):
        """Parses Orthology entry
        ::
            res = s.get("ko:K00001")
            d = s.parseOrthology(res)
        .. note:: in other case genes key is "gene". Here it is "genes".
        """
        flatfile = ['ENTRY', "NAME", "DEFINITION", "PATHWAY", "MODULE",
                    "DISEASE", "BRITE", "DBLINKS", "GENES", "REFERENCE"]
        parser = self._parse(res, flatfile)
        return parser

    def parseGenome(self, res):
        """Parses a Genome entry
        ::
            res = s.get('genome:T00001')
            d = s.parseGenome(res)
        """

        flatfile = ["ENTRY", "NAME", "DEFINITION", "ANNOTATION", "TAXONOMY",
                    "DATA_SOURCE", "ORIGINAL_DB", "KEYWORDS", "DISEASE", "COMMENT",
                    "CHROMOSOME", "PLASMID", "STATISTICS", "REFERENCE"]
        parser = self._parse(res, flatfile)
        return parser

    def parseGene(self, res):
        """Parses a gene entry
        ::
            res = s.get("hsa:1525")
            d = s.parseGene(res)
        """

        flatfile = ["ENTRY", "NAME", "DEFINITION", "ORTHOLOGY", "ORGANISM",
                    "PATHWAY", "MODULE", "DISEASE", "DRUG_TARGET", "CLASS", "MOTIF", "DBLINKS",
                    "STRUCTURE", "POSITION", "AASEQ", "NTSEQ"]
        parser = self._parse(res, flatfile)
        return parser


    def parseCompound(self, res):
        """Parses a compound entry
        ::
            s.get("cpd:C00001")
            d = s.parseCompound(res)
        """
        flatfile = ["ENTRY", "NAME", "FORMULA", "EXACT_MASS", "MOL_WEIGHT",
                    "SEQUENCE", "REMARK", "COMMENT", "REACTION", "PATHWAY", "ENZYME", "BRITE",
                    "REFERENCE", "DBLINKS", "ATOM", "BOND", "BRACKET"]
        parser = self._parse(res, flatfile)
        return parser

    def parseGlycan(self, res):
        """Parses a glycan entry
        ::
            res = s.get("gl:G00001")
            d = s.parseGlycan(res)
        """
        flatfile = ["ENTRY", "NAME", "COMPOSITION", "MASS", "CLASS", "REMARK",
                    "COMMENT", "REACTION", "PATHWAY", "ENZYME", "ORTHOLOGY",
                    "REFERENCE", "DBLINKS", "NODE", "EDGE", "BRACKET"]
        parser = self._parse(res, flatfile)
        return parser

    def parseReaction(self, res):
        """Parses a reaction entry
        ::
            res = s.get("rn:R00001")
            d = s.parseReaction(res)
        """
        flatfile = ["ENTRY", "NAME", "DEFINITION", "EQUATION", "REMARK",
                    "COMMENT", "RPAIR", "ENZYME", "PATHWAY", "ORTHOLOGY", "REFERENCE"]
        parser = self._parse(res, flatfile)
        return parser

    def parseRpair(self, res):
        """Parses a rpair entry
        ::
            res = s.get("rp:RP00001")
            d = s.parseRpair(res)
        .. todo:: a better parsing
        """
        flatfile = ["ENTRY", "NAME", "COMPOUND", "TYPE", "RDM", "RCLASS",
                    "RELATEDPAIR", "REACTION", "Enzyme  ENZYME", "ALIGN", "ENTRY1", "ENTRY2"]
        parser = self._parse(res, flatfile)
        return parser


    def parseRclass(self, res):
        """Parses a rclass entry
        ::
            res = s.get("rc:RC00001")
            d = s.parseRclass(res)
        .. todo:: a better parsing
        """
        flatfile = ["ENTRY", "DEFINITION", "RPAIR", "REACTION",
                    "ENZYME", "PATHWAY", "ORTHOLOGY"]
        parser = self._parse(res, flatfile)
        return parser

    def parseEnzyme(self, res):
        """Parses an enzyme entry
        ::
            res = s.get('ec:1.1.1.1')
            d = s.parseEnzyme(res)
        """
        flatfile = ["ENTRY", "NAME", "CLASS", "SYSNAME", "REACTION", "ALL_REAC",
                    "SUBSTRATE", "PRODUCT", "COMMENT", "PATHWAY", "ORTHOLOGY", "GENES",
                    "REFERENCE"]
        parser = self._parse(res, flatfile)
        return parser

    def _parse(self, res, flatfile):
        """Reaction is currently a dictionary if more than one line maybe we
        want a list instead.
        """
        output = {}
        lines = res.split("\n")

        # scanning res and searching for flatfile keywords; keep track of
        # current one. Should be an entry first.
        current = None
        countref = 1  # reference counter for reference without a value
        for line in lines:
            line = line.strip()
            if line == "///" or len(line) == 0:
                continue

            if len(line.split()) >= 2:  # split each line to search for the first term
                key, text = line.split(None, 1)
            else:
                key = line

            # REFERENCES are dealt with in the else
            if key in flatfile and \
                            key not in ["REFERENCE", "AUTHORS", "TITLE", "JOURNAL"]:
                # store the first appearance of a key
                output[key.lower()] = line.split(key)[1].strip()
                current = key.lower()  # keep track of the current key
            else:
                # There are many instances of referneces that are followed
                # by authors/title/journal triplet
                if key == "REFERENCE":
                    current = key.lower()
                    if current not in output.keys():
                        # the first time, we create a dictionary
                        output[current] = {}

                # Sometimes, we want to create a dictionary. For instance, genes
                # but in other cases  we just want to append the text (e.g.
                # remarks)
                if current in ["gene", "reference", "rel_pathway", "orthology", \
                               "pathway", "reaction", "compound", "dblinks", "marker"]:
                    if isinstance(output[current], dict) is False:
                        # The item may be of different length. In the gene case, we
                        # want to provide a list of dictionaries with key being the
                        # gene id but in some other cases,
                        try:
                            key, value = output[current].split(" ", 1)
                        except:
                            value = output[current]
                        output[current] = {key: value}
                    mode = "dict"
                else:
                    if isinstance(output[current], list) is False:
                        value = output[current]
                        output[current] = [value]
                    mode = "append"

                # For references only
                if current == "reference":
                    try:
                        key, value = line.strip().split(" ", 1)
                    except:
                        key = line.strip()
                        countref += 1
                        value = str(countref)
                    if key.upper() in ["AUTHORS", "TITLE", "JOURNAL"]:
                        output[current][pubmed][key] = value
                    elif key.upper() == "REFERENCE":
                        pubmed = value.strip()
                        if pubmed in output[current].keys():
                            pubmed += "_" + str(countref)
                            countref += 1
                        output[current][pubmed] = {}
                else:  # and all others
                    if mode == "dict":
                        try:
                            key, value = line.strip().split(" ", 1)
                        except:  # needed in INTERACTION case (DRUG)
                            key = line.strip()
                            value = ""
                        output[current][key.strip()] = value.strip()
                    else:
                        output[current].append(line)

        # some cleanup
        if "ntseq" in output.keys():
            data = output['ntseq']
            output['ntseq'] = {data[0]: reduce(lambda x, y: x + y, data[1:])}
        if "aaseq" in output.keys():
            data = output['aaseq']
            output['aaseq'] = {data[0]: reduce(lambda x, y: x + y, data[1:])}
        if "dblinks" in output.keys():
            try:
                data = output['dblinks']
                output['dblinks'] = {k[0:-1]: v for k, v in output['dblinks'].items()}
            except:
                pass

        return output


class KEGGTools(KEGG):
    """
    k = kegg.KEGGTools()
    k.load_genes("hsa")
    k.dbentries = []
    for i, this in enumerate(k.genes[0:50]):
        res = k.scan_genes(i)
        print(float(i)/len(k.genes))
        k.dbentries.append(res)
    """

    def __init__(self, verbose=False, organism="hsa"):
        self.kegg = KEGG()
        self.parser = KEGGParser()
        print("initialisation")

    def load_genes(self, organism):
        res = self.parser.list(organism)
        self.genes = [x.split("\t")[0] for x in res.strip().split("\n")]
        return self.genes


    def scan_genes(self, i):
        return self.parser.parse(self.kegg.get(self.genes[i]))
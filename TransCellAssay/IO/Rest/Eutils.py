# coding=utf-8
"""
Interface to the EUtils web Service.

.. topic:: What is EUtils ?

    :URL: http://www.ncbi.nlm.nih.gov/books/NBK25497/

    .. highlights::

        The Entrez Programming Utilities (E-utilities) are a set of eight server-side programs that provide a stable
        interface into the Entrez query and database system at the National Center for Biotechnology Information (NCBI).
        The E-utilities use a fixed URL syntax that translates a standard set of input parameters into the values
        necessary for various NCBI software components to search for and retrieve the requested data. The E-utilities
        are therefore the structured interface to the Entrez system, which currently includes 38 databases covering a
        variety of biomedical data, including nucleotide and protein sequences, gene records, three-dimensional
        molecular structures, and the biomedical literature.

       -- from http://www.ncbi.nlm.nih.gov/books/NBK25497/, March 2013

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


class EUtils(REST):
    """
    Interface to NCBI Entrez Utilities <http://eutils.ncbi.nlm.nih.gov/entrez/eutils/> service

    The EUtils class has a method called EFetch so this is actually covering
    all Entrez functionalities.

    .. warning:: Read the `guidelines
        <http://www.ncbi.nlm.nih.gov/books/NBK25497/>`_ before sending requests.
        No more than 3 requests per seconds otherwise your IP may be banned.
        You should provide your email by filling the :attr:`email` so that
        before being banned, you may be contacted.

    """

    _db = """

        Entrez Database     UID common name     E-utility Database Name
        ---------------------------------------------------------------
        Bioproject          BioProject ID       bioproject
        BioSample           BioSample ID        biosample
        Biosystems          BSID                biosystems
        Books               Book ID             books
        Conserved Domains   PSSM-ID             cdd
        dbGaP               dbGap ID            gap
        dbVar               dbVar ID            dbvar
        Epigenomics         Epigenomics ID      epigenomics
        EST                 GI number           nucest
        Gene                Gene ID             gene
        Genome              Genome ID           genome
        GEO Datasets        GDS ID              gds
        GEO Profils         GEO ID              geoprofiles
        GSS                 GI number           nucgss
        HomoloGene          HomoloGene ID       homologene
        MeSH                MeSH ID             mesh
        NCBI C++ Toolkit    Toolkit ID          toolkit
        NCBI Web Site       Web Site ID         ncbisearch
        NLM Catalog         NLM Catalog ID      nlmcatalog
        Nucleotide          GI number           nuccore
        OMIA                OMIA ID             omia
        PopSet              PopSet ID           popset
        Probe               Probe ID            probe
        Protein             GI number           protein
        Protein Clusters    Protein CLuster ID  proteinclusters
        PubChem BioAssay    AID                 pcassay
        PubChem Compound    CID                 pccompound
        PubChem Substance   SID                 pcsubstance
        PubMed              PMID                pubmed
        PubMed Central      PMCID               pmc
        SNP                 rs number           snp
        SRA                 SRA ID              sra
        Structure           MMDB-ID             structure
        Taxonomy            TaxID               taxonomy
        Unigene             Unigene Cluster ID  unigene
        UniSTS              STS ID              unists

"""

    def __init__(self, verbose=False, email="unknown"):

        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        super(EUtils, self).__init__(url=url, name="EUtils", verbose=verbose)

        warning = """

        NCBI recommends that users post no more than three URL requests per second.
        Failure to comply with this policy may result in an IP address being blocked
        from accessing NCBI. If NCBI blocks an IP address, service will not be
        restored unless the developers of the software accessing the E-utilities
        register values of the tool and email parameters with NCBI. The value of
        email will be used only to contact developers if NCBI observes requests
        that violate our policies, and we will attempt such contact prior to blocking
        access.  For more details see http://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.chapter2_table1

        This message will not appear if you set the email as a parameter::

            e = EUtils(email="name@adress")

        """
        self._databases = None
        self.tool = "TransCellAssay"
        self.email = email
        if self.email == "unknown":
            print('\033[0;33m[WARNING]\033[0m', warning)

    def get_databases(self):
        if self._databases is None:
            tmp = self.easyXML(self.http_get(query="einfo.fcgi", frmt='xml'))
            self._databases = sorted([tag.contents[0] for tag in tmp.soup.find_all('dbname')])
        return self._databases

    databases = property(get_databases, doc="Returns list of valid databases")

    def _check_db(self, db):
        if db not in self.databases:
            raise ValueError("You must provide a valid databases from : ", self.databases)

    def _check_frmt(self, frmt):
        if frmt not in ['xml', 'json', 'text']:
            raise ValueError("Unsupported format")

    def _check_ids(self, sid):
        if isinstance(sid, int):
            sid = [sid]
        if isinstance(sid, list):
            sid = ",".join([str(x) for x in sid])
        # If there are commas, let us split, strip spaces and join back the ids
        sid = ",".join([x.strip() for x in sid.split(',') if x.strip() != ""])
        if len(sid.split(",")) > 200:
            raise ValueError("Number of comma separated IDs must be less than 200")
        return sid

    def ESearch(self, db, query):
        """
        Return UIDs that match to request in specific databse
        :param query:
        :param db:
        :return: return UIDs
        """
        pass

    def EGQuery(self, query):
        """
        Return UIDs that match to requests in all database
        :param query:
        :return:
        """
        pass

    def ESummary(self, database, uid):
        """
        Return document Summary of list of UIDs
        :param database:
        :param uid:
        :return: Return DocSum
        """
        pass

    def EInfo(self, database=None):
        """
        Return detailed information about database : indexing fields
        :param database:
        :return:
        """
        if database is not None:
            self._check_db(database)
            url = "einfo.fcgi?db=" + str(database)
        else:
            raise ValueError('Must provided database')

    def EFetch(self, db, uid=None, frmt="text", **kwargs):
        """

        :param db: Database from which to retrieve UIDs, must be a valid entrez database
        :param uid: UID list, limited to 200
        :param frmt: text, xml not good
        :param kwargs: rettype, could be fasta, summar
        """
        pass

    def ELink(self, dbfrom, db, cmd, uid=None):
        """
        The entrez links utility, Responds to a list of UIDs in a given database with either a list of
        related UIDs (and relevancy scores) in the same database or a list of linked
        UIDs in another Entrez database; checks for the existence of a specified link
        from a list of one or more UIDs; creates a hyperlink to the primary LinkOut
        provider for a specific UID and database, or lists LinkOut URLs and attributes
        for multiple UIDs.
        :param db:Database from which to retrieve UIDs. The value must be a valid Entrez database
                name. This is the destination database for the link operation.
        :param dbfrom: Database containing the input UIDs. The value must be a
                valid Entrez database name (default = pubmed). This is the origin database of
                the link operation. If db and dbfrom are set to the same database value, then
                ELink will return computational neighbors within that database. Please see the
                full list of Entrez links for available computational neighbors. Computational
                neighbors have linknames that begin with dbname_dbname (examples:
                protein_protein, pcassay_pcassay_activityneighbor).
        :param uid: Either a single UID or a comma-delimited list of UIDs may be provided.
                All of the UIDs must be from the database specified by db. Limited to 200 Ids
        :param cmd: ELink command mode. The command mode specified which
                function ELink will perform. Some optional parameters only function for certain
                values of cmd (see http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink).
                Examples are neighbor, prlinks.
        :return:
        """
        pass

    def ESpell(self, db, term, **kwargs):
        """
        Retrieve spelling suggestions for a text query in a given databse
        :param db: database to search
        :param term: entrez query text, url encoded
        :param kwargs:
        """
        pass

    def EPost(self, db, uid, **kwargs):
        """
        Accepts a list of UIDs from a given database, store the set on the history server, and responds with a query
        key and web env fro the uploaded dataset
        :param db: valid databse
        :param uid: list of string of string
        :param kwargs:
        """
        pass


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class EUtilsParser(AttrDict):
    """
    Convert xml returned by EUtils into a structure easier to manipulate
    Tested and used for EInfo,
    Does not work for Esummary
    """
    def __init__(self, xml):
        super(EUtilsParser, self).__init__()
        try:
            children = xml.root.getchildren()[0].getchildren()
            self.__name = xml.root.getchildren()[0].tag
        except:
            children = xml.getchildren()

        for i, child in enumerate(children):
            if len(child.getchildren()) == 0:
                self[child.tag] = child.text
            else:
                # This is probably a list then
                self[child.tag] = []
                for subchild in child.getchildren():
                    self[child.tag].append(EUtilsParser(subchild))
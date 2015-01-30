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
import webbrowser


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

    def __init__(self, verbose=False, email="unknown"):
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        super(EUtils, self).__init__(url=url, name="EUtils", verbose=verbose)
        self._verbose = verbose
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
            tmp = self.easyXML(self.http_get(query="einfo.fcgi?", frmt='xml'))
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

    @staticmethod
    def open_query_doc():
        """
        Open in brower documentation for making query
        :return:
        """
        webbrowser.open('http://www.ncbi.nlm.nih.gov/books/NBK25499/')

    @staticmethod
    def _format_param(param, value):
        """
        Format a required/optionnal parameter to query :
        &param=value
        :param param: parameter
        :param value: value
        :return: return str query
        """
        return '&' + str(param) + '=' + str(value)

    def _add_email_tools(self):
        txt = str()
        if self.email is not None:
            txt += self._format_param('email', self.email)
        txt += self._format_param('tool', self.tool)
        return txt

    def ESearch(self, db, term, retmode='xml', **kwargs):
        """
        Return UIDs that match to request in specific database
        :param db:
        :param term:
        :return: return UIDs
        """
        _valid_opt_param = ['usehistory', 'WebEnv', 'query_key', 'retstart', 'retmax', 'rettype', 'sort', 'field',
                            'datatype', 'reldata' 'mindata', 'maxdate']

        url = 'esearch.fcgi?' + self._format_param('db', db) + self._format_param('term', term) + \
              self._format_param('retmode', retmode)
        for key, value in kwargs:
            if key in _valid_opt_param:
                url += self._format_param(key, value)
        if retmode is 'xml':
            res = self.easyXML(self.http_get(url, frmt='xml'))
        else:
            res = self.http_get(url)
        return res

    def EGQuery(self, term):
        """
        Return UIDs that match to requests in all database
        :param term: Entrez text query. All special characters must be URL encoded. Spaces may be replaced by '+'
            signs. For very long queries (more than hundred characters long), consider using HTTP POST call
        :return:
        """
        url = 'egquery.fcgi?' + self._format_param('term', term)
        res = self.easyXML(self.http_get(url, frmt='xml'))
        return res

    def ESummary(self, db, id, retmode='xml', **kwargs):
        """
        Return document Summary of list of UIDs
        :param db:
        :param id:
        :param retmode:
        :return: Return DocSum
        """
        _valid_opt_param = ['query_key', 'WebEnv', 'retstart', 'retmax']
        url = 'esummary.fcgi?' + self._format_param('db', db) + self._format_param('id', id) + \
              self._format_param('retmode', retmode)
        for key, value in kwargs:
            if key in _valid_opt_param:
                url += self._format_param(key, value)
        res = self.easyXML(self.http_get(url, frmt='xml'))
        return res

    def EInfo(self, db=None, retmode='xml'):
        """
        Return detailed information about database : indexing fields
        :param db: database to get info
        :param retmode: xml or json
        :return: Return xml doc with field list, use with EutilsParser
        """
        if db is None:
            raise ValueError('Need a database name')
        else:
            self._check_db(db)
            url = "einfo.fcgi?" + self._format_param('db', db) + self._add_email_tools()
            if retmode is 'xml':
                res = self.easyXML(self.http_get(url, frmt=retmode))
            elif retmode is 'json':
                url += self._format_param('retmode', retmode)
                res = self.http_get(url, frmt=retmode)
            return res

    def EFetch(self, db, id=None, **kwargs):
        """
        Return formatted data records for a list of input id
        :param db: Database from which to retrieve UIDs, must be a valid entrez database
        :param id: UID list, limited to 200
        :param kwargs: rettype, could be fasta, summar
        """
        _valid_opt_param = ['query_key', 'WebEnv', 'retmode', 'rettype', 'retstart', 'retmax', 'strand', 'seq_start',
                            'seq_stop', 'complexity']
        url = 'efetch.fcgi?' + self._format_param('db', db) + self._format_param('id', id)
        for key, value in kwargs:
            if key in _valid_opt_param:
                url += self._format_param(key, value)
        res = self.http_get(url)
        return res

    def ELink(self, db, dbfrom, cmd, id=None, **kwargs):
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
        :param id: Either a single UID or a comma-delimited list of UIDs may be provided.
                All of the UIDs must be from the database specified by db. Limited to 200 Ids
        :param cmd: ELink command mode. The command mode specified which
                function ELink will perform. Some optional parameters only function for certain
                values of cmd (see http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink).
                Examples are neighbor, prlinks.
        :param kwargs:
        :return:
        """
        _valid_cmd = ['neighbor', 'neighbor_score', 'neighbor_history', 'acheck', 'ncheck', 'lcheck', 'llinks',
                      'llinkslib', 'prlinks']
        _valid_opt_param = ['query_key', 'WebEnv', 'linkname', 'term', 'holding', 'datetype', 'reldate', 'mindata',
                            'maxdata']
        url = 'elink.fcgi?' + self._format_param('db', db) + self._format_param('dbfrom', dbfrom) + \
              self._format_param('id', id)
        if cmd in _valid_cmd:
            url += self._format_param('cmd', cmd)
        for key, value in kwargs:
            if key in _valid_opt_param:
                url += self._format_param(key, value)
        res = self.easyXML(self.http_get(url, frmt='xml'))
        return res

    def ESpell(self, db, term):
        """
        Retrieve spelling suggestions for a text query in a given databse
        :param db: database to search
        :param term: entrez query text, url encoded
        """
        url = 'espell.fcgi?' + self._format_param('db', db) + self._format_param('term', term)
        res = self.easyXML(self.http_get(url, frmt='xml'))
        return res

    def EPost(self, db, id, **kwargs):
        """
        Accepts a list of UIDs from a given database, store the set on the history server, and responds with a query
        key and web env fro the uploaded dataset
        :param db: valid databse
        :param id: list of string of string
        :param kwargs:
        """
        _valid_opt_param = ['query_key', 'WebEnv']
        url = 'epost.fcgi?' + self._format_param('db', db) + self._format_param('id', id)
        for key, value in kwargs.items():
            if key in _valid_opt_param:
                url += self._format_param(key, value)
        res = self.easyXML(self.http_get(url, frmt='xml'))
        return res

    def ECitMatch(self, db, bdata, retmode='xml'):
        """
        Retrieve PubMed IDs (PMIDs) that correspond to a set of input citation strings.
        :param db: database to search
        :param retmode: xml
        :param bdata: Citation strings
        """
        url = 'ecitmatch.cgi?' + self._format_param('db', db) + self._format_param('bdata', bdata) +\
              self._format_param('retmode', retmode)
        res = self.easyXML(self.http_get(url, frmt=retmode))
        return res


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class EUtilsParser(AttrDict):
    """
    Convert xml returned by EUtils into a structure easier to manipulate
    Tested and used for EInfo, for discoving Field for each database
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

    def __str__(self):
        name = self._EUtilsParser__name
        if name == "DbInfo":
            txt = ""
            for this in self.FieldList:
                txt += "{0:10}:  {1}\n".format(this.Name, this.Description)
            return txt
        else:
            print("Not implemented for {0}".format(name))
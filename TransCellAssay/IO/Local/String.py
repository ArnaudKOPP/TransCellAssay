__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import os
import shutil
import gzip
import csv
import sqlite3
import posixpath
import textwrap
import urllib.request
from TransCellAssay.Utils.utils import reporthook
from collections import namedtuple
from operator import itemgetter


class STRING(object):
    """
    Access `STRING <http://www.string-db.org/>`_ PPI database.
    """

    DATABASE_SCHEMA = """\
    Database schema
    ---------------
    table `links`:
        - `protein_id1`: id (text)
        - `protein_id2`: id (text)
        - `score`: combined score (int)

    table `actions`:
        - `protein_id1`: id (text)
        - `protein_id2`: id (text)
        - `mode`: mode (text)
        - `action`: action type (text)
        - `score`: action score (int)

    table `proteins`:
        - `protein_id`: protein id in STRING (text) (in the form of {taxid}.{name})
        - `taxid`: organism taxid (text)

    table `aliases`:
        - `protein_id: id (text)
        - `alias`: protein alias (text)
        - `source`: protein alias source (text)

    """
    FILENAME = "string.protein.{taxid}.sqlite"

    # Homo sapiens and mus musculus default id
    TAXID_MAP = ("9606", "10090")

    def __init__(self, taxid=None, database=None):
        if taxid is not None and database is not None:
            raise ValueError("taxid and database parameters are exclusive.")

        self.db = None

        if taxid is None and database is not None:
            if isinstance(database, sqlite3.Connection):
                self.db = database
                self.filename = None
            else:
                self.filename = database
                self.db = sqlite3.connect(database)
        elif taxid is not None and database is None:
            self.filename = self.FILENAME.format(taxid=taxid)
        elif taxid is None and database is None:
            # Back compatibility
            self.filename = "string-protein.sqlite"
        else:
            assert False, "Not reachable"

        if self.db is None:
            self.db = sqlite3.connect(self.filename)

    @classmethod
    def default_db_filename(cls, taxid):
        return cls.FILENAME.format(taxid=taxid)

    @classmethod
    def defaults_taxids(cls):
        return cls.TAXID_MAP

    def organisms(self):
        """
        Return all organism taxids contained in this database.
        """
        cur = self.db.execute("select distinct taxid from proteins")
        return [r[0] for r in cur.fetchall()]

    def ids(self, taxid=None):
        """
        Return a list of all protein ids. If `taxid` is not None limit
        the results to ids from this organism only.

        """
        if taxid is not None:
            cur = self.db.execute("""\
                select protein_id
                from proteins
                where taxid=?
                """, (taxid,))
        else:
            cur = self.db.execute("""\
                select protein_id
                from proteins
                """)
        return [r[0] for r in cur.fetchall()]

    def synonyms(self, id):
        """
        Return a list of synonyms for primary `id` as reported by STRING
        (proteins.aliases.{version}.txt file)
        """
        cur = self.db.execute("""\
            select alias
            from aliases
            where protein_id=?
            """, (id,))
        res = cur.fetchall()
        return [r[0] for r in res]

    def synonyms_with_source(self, id):
        """
        Return a list of synonyms for primary `id` along with its
        source as reported by STRING (proteins.aliases.{version}.txt file)

        """
        cur = self.db.execute("""\
            select alias, source
            from aliases
            where protein_id=?
            """, (id,))
        res = cur.fetchall()
        return [(syn, set(source.split(" "))) \
                for syn, source in res]

    def all_edges(self, taxid=None):
        """
        Return a list of all edges. If taxid is not None return the edges
        for this organism only.

        .. note:: This may take some time (and memory).

        """
        if taxid is not None:
            cur = self.db.execute("""\
                select links.protein_id1, links.protein_id2, score
                from links join proteins on
                    links.protein_id1=proteins.protein_id
                where taxid=?
                """, (taxid,))
        else:
            cur = self.db.execute("""\
                select protein_id1, protein_id1, score
                from links
                """)
        return cur.fetchall()

    def edges(self, id):
        """
        Return a list of all edges (a list of 3-tuples (id1, id2, score)).
        """
        cur = self.db.execute("""\
            select protein_id1, protein_id2, score
            from links
            where protein_id1=?
            """, (id,))
        return cur.fetchall()

    def all_edges_annotated(self, taxid=None):
        res = []
        for id in self.ids(taxid):
            res.extend(self.edges_annotated(id))
        return res

    def edges_annotated(self, id):
        cur = self.db.execute("""\
            select links.protein_id1, links.protein_id2, links.score,
                   actions.action, actions.mode, actions.score
            from links left join actions on
                   links.protein_id1=actions.protein_id1 and
                   links.protein_id2=actions.protein_id2
            where links.protein_id1=?
        """, (id,))
        return map(STRINGInteraction._make, cur.fetchall())

    def search_id(self, name, taxid=None):
        if taxid is None:
            cur = self.db.execute("""\
                select proteins.protein_id
                from proteins natural join aliases
                where aliases.alias=?
            """, (name,))
        else:
            cur = self.db.execute("""\
                select proteins.protein_id
                from proteins natural join aliases
                where aliases.alias=? and proteins.taxid=?
            """, (name, taxid))
        return map(itemgetter(0), cur)

    @classmethod
    def download_data(cls, version, taxids=None):
        """
        Download the  PPI data for local work (this may take some time).
        Pass the version of the  STRING release e.g. v9.1.
        """
        if taxids is None:
            taxids = cls.defaults_taxids()

        for taxid in taxids:
            cls.init_db(version, taxid)

    @classmethod
    def init_db(cls, version, taxid, cache_dir=None, dbfilename=None):
        if cache_dir is None:
            cache_dir = os.path.join(os.path.curdir, "TMP")

        if dbfilename is None:
            dbfilename = cls.default_db_filename(taxid)

        pjoin = os.path.join

        base_url = "http://www.string-db.org/newstring_download/"

        def paths(flatfile):
            url = "{flatfile}.{version}/{taxid}.{flatfile}.{version}.txt.gz"
            url = url.format(flatfile=flatfile, version=version, taxid=taxid)
            return posixpath.basename(url), base_url + url

        def ffname(pattern):
            return pattern.format(taxid=taxid, version=version)

        links_filename, links_url = paths("protein.links")

        actions_filename, actions_url = paths("protein.actions")

        aliases_filename, aliases_url = paths("protein.aliases")

        def download(filename, url):
            with open(pjoin(cache_dir, filename + ".tmp"), "wb") as dest:
                urllib.request.urlretrieve(url=url, filename=dest, reporthook=reporthook)

            shutil.move(pjoin(cache_dir, filename + ".tmp"),
                        pjoin(cache_dir, filename))

        for fname, url in [(links_filename, links_url),
                           (actions_filename, actions_url),
                           (aliases_filename, aliases_url)]:
            if not os.path.exists(pjoin(cache_dir, fname)):
                download(fname, url)

        links_fileobj = open(pjoin(cache_dir, links_filename), "rb")
        actions_fileobj = open(pjoin(cache_dir, actions_filename), "rb")
        aliases_fileobj = open(pjoin(cache_dir, aliases_filename), "rb")

        links_file = gzip.GzipFile(fileobj=links_fileobj)
        actions_file = gzip.GzipFile(fileobj=actions_fileobj)
        aliases_file = gzip.GzipFile(fileobj=aliases_fileobj)

        con = sqlite3.connect(dbfilename)

        with con:
            cls.clear_db(con)

            links_file.readline()  # read the header line

            reader = csv.reader(links_file, delimiter=" ")

            def read_links(reader):
                for i, (p1, p2, score) in enumerate(reader):
                    yield p1, p2, int(score)

            con.executemany("INSERT INTO links VALUES (?, ?, ?)",
                            read_links(reader))

            def part(string, sep, part):
                return string.split(sep)[part]

            con.create_function("part", 3, part)
            con.execute("""
                INSERT INTO proteins
                SELECT protein_id1, part(protein_id1, '.', 0)
                FROM (SELECT DISTINCT(protein_id1)
                     FROM links
                     ORDER BY protein_id1)
            """)

            actions_file.readline()  # read header line

            reader = csv.reader(actions_file, delimiter="\t")

            def read_actions(reader):
                for i, (p1, p2, mode, action, a_is_acting, score) in \
                        enumerate(reader):
                    yield p1, p2, mode, action, int(score)

            con.executemany("INSERT INTO actions VALUES (?, ?, ?, ?, ?)",
                            read_actions(reader))

            aliases_file.readline()  # read header line

            reader = csv.reader(aliases_file, delimiter="\t")

            def read_aliases(reader):
                for i, (taxid, name, alias, source) in enumerate(reader):
                    yield (".".join([taxid, name]),
                           alias.decode("utf-8", errors="ignore"),
                           source.decode("utf-8", errors="ignore"))

            con.executemany("INSERT INTO aliases VALUES (?, ?, ?)",
                            read_aliases(reader, ))

            print("Indexing the database")
            cls.create_db_index(con)

            con.executescript("""
                DROP TABLE IF EXISTS version;
                CREATE TABLE version (
                     string_version text,
                     api_version text
                );""")

            con.execute("""
                INSERT INTO version
                VALUES (?, ?)""", (version, cls.VERSION))

    @classmethod
    def clear_db(cls, dbcon):
        dbcon.executescript(textwrap.dedent("""
            DROP TABLE IF EXISTS links;
            DROP TABLE IF EXISTS proteins;
            DROP TABLE IF EXISTS actions;
            DROP TABLE IF EXISTS aliases;
        """))

        dbcon.executescript(textwrap.dedent("""
            CREATE TABLE links
                (protein_id1 TEXT, protein_id2 TEXT, score INT);

            CREATE TABLE proteins
                (protein_id TEXT, taxid TEXT);

            CREATE TABLE actions
                (protein_id1 TEXT, protein_id2 TEXT, mode TEXT,
                 action TEXT, score INT);

            CREATE TABLE aliases
                (protein_id TEXT, alias TEXT, source TEXT);
        """))

    @classmethod
    def create_db_index(cls, dbcon):
        dbcon.executescript(textwrap.dedent("""
            CREATE INDEX IF NOT EXISTS index_link_protein_id1
                ON links (protein_id1);

            CREATE INDEX IF NOT EXISTS index_action_protein_id1
                ON actions (protein_id1);

            CREATE INDEX IF NOT EXISTS index_proteins_id
                ON proteins (protein_id);

            CREATE INDEX IF NOT EXISTS index_taxids
                ON proteins (taxid);

            CREATE INDEX IF NOT EXISTS index_aliases_id
                ON aliases (protein_id);

            CREATE INDEX IF NOT EXISTS index_aliases_alias
                ON aliases (alias);
        """))


STRINGInteraction = namedtuple(
    "STRINGInteraciton",
    ["protein_id1",
     "protein_id2",
     "combined_score",
     "mode",
     "action",
     "score"]
)

STRINGDetailedInteraction = namedtuple(
    "STRINGDetailedInteraction",
    ["protein_id1",
     "protein_id2",
     "combined_score",
     "mode",
     "action",
     "score",
     "neighborhood",
     "fusion",
     "cooccurence",
     "coexpression",
     "experimental",
     "database",
     "textmining"]
)


class STRINGDetailed(STRING):
    """
    Access `STRING <http://www.string-db.org/>`_ PPI database.
    This class also allows access to subscores per channel.

    .. note::
        This data is released under a `Creative Commons
        Attribution-Noncommercial-Share Alike 3.0 License
        <http://creativecommons.org/licenses/by-nc-sa/3.0/>`_.

        If you want to use this data for commercial purposes you must
        get a license from STRING.

    """

    DATABASE_SCHEMA = """\
    DATABASE SCHEMA
    ===============

    table `evidence`:
        - `protein_id1`: protein id (text)
        - `protein_id2`: protein id (text)
        - `neighborhood`: score (int)
        - `fusion`: score (int)
        - `cooccurence`: score (int)
        - `coexpression`: score (int)
        - `experimental`: score (int)
        - `database`: score (int)
        - `textmining`: score (int)

    """
    FILENAME_DETAILED = "string.protein.detailed.{taxid}.sqlite"

    def __init__(self, taxid=None, database=None, detailed_database=None):
        STRING.__init__(self, taxid, database)
        if taxid is not None and detailed_database is not None:
            raise ValueError("taxid and detailed_database are exclusive")

        db_file = self.FILENAME
        if taxid is not None and detailed_database is None:
            detailed_database = self.FILENAME_DETAILED.format(taxid=taxid)
        elif taxid is None and detailed_database is not None:
            detailed_database = detailed_database
        elif taxid is None and detailed_database is None:
            # Back compatibility
            detailed_database = "string-protein-detailed.sqlite"

        self.db_detailed = sqlite3.connect(detailed_database)
        self.db_detailed.execute("ATTACH DATABASE ? as string", (db_file,))

    def edges_annotated(self, id):
        edges = STRING.edges_annotated(self, id)
        edges_nc = []
        for edge in edges:
            id1, id2 = edge.protein_id1, edge.protein_id2
            cur = self.db_detailed.execute("""
                SELECT neighborhood, fusion, cooccurence, coexpression,
                       experimental, database, textmining
                FROM evidence
                WHERE protein_id1=? AND protein_id2=?
                """, (id1, id2))
            res = cur.fetchone()
            if res:
                evidence = res
            else:
                evidence = [0] * 7
            edges_nc.append(
                STRINGDetailedInteraction(*(tuple(edge) + tuple(evidence)))
            )
        return edges_nc

    @classmethod
    def init_db(cls, version, taxid, cache_dir=None, dbfilename=None):
        if cache_dir is None:
            cache_dir = os.path.join(os.path.curdir, "TMP")
        if dbfilename is None:
            dbfilename = "string-protein-detailed.{taxid}.sqlite".format(taxid=taxid)

        pjoin = os.path.join

        base_url = "http://www.string-db.org/newstring_download/"
        filename = "{taxid}.protein.links.detailed.{version}.txt.gz"
        filename = filename.format(version=version, taxid=taxid)
        url = base_url + "protein.links.detailed.{version}/" + filename
        url = url.format(version=version)

        if not os.path.exists(pjoin(cache_dir, filename)):
            urllib.request.urlretrieve(url=url, filename=filename, reporthook=reporthook)

        links_fileobj = open(pjoin(cache_dir, filename), "rb")
        links_file = gzip.GzipFile(fileobj=links_fileobj)

        con = sqlite3.connect(dbfilename)
        with con:
            con.execute("""
                DROP TABLE IF EXISTS evidence
            """)

            con.execute("""
                CREATE TABLE evidence(
                     protein_id1 TEXT,
                     protein_id2 TEXT,
                     neighborhood INTEGER,
                     fusion INTEGER,
                     cooccurence INTEGER,
                     coexpression INTEGER,
                     experimental INTEGER,
                     database INTEGER,
                     textmining INTEGER
                    )
                """)

            links = csv.reader(links_file, delimiter=" ")
            links.next()  # Read header
            filesize = os.stat(pjoin(cache_dir, filename)).st_size

            def read_links(reader):
                for i, (p1, p2, n, f, c, cx, ex, db, t, _) in \
                        enumerate(reader):
                    yield p1, p2, n, f, c, cx, ex, db, t

            con.executemany("""
                INSERT INTO evidence
                VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, read_links(links))

            print("Indexing")
            con.execute("""\
                CREATE INDEX IF NOT EXISTS index_evidence
                    ON evidence (protein_id1, protein_id2)
            """)

            con.executescript("""
                DROP TABLE IF EXISTS version;

                CREATE TABLE version (
                     string_version text,
                     api_version text
                );
                """)

            con.execute("""
                INSERT INTO version
                VALUES (?, ?)""", (version, cls.VERSION))

    @classmethod
    def download_data(cls, version, taxids=None):
        if taxids is None:
            taxids = cls.defaults_taxids()

        for taxid in taxids:
            cls.init_db(version, taxid)
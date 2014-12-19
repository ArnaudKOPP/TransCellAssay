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
import zipfile
import csv
import sqlite3
from io import StringIO
from collections import namedtuple
from operator import itemgetter
import urllib.request
from TransCellAssay.Utils.utils import reporthook


class BioGRID(object):
    """
    Access `BioGRID <http://thebiogrid.org>`_ PPI data.
    Example ::
    biogrid = BioGRID()
    print biogrid.organism() # Print a list of all organism ncbi taxis in BioGRID
    print biogrid.ids(taxid="9606") # Print a set of all human protein ids
    print biogrid.synonyms("110004") # Print a list of all synonyms for protein id '110004' as reported by BioGRID
    """

    SCHEMA = [
        ("links",
         """\
         biogrid_interaction_id text,
         biogrid_id_interactor_a text,
         biogrid_id_interactor_b text,
         experimental_system text,
         experimental_system_type text,
         author text,
         pubmed_id text,
         throughput text,
         score real,
         modification text,
         phenotypes text,
         qualifications text,
         tags text,
         source_database text
         """),
        ("proteins",
         """\
         biogrid_id_interactor text,
         entrez_gene_interactor text,
         systematic_name_interactor text,
         official_symbol_interactor text,
         synonyms_interactor text,
         organism_interactor text,
         """)
    ]

    # All column names in the BioGRID tab2 source table.
    FIELDS = ['biogrid_interaction_id',
              'entrez_gene_interactor_a',
              'entrez_gene_interactor_b',
              'biogrid_id_interactor_a',
              'biogrid_id_interactor_b',
              'systematic_name_interactor_a',
              'systematic_name_interactor_b',
              'official_symbol_interactor_a',
              'official_symbol_interactor_b',
              'synonyms_interactor_a',
              'synonyms_interactor_b',
              'experimental_system',
              'experimental_system_type',
              'author',
              'pubmed_id',
              'organism_interactor_a',
              'organism_interactor_b',
              'throughput',
              'score',
              'modification',
              'phenotypes',
              'qualifications',
              'tags',
              'source_database'
    ]

    SERVER_FILE = "BIOGRID-ALL.sqlite"

    def __init__(self):
        self.filename = "BIOGRID-ALL.sqlite"
        if not os.path.isfile(self.filename):
            self.download_data()
        self.db = sqlite3.connect(self.filename)
        self.init_db_index()

    def organisms(self):
        cur = self.db.execute("select distinct organism_interactor from proteins")
        return map(itemgetter(0), cur.fetchall())

    def ids(self, taxid=None):
        """
        Return a list of all protein ids (biogrid_id_interactors).
        If `taxid` is not None limit the results to ids from this organism
        only.

        """
        if taxid is None:
            cur = self.db.execute("""select biogrid_id_interactor from proteins""")
        else:
            cur = self.db.execute("""\
                select biogrid_id_interactor from proteins where organism_interactor=?""", (taxid,))

        return [t[0] for t in cur.fetchall()]

    def synonyms(self, id):
        """
        Return a list of synonyms for primary `id`.
        """
        cur = self.db.execute("""\
            select entrez_gene_interactor,
                   systematic_name_interactor,
                   official_symbol_interactor,
                   synonyms_interactor
            from proteins
            where biogrid_id_interactor=?""",
                              (id,))
        rec = cur.fetchone()
        if rec:
            synonyms = list(rec[:-1]) + \
                       (rec[-1].split("|") if rec[-1] is not None else [])
            return [s for s in synonyms if s is not None]
        else:
            return []

    def all_edges(self, taxid=None):
        """
        Return a list of all edges. If taxid is not None return the
        edges for this organism only.

        """
        if taxid is not None:
            cur = self.db.execute("""\
                select biogrid_id_interactor_a, biogrid_id_interactor_a, score
                from links left join proteins on
                    biogrid_id_interactor_a=biogrid_id_interactor or
                    biogrid_id_interactor_b=biogrid_id_interactor
                where organism_interactor=?
            """, (taxid,))
        else:
            cur = self.db.execute("""\
                select biogrid_id_interactor_a, biogrid_id_interactor_a, score
                from links
            """)
        edges = cur.fetchall()
        return edges

    def edges(self, id):
        """
        Return a list of all interactions where id is a participant
        (a list of 3-tuples (id_a, id_b, score)).

        """

        cur = self.db.execute("""\
            select biogrid_id_interactor_a, biogrid_id_interactor_b, score
            from links
            where biogrid_id_interactor_a=? or biogrid_id_interactor_b=?
        """, (id, id))
        return cur.fetchall()

    def all_edges_annotated(self, taxid=None):
        """
        Return a list of all edges annotated. If taxid is not None
        return the edges for this organism only.

        """
        if taxid is not None:
            cur = self.db.execute("""\
                select *
                from links left join proteins on
                    biogrid_id_interactor_a=biogrid_id_interactor or
                    biogrid_id_interactor_b=biogrid_id_interactor
                where organism_interactor=?
            """, (taxid,))
        else:
            cur = self.db.execute("""\
                select *
                from links
            """)
        edges = cur.fetchall()
        return edges

    def edges_annotated(self, id):
        """ Return a list of all links
        """
        cur = self.db.execute("""\
            select *
            from links
            where biogrid_id_interactor_a=? or biogrid_id_interactor_b=?
        """, (id, id))
        return cur.fetchall()

    def search_id(self, name, taxid=None):
        """
        Search the database for protein name. Return a list of matching
        primary ids. Use `taxid` to limit the results to a single organism.

        """
        # TODO: synonyms_interactor can contain multiple synonyms
        # (should create an indexed table of synonyms)
        if taxid is None:
            cur = self.db.execute("""\
                select biogrid_id_interactor
                from proteins
                where (biogrid_id_interactor=? or
                       entrez_gene_interactor=? or
                       systematic_name_interactor=? or
                       official_symbol_interactor=? or
                       synonyms_interactor=?)
            """, ((name,) * 5))
        else:
            cur = self.db.execute("""\
                select biogrid_id_interactor
                from proteins
                where (biogrid_id_interactor=? or
                       entrez_gene_interactor=? or
                       systematic_name_interactor=? or
                       official_symbol_interactor=? or
                       synonyms_interactor=?)
                      and organism_interactor=?
            """, ((name,) * 5) + (taxid,))
        res = map(itemgetter(0), cur)
        return res

    @classmethod
    def download_data(cls, address=None):
        """
        Pass the address of the latest BIOGRID-ALL release (in tab2 format).
        """
        if address is None:
            address = "http://thebiogrid.org/downloads/archives/Latest%20Release/BIOGRID-ALL-LATEST.tab2.zip"
        try:
            urllib.request.urlretrieve(address, filename="BIOGRID-ALL.tab2", reporthook=reporthook)
        except IOError:
            raise IOError

        stream = urllib.request.urlopen(address)
        stream = StringIO(stream.read())
        zfile = zipfile.ZipFile(stream)
        # Expecting only one file.
        filename = zfile.namelist()[0]

        with open(filename, "wb") as f:
            shutil.copyfileobj(zfile.open(filename, "r"), f)

        cls.init_db(filename)

    @classmethod
    def init_db(cls, filepath):
        """
        Initialize the sqlite data base from a BIOGRID-ALL.*tab2.txt file
        format.

        """
        dirname = os.path.dirname(filepath)
        rows = csv.reader(open(filepath, "rb"), delimiter="\t")
        rows.next()  # read the header line

        con = sqlite3.connect(os.path.join(dirname, BioGRID.SERVER_FILE))
        con.execute("drop table if exists links")  # Drop old table
        con.execute("drop table if exists proteins")  # Drop old table

        con.execute("""\
            create table links (
                biogrid_interaction_id text,
                biogrid_id_interactor_a text,
                biogrid_id_interactor_b text,
                experimental_system text,
                experimental_system_type text,
                author text,
                pubmed_id text,
                throughput text,
                score real,
                modification text,
                phenotypes text,
                qualifications text,
                tags text,
                source_database text
            )""")

        con.execute("""\
            create table proteins (
                biogrid_id_interactor text,
                entrez_gene_interactor text,
                systematic_name_interactor text,
                official_symbol_interactor text,
                synonyms_interactor text,
                organism_interactor text
            )""")

        proteins = {}

        # Values that go in the links table
        link_indices = [0, 3, 4, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23]
        # Values that go in the proteins table
        interactor_a_indices = [3, 1, 5, 7, 9, 15]
        # Values that go in the proteins table
        interactor_b_indices = [4, 2, 6, 8, 10, 16]

        def to_none(val):
            return None if val == "-" else val

        def processlinks(rowiter):
            for row in rowiter:
                fields = map(to_none, row)
                yield [fields[i] for i in link_indices]

                interactor_a = [fields[i] for i in interactor_a_indices]
                interactor_b = [fields[i] for i in interactor_b_indices]
                proteins[interactor_a[0]] = interactor_a
                proteins[interactor_b[0]] = interactor_b

        con.executemany("""
            insert into links values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, processlinks(rows))

        con.executemany("""\
            insert into proteins values (?, ?, ?, ?, ?, ?)
            """, proteins.itervalues())
        con.commit()
        con.close()

    def init_db_index(self):
        """
        Will create an indexes (if not already present) in the database
        for faster searching by primary ids.

        """
        self.db.execute("""\
        create index if not exists index_on_biogrid_id_interactor_a
           on links (biogrid_id_interactor_a)
        """)
        self.db.execute("""\
        create index if not exists index_on_biogrid_id_interactor_b
           on links (biogrid_id_interactor_b)
        """)
        self.db.execute("""\
        create index if not exists index_on_biogrid_id_interactor
           on proteins (biogrid_id_interactor)
        """)


STRINGInteraction = namedtuple(
    "STRINGInteraciton",
    ["protein_id1",
     "protein_id2",
     "combined_score",
     "mode",
     "action",
     "score"]
)
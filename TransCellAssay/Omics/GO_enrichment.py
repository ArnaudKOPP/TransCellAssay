"""
Go enrichement
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import collections
import numpy as np
import scipy.stats
import pandas as pd
import urllib.request

typedef_tag, term_tag = "[Typedef]", "[Term]"


def after_colon(line):
    # macro for getting anything after the :
    return line.split(":", 1)[1].strip()


def read_until(handle, start):
    # read each line until it has a certain start, and then puts
    # the start tag back
    while 1:
        pos = handle.tell()
        line = handle.readline()
        if not line:
            break
        if line.startswith(start):
            handle.seek(pos)
            return
    raise EOFError("%s tag cannot be found" % start)


class OBOreader():
    """
    Parse obo file
    """

    def __init__(self, obo_file="gene_ontology.1_2.obo"):
        try:
            self._handle = open(obo_file)
        except IOError:
            self._handle = urllib.request.urlretrieve(
                "http://geneontology.org/ontology/obo_format_1_2/gene_ontology.1_2.obo", "gene_ontology.1_2.obo")

    def __iter__(self):
        line = self._handle.readline()
        if not line.startswith(term_tag):
            read_until(self._handle, term_tag)
        while 1:
            yield self.next()

    def next(self):
        lines = []
        line = self._handle.readline()
        if not line or line.startswith(typedef_tag):
            raise StopIteration

        # read until the next tag and save everything in between
        while 1:
            pos = self._handle.tell()  # save current postion for roll-back
            line = self._handle.readline()
            if not line or (line.startswith(typedef_tag)
                            or line.startswith(term_tag)):
                self._handle.seek(pos)  # roll-back
                break
            lines.append(line)

        rec = GOTerm()
        for line in lines:
            if line.startswith("id:"):
                rec.id = after_colon(line)
            if line.startswith("alt_id:"):
                rec.alt_ids.append(after_colon(line))
            elif line.startswith("name:"):
                rec.name = after_colon(line)
            elif line.startswith("namespace:"):
                rec.namespace = after_colon(line)
            elif line.startswith("is_a:"):
                rec._parents.append(after_colon(line).split()[0])
            elif line.startswith("is_obsolete:") and after_colon(line) == "true":
                rec.is_obsolete = True

        return rec


class GOTerm:
    """
    Go term, contain a lot more attribut than interfaced here
    """

    def __init__(self):
        self.id = ""  # GO:xxxxxx
        self.name = ""  # description
        self.namespace = ""  # BP, CC, MF
        self._parents = []  # is_a basestring of parents
        self.parents = []  # parent records
        self.children = []  # children records
        self.level = -1  # distance from root node
        self.is_obsolete = False  # is_obsolete
        self.alt_ids = []  # alternative identifiers

    def __str__(self):
        obsolete = "obsolete" if self.is_obsolete else ""
        return "%s\tlevel-%02d\t%s [%s] %s" % (self.id, self.level, self.name,
                                               self.namespace, obsolete)

    def __repr__(self):
        return "GOTerm('%s')" % (self.id)

    def has_parent(self, term):
        for p in self.parents:
            if p.id == term or p.has_parent(term):
                return True
        return False

    def has_child(self, term):
        for p in self.children:
            if p.id == term or p.has_child(term):
                return True
        return False

    def get_all_parents(self):
        all_parents = set()
        for p in self.parents:
            all_parents.add(p.id)
            all_parents |= p.get_all_parents()
        return all_parents

    def get_all_children(self):
        all_children = set()
        for p in self.children:
            all_children.add(p.id)
            all_children |= p.get_all_children()
        return all_children

    def get_all_parent_edges(self):
        all_parent_edges = set()
        for p in self.parents:
            all_parent_edges.add((self.id, p.id))
            all_parent_edges |= p.get_all_parent_edges()
        return all_parent_edges

    def get_all_child_edges(self):
        all_child_edges = set()
        for p in self.children:
            all_child_edges.add((p.id, self.id))
            all_child_edges |= p.get_all_child_edges()
        return all_child_edges


class GO_tree():
    def __init__(self, obo_file="gene_ontology.1_2.obo"):
        self.go_Term = {}
        self.load_obo_file(obo_file)

    def load_obo_file(self, obo_file):
        print("load obo file ", obo_file)
        obo_reader = OBOreader(obo_file)
        for rec in obo_reader:
            self.go_Term[rec.id] = rec
            for alt in rec.alt_ids:
                self.go_Term[alt] = rec

        self.populate_terms()
        print("All GO nodes imported : ", len(self.go_Term))

    def populate_terms(self):
        def depth(rec):
            if rec.level < 0:
                if not rec.parents:
                    rec.level = 0
                else:
                    rec.level = min(depth(rec) for rec in rec.parents) + 1
            return rec.level

        # make the parents references to the GO terms
        for rec in self.go_Term.items():
            rec = rec[1]
            rec.parents = [self.go_Term[x] for x in rec._parents]

        # populate children and levels
        for rec in self.go_Term.items():
            rec = rec[1]
            for p in rec.parents:
                p.children.append(rec)

            if rec.level < 0:
                depth(rec)

    def print_all_go_id(self):
        for rec_id, rec in sorted(self.go_Term.items()):
            print(rec)

    def query_term(self, term, verbose=True):
        if term not in self.go_Term:
            print("Term %s not found! ", term)
            return

        rec = self.go_Term[term]
        if verbose:
            print("all parents: ", rec.get_all_parents())
            print("all children: ", rec.get_all_children())

        return rec

    def paths_to_top(self, term):
        if term not in self.go_Term:
            print("Term %s not found!", term)
            return

        def _paths_to_top_recursive(rec):
            if rec.level == 0:
                return [[rec]]
            paths = []
            for parent in rec.parents:
                top_paths = _paths_to_top_recursive(parent)
                for top_path in top_paths:
                    top_path.append(rec)
                    paths.append(top_path)
            return paths

        go_term = self.go_Term[term]
        return _paths_to_top_recursive(go_term)

    def _label_wrap(self, label):
        wrapped_label = r"%s\n%s" % (label, self.go_Term[label].name.replace(",", r"\n"))
        return wrapped_label

    def update_association(self, association):
        """
        Add parents in association dict
        """
        bad_terms = set()
        print("Update association")
        for key, terms in association.association.items():
            parents = set()
            for term in terms:
                try:
                    parents.update(self.go_Term[term].get_all_parents())
                except:
                    bad_terms.add(term)
            terms.update(parents)
        if bad_terms:
            print("terms not found: ", bad_terms)


class Association():
    """
    Association file in csv format
    first col = id
    second col = GO id reference
    id	go_id
    3804	GO:0003823
    3804	GO:0004872
    3804	GO:0005515
    3804	GO:0005886

    """

    def __init__(self, file):
        self.association = {}
        self._load_association_file(file)

    def _load_association_file(self, file):
        try:
            assoc = pd.read_csv(file)
            assoc = assoc.dropna(axis=0)
            self._make_association(assoc)
            print("Load association file")
        except:
            try:
                assoc = pd.read_csv(file, sep=',')
                assoc = assoc.dropna(axis=0)
                self._make_association(assoc)
                print("Load association file")
            except Exception as e:
                print(e)

    def _make_association(self, assoc_data_frame):
        datagp = assoc_data_frame.groupby('id')
        for gene in assoc_data_frame.id.unique():
            go = datagp.get_group(gene)['go_id']
            self.association[gene] = set(go)
        print("Make association ")

    def query(self, term):
        return self.association[term]


class GOEnrichmentRecord(object):
    """Represents one result (from a single GOTerm) in the GOEnrichmentStudy
    """
    _fields = "id enrichment ratio_in_study ratio_in_pop p_uncorrected description ".split()

    def __init__(self, id, ratio_in_study, ratio_in_pop, p_uncorrected):
        self.id = id
        self.ratio_in_study = ratio_in_study
        self.ratio_in_pop = ratio_in_pop
        self.p_uncorrected = p_uncorrected
        self.enrichment = 'e' if ((1.0 * self.ratio_in_study[0] / self.ratio_in_study[1]) > (
            1.0 * self.ratio_in_pop[0] / self.ratio_in_pop[1])) else 'p'

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __str__(self, indent=False):
        field_data = [self.__dict__[f] for f in self._fields]
        return field_data

    def __repr__(self):
        return "GOEnrichmentRecord(%s)" % self.id

    def find_goterm(self, go):
        if self.id in go.go_Term:
            self.goterm = go.go_Term[self.id]
            self.description = self.goterm.name


def read_geneset(study_fn, pop_fn, compare=False):
    pop = set(_.strip() for _ in open(pop_fn) if _.strip())
    study = frozenset(_.strip() for _ in open(study_fn) if _.strip())
    # some times the pop is a second group to compare, rather than the
    # population in that case, we need to make sure the overlapping terms
    # are removed first
    if compare:
        common = pop & study
        pop |= study
        pop -= common
        study -= common
        print("removed ", len(common), " overlapping items")
        print("Set 1: {0}, Set 2: {1}".format(len(study), len(pop)))

    return study, pop


class EnrichmentStudy():
    """
    Runs Fisher's exact test, as well as multiple corrections
    study file contain id
    pop file contain background id
    assoc file is csv format
    """

    def __init__(self, study, pop, assoc, verbose=True):
        self.verbose = verbose
        self.alpha = 0.05
        self.pval = 0.05
        self.compare = True
        self.ration = 1
        self.indent = True
        self.min_ratio = self.ration
        if self.min_ratio is not None:
            assert 1 <= self.min_ratio <= 2
        assert 0 < self.alpha < 1, "Test-wise alpha must fall between (0, 1)"
        self.methods = ["bonferroni", "sidak"]

        self.results = []
        self.study, self.pop = read_geneset(study, pop, compare=self.compare)
        self.association = Association(assoc)
        self.go_tree = GO_tree()
        self.go_tree.update_association(self.association)

        self.term_study = self.count_terms(self.study, self.association, self.go_tree)
        self.term_pop = self.count_terms(self.pop, self.association, self.go_tree)

        self.pop_n, self.study_n = len(self.pop), len(self.study)

        self.Run()

    def Run(self):
        for term, study_count in self.term_study.items():
            pop_count = self.term_pop[term]
            p = scipy.stats.fisher_exact(([[study_count, self.study_n], [pop_count, self.pop_n]]))

            one_record = GOEnrichmentRecord(id=term, p_uncorrected=p, ratio_in_study=(study_count, self.study_n),
                                            ratio_in_pop=(pop_count, self.pop_n))

            self.results.append(one_record)

        self.results.sort(key=lambda r: r.p_uncorrected[1])
        self.results = self.results

        for rec in self.results:
            # get go term for description and level
            rec.find_goterm(self.go_tree)

        if self.verbose:
            self.print_summary()

        return self.results

    def print_summary(self):
        # field names for output
        print("  Go Id     enrichment ratio/stu ratio/pop   Oddratio       p_uncorrected         description")
        # print first 20 go enrichment
        for rec in self.results[:20]:
            print(rec.__str__(indent=self.indent))
        return 0

    def count_terms(self, geneset, assoc, go_tree):
        """count the number of terms in the study group
        """
        term_cnt = collections.defaultdict(int)
        for gene in geneset:
            try:
                for x in assoc.association[int(gene)]:
                    if x in go_tree.go_Term:
                        term_cnt[go_tree.go_Term[x].id] += 1
            except:
                continue
        return term_cnt


def adjustPValues(pvalues, method='fdr', n=None):
    '''returns an array of adjusted pvalues

    Reimplementation of p.adjust in the R package.

    p: numeric vector of p-values (possibly with 'NA's).  Any other
    R is coerced by 'as.numeric'.

    method: correction method. Valid values are:

    n: number of comparisons, must be at least 'length(p)'; only set
    this (to non-default) when you know what you are doing

    For more information, see the documentation of the
    p.adjust method in R.
    '''

    if n is None:
        n = len(pvalues)

    if method == "fdr":
        method = "BH"

    # optional, remove NA values
    p = np.array(pvalues, dtype=np.float)
    lp = len(p)

    assert n <= lp

    if n <= 1:
        return p

    if method == "bonferroni":
        p0 = n * p
    elif method == "holm":
        i = np.arange(lp)
        o = np.argsort(p)
        ro = np.argsort(o)
        m = np.maximum.accumulate((n - i) * p[o])
        p0 = m[ro]
    elif method == "hochberg":
        i = np.arange(0, lp)[::-1]
        o = np.argsort(1 - p)
        ro = np.argsort(o)
        m = np.minimum.accumulate((n - i) * p[o])
        p0 = m[ro]
    elif method == "BH":
        i = np.arange(1, lp + 1)[::-1]
        o = np.argsort(1 - p)
        ro = np.argsort(o)
        m = np.minimum.accumulate(float(n) / i * p[o])
        p0 = m[ro]
    elif method == "BY":
        i = np.arange(1, lp + 1)[::-1]
        o = np.argsort(1 - p)
        ro = np.argsort(o)
        q = np.sum(1.0 / np.arange(1, n + 1))
        m = np.minimum.accumulate(q * float(n) / i * p[o])
        p0 = m[ro]
    elif method == "none":
        p0 = p

    return np.minimum(p0, np.ones(len(p0)))
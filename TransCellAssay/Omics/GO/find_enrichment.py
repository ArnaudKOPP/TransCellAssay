"""
Find enrichement
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import os
from TransCellAssay.Omics.GO.go_enrichment import GOEnrichmentStudy
from TransCellAssay.Omics.GO.obo_file_parser import GODag


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
        print("removed %d overlapping items", (len(common), ))
        print("Set 1: {0}, Set 2: {1}".format(len(study), len(pop)))

    return study, pop


def read_associations(assoc_fn):
    assoc = {}
    for row in open(assoc_fn):
        atoms = row.split()
        if len(atoms) == 2:
            a, b = atoms
        elif len(atoms) > 2 and row.count('\t') == 1:
            a, b = row.split("\t")
        else:
            continue
        b = set(b.split(";"))
        assoc[a] = b

    return assoc


def plot_go_term(term, gml=True, disable_draw_parents=False, disable_draw_children=False):
    obo_file = "gene_ontology.1_2.obo"
    assert os.path.exists(obo_file), "file %s not found!" % obo_file
    g = GODag(obo_file)

    g.write_dag()

    # run a test case
    if term is not None:
        rec = g.query_term(term, verbose=True)
        g.draw_lineage([rec], gml=gml, draw_parents=disable_draw_parents, draw_children=disable_draw_children)


def find_enrichment():
    alpha = 0.05
    pval = 0.05
    compare = False
    ration = False
    fdr = False
    indent = False

    min_ratio = ration
    if min_ratio is not None:
        assert 1 <= min_ratio <= 2

    assert 0 < alpha < 1, "Test-wise alpha must fall between (0, 1)"

    study_fn = None  # study file
    pop_fn = None  # population file
    assoc_fn = None  # association file
    study, pop = read_geneset(study_fn, pop_fn, compare=compare)
    assoc = read_associations(assoc_fn)

    methods = ["bonferroni", "sidak", "holm"]
    if fdr:
        methods.append("fdr")

    obo_dag = GODag(obo_file="gene_ontology.1_2.obo")
    g = GOEnrichmentStudy(pop, assoc, obo_dag, alpha=alpha, study=study, methods=methods)
    g.print_summary(min_ratio=min_ratio, indent=indent, pval=pval)
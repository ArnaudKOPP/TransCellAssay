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
        print("removed ", len(common), " overlapping items")
        print("Set 1: {0}, Set 2: {1}".format(len(study), len(pop)))

    return study, pop


def read_associations(assoc_fn):
    assoc = {}
    datagp = assoc_fn.groupby('entrezgene')
    for gene in assoc_fn.entrezgene.unique():
        go = datagp.get_group(gene)['go_id']
        assoc[gene] = set(go)
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


def read_assoc_dataframe(assoc_file):
    """
    Read the association file that have been make by biomaRt on R, entrezid and go_id in csv file format
    :param assoc_file: csv file
    :return: return data
    """
    import pandas as pd

    data = pd.read_table(assoc_file, sep=',')
    data = data.dropna(axis=0)
    return data


def find_enrichment(study_test, population_fn, assoc_file):
    alpha = 0.05
    pval = 0.05
    compare = False
    ration = 1
    indent = True

    min_ratio = ration
    if min_ratio is not None:
        assert 1 <= min_ratio <= 2

    assert 0 < alpha < 1, "Test-wise alpha must fall between (0, 1)"

    study_fn = study_test  # study file
    pop_fn = population_fn  # population file
    assoc_fn = read_assoc_dataframe(assoc_file)  # association file
    study, pop = read_geneset(study_fn, pop_fn, compare=compare)
    assoc = read_associations(assoc_fn)

    methods = ["bonferroni", "sidak", "holm"]

    obo_dag = GODag(obo_file="gene_ontology.1_2.obo")
    g = GOEnrichmentStudy(pop, assoc, obo_dag, alpha=alpha, study=study, methods=methods)
    g.print_summary(min_ratio=min_ratio, indent=indent, pval=pval)
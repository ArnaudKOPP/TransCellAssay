#!/usr/bin/env python3
# encoding: utf-8
"""
For testing module in actual dev
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import TransCellAssay.Omics.GO_enrichment as GO

from TransCellAssay.IO.Rest.Service import REST
# from TransCellAssay import REST

s = REST("test", "https://www.ebi.ac.uk/chemblws")
res = s.get_one("targets/CHEMBL5246.json", "json")
print(res)


# go_tree = GO.GO_tree(obo_file="gene_ontology.1_2.obo")
# go_term = go_tree.go_Term['GO:0000001']
# go_tree.query_term('GO:0045056', verbose=True)
# print(go_term)
# #print(go_tree.paths_to_top('GO:0000001'))
# #go_tree.print_all_go_id()
# asso = GO.Association("/home/akopp/Bureau/gene_id_go_id.csv")
# print(asso.query(3804))
# go_tree.update_association(asso)
# print(asso.query(3804))
# print(asso.association[3804])

'''
enrichment = GO.EnrichmentStudy(study="/home/akopp/Bureau/study.txt", pop="/home/akopp/Bureau/population.txt",
                                assoc="/home/akopp/Bureau/gene_id_go_id.csv")
'''
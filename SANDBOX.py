#!/usr/bin/env python3
# encoding: utf-8
"""
For testing module in actual dev
"""
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
np.set_printoptions(linewidth=250)
np.set_printoptions(suppress=True)
"""
import os
import sys
import time
import TransCellAssay as TCA

time_start = time.time()

# # reading TEST
time_norm_start = time.time()

screen_test = TCA.Core.Screen()
plaque1 = TCA.Core.Plate(name='Plate 1')
platesetup = TCA.Core.PlateMap(platemap="/home/arnaud/Desktop/antagomir/Pl1PP.csv")
# plaque1.addPlateMap(platesetup)
# # or
plaque1 + platesetup
rep1 = TCA.Core.Replicat(name="rep1", data="/home/arnaud/Desktop/antagomir/Pl9rep_1.csv")
rep2 = TCA.Core.Replicat(name="rep2", data="/home/arnaud/Desktop/antagomir/Pl9rep_2.csv")
rep3 = TCA.Core.Replicat(name="rep3", data="/home/arnaud/Desktop/antagomir/Pl9rep_3.csv")

# listing = list()
# listing.append(rep1)
# listing.append(rep2)
# listing.append(rep3)
# plaque1 + listing
# # or
plaque1 + rep1
plaque1 + rep2
plaque1 + rep3

## or
# plaque1.addReplicat(rep1)
# plaque1.addReplicat(rep2)
# plaque1.addReplicat(rep3)
screen_test.add_plate(plaque1)

feature = "Nuc Intensity"
neg = "NT"
pos = "SINV C"

time_norm_stop = time.time()
print("\033[0;32m ->Reading input data Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

time_start_comp = time.time()

time_norm_start = time.time()
TCA.plate_quality_control(plaque1, features=feature, cneg=neg, cpos=pos, sedt=False, sec_data=False, verbose=True)
time_norm_stop = time.time()
print("\033[0;32mQuality Control Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

time_norm_start = time.time()
analyse = TCA.plate_analysis(plaque1, [feature], neg, pos, threshold=50)
print(analyse)
time_norm_stop = time.time()
print("\033[0;32mCompute Plate Analyzis Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

time_norm_start = time.time()
plaque1.normalization(feature, method='Zscore', log=True, neg=neg, pos=pos)
time_norm_stop = time.time()
print("\033[0;32mNormalization Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

time_norm_start = time.time()
plaque1.compute_data_from_replicat(feature)
print(plaque1.Data)
print('rep1')
print(plaque1['rep1'].Data)

# TCA.systematic_error_detection_test(plaque1.Data, alpha=0.05, verbose=True)
# TCA.systematic_error_detection_test(rep1.Data, alpha=0.05, verbose=True)
# TCA.systematic_error_detection_test(rep2.Data, alpha=0.05, verbose=True)
# TCA.systematic_error_detection_test(rep3.Data, alpha=0.05, verbose=True)

plaque1.systematic_error_correction(method='median', apply_down=True, save=True, verbose=False)
# plaque1.SystematicErrorCorrection(apply_down=False, save=True)  # apply only when replicat are not SE norm
plaque1.compute_data_from_replicat(feature, use_sec_data=True)
print("SEC")
print(plaque1.SECData)
print('rep1')
print(plaque1['rep1'].SECData)
TCA.systematic_error_detection_test(plaque1.SECData, alpha=0.05, verbose=True)
time_norm_stop = time.time()
print("\033[0;32mSEC Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

# print("\n \033[0;32m     SSMD TESTING \033[0m")
# time_norm_start = time.time()
# TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, sec_data=False, verbose=True)
# TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, robust_version=False, sec_data=False, verbose=True)
# TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, variance='equal', sec_data=False, verbose=True)
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, variance='unequal', robust_version=False,
                     sec_data=True, verbose=True)

start = time.time()
plaque1.check_data_consistency()
stop = time.time()
print("\033[0;32mCheck data Executed in {0:f}s\033[0m".format(float(stop - start)))
# TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, sec_data=True, verbose=True)
# TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, robust_version=False, sec_data=True, verbose=True)
# ssmd = TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', sec_data=True, verbose=True)
# TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', robust_version=False,
# sec_data=True, verbose=True)
# TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', sec_data=False, verbose=True,
#                      inplate_data=True)
# TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', robust_version=False,
#                      sec_data=False, verbose=True, inplate_data=True)
# print("\033[0;32m    T-Stat TESTING \033[0m")
# TCA.plate_tstat_score(plaque1, neg_control=neg, paired=False, variance='equal', sec_data=True, verbose=True)
# TCA.plate_tstat_score(plaque1, neg_control=neg, paired=False, variance='equal', sec_data=False, verbose=True)
# TCA.plate_tstat_score(plaque1, neg_control=neg, paired=True, sec_data=True, verbose=True)
# test = TCA.plate_tstat_score(plaque1, neg_control=neg, paired=True, sec_data=False, verbose=True)
#
# gene = platesetup.platemap.values.flatten().reshape(96, 1)
# stat = np.append(gene, test.flatten().reshape(96, 1), axis=1)
# stat = np.append(stat, ssmd.flatten().reshape(96, 1), axis=1)
# print(stat)


# TCA.Graphics.plotDistribution('C5', plaque1, feature)
# Graphics.boxplotByWell(rep1.Dataframe, feature)
# Graphics.PlateHeatmap(rep1.Data)
# Graphics.SystematicError(rep1.Data)
# Graphics.plotSurf3D_Plate(rep1.Data)
# Graphics.plotScreen(screen_test)
# TCA.plotSurf3D_Plate(ssmd)

# clustering = TCA.k_mean_clustering(plaque1)
# clustering.do_cluster()

time_stop_comp = time.time()
print("\033[0;32m ->Computation Executed in {0:f}s\033[0m".format(float(time_stop_comp - time_start_comp)))
"""

"""
time_start = time.time()
import TransCellAssay.Omics.GO_enrichment as GO

# go_tree = GO.GO_tree(obo_file="go.obo")
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


enrichment = GO.EnrichmentStudy(study="/home/arnaud/Desktop/study.txt", pop="/home/arnaud/Desktop/pop.txt",
                                assoc="/home/arnaud/Desktop/assoc.csv", compare=False)
result = enrichment.to_dataframe()

print(pd.DataFrame(result))


time_stop = time.time()
print("\033[0;32m   ----> TOTAL TIME : {0:f}s\033[0m".format(float(time_stop - time_start)))
"""
# ### Encode REST TEST
# from TransCellAssay.IO.Rest.Encode import Encode
# encode = Encode()
# response = encode.test()

# import json
# Print the object
# print(json.dumps(response, indent=4, separators=(',', ': ')))

# ### String REST TEST
from TransCellAssay.IO.Rest.String import String

str = String()
response = str.test()
print(response)

# ### Array Express REST TEST
# from TransCellAssay.IO.Rest.ArrayExpress import ArrayExpress

# ae = ArrayExpress()
# res = ae.query_experiments(species="Homo sapiens", ef="organism_part", efv="liver")


# #### Psicquic REST TEST
# from TransCellAssay.IO.Rest.Psicquic import PSICQUIC

# p = PSICQUIC()
# p.print_status()
# print(p.query("string", "species:10090", firstResult=0, maxResults=100, output="tab25"))
# print(p.query("biogrid", "ZAP70"))
# print(p.query("biogrid", "ZAP70 AND species:10090"))
# res = p.query("intact", "zap70")
# for x in res:
# print(x)
# print(p.queryAll("ZAP70 AND species:9606"))

# #### Biogrid REST TEST
# from TransCellAssay.IO.Rest.Biogrid import Biogrid

# b = Biogrid()
# print(b.get_biogrid_version())
# print(b._supported_organism_list())
# print(b.SupportedOrganismId)
# print(b.SupportedOrganismId["9606"])
# res = b.interaction(geneList="31623", searchbiogridids="true", includeInteractors="true", caca="grzefg")
# print(res)

# from io import StringIO

# data = pd.read_table(StringIO(res), header=None)
# print(data)

# import pandas as pd
# from io import StringIO
#
# data = pd.read_table(StringIO(res), header=None)
# print(data)


# #### UNIPROT REST TEST
# from TransCellAssay.IO.Rest.Uniprot import UniProt
# u = UniProt()

# print(u.mapping("ACC", "KEGG_ID", query='P43403 P29317'))
# res = u.search("P43403")
# print(res)
# Returns sequence on the ZAP70_HUMAN accession Id
# sequence = u.search("ZAP70_HUMAN", columns="sequence")
# print(sequence)

# fasta = u.retrieve([u'P29317', u'Q5BKX8', u'Q8TCD6'], frmt='fasta')
# print(fasta[0])

# res = u.retrieve("P09958", frmt="xml")
# print(res)

# res = u.get_fasta("P09958")
# print(res)
# print(u.get_fasta_sequence("P09958"))

# print(u.search('zap70+AND+organism:9606', frmt='list'))
# print(u.search("zap70+and+taxonomy:9606", frmt="tab", limit=3, columns="entry name,length,id, genes"))

# #### KEGG REST TEST

# from TransCellAssay.IO.Rest.Service import REST
# s = REST("test", "https://www.ebi.ac.uk/chemblws")
# res = s.get_one("targets/CHEMBL5246.json", "json")
# target = res['target']
# print(target['organism'])

# from TransCellAssay.IO.Rest.KEGG import KEGG, KEGGParser

# k = KEGG()
# print(k.Tnumber2code("T01001"))
# print(k.code2Tnumber("hsa"))
# print(k.isOrganism("hsa"))

# print(k.info())
# print(k.info("hsa"))
# print(k.info("T01001"))  # same as above
# print(k.info("pathway"))

# k.list('organism')
# print(k.organismIds)
# k.organism = "hsa"
# print(k.pathwayIds)
# print(k.get("hsa:7535"))
# print(k.list("pathway", organism="hsa"))
# k.reaction
# k.reactionIds

# print(k.list("pathway"))  # returns the list of reference pathways
# print(k.list("pathway", "hsa"))  # returns the list of human pathways
# print(k.list("organism"))  # returns the list of KEGG organisms with taxonomic classification
# print(k.list("hsa"))  # returns the entire list of human genes
# print(k.list("T01001"))  # same as above
# print(k.list("hsa:10458+ece:Z5100"))  # returns the list of a human gene and an E.coli O157 gene
# print(k.list("cpd:C01290+gl:G00092"))  # returns the list of a compound entry and a glycan entry
# print(k.list("C01290+G00092"))  # same as above

# # search for pathways that contain Viral in the definition
# print(k.find("pathway", "Viral"))
# # for keywords "shiga" and "toxin"
# print(k.find("genes", "shiga+toxin"))
# # for keywords "shiga toxin"
# print(k.find("genes", "shiga toxin"))
# # for chemical formula "C7H10O5"
# print(k.find("compound", "C7H10O5", "formula"))
# # for chemical formula containing "O5" and "C7"
# print(k.find("compound", "O5C7", "formula"))
# # for 174.045 =< exact mass < 174.055
# print(k.find("compound", "174.05", "exact_mass"))
# # for 300 =< molecular weight =< 310
# print(k.find("compound", "300-310", "mol_weight"))

# # retrieves a compound entry and a glycan entry
# print(k.get("cpd:C01290+gl:G00092"))
# # same as above
# print(k.get("C01290+G00092"))
# # retrieves a human gene entry and an E.coli O157 gene entry
# print(k.get("hsa:10458+ece:Z5100"))
# # retrieves amino acid sequences of a human gene and an E.coli O157 gene
# print(k.get("hsa:10458+ece:Z5100/aaseq"))

# res = k.get("hsa05130/image")
# # same as : res = s.get("hsa05130","image")
# f = open("test.png", "wb")
# f.write(res)
# f.close()

# # conversion from NCBI GeneID to KEGG ID for E. coli genes
# print(k.conv("eco", "ncbi-geneid"))
# # inverse of the above example
# print(k.conv("eco", "ncbi-geneid"))
# # conversion from KEGG ID to NCBI GI
# print(k.conv("ncbi-gi", "hsa:10458+ece:Z5100"))

# # KEGG pathways linked from each of the human genes
# print(k.link("pathway", "hsa"))
# # human genes linked from each of the KEGG pathways
# print(k.link("hsa", "pathway"))
# # KEGG pathways linked from a human gene and an E. coli O157 gene.
# print(k.link("pathway", "hsa:10458+ece:Z5100"))

# # show a pathway in the browser
# k.show_pathway("path:hsa05416", scale=50)
# # Same as above but also highlights some KEGG Ids (red for all)
# k.show_pathway("path:hsa05416", dcolor="white", keggid=['1525', '1604', '2534'])
# # You can refine the colors using a dictionary:
# k.show_pathway("path:hsa05416", dcolor="white", keggid={'1525': 'yellow,red', '1604': 'blue,green', '2534': "blue"})
# print(k.check_dbentries("hsa:10458+ece:Z5100"))
# print(k.get_pathway_by_gene("7535", "hsa"))

# s = KEGGParser()
# data = s.get("hsa:7535")
# dict_data = s.parse(data)
# print(dict_data)

# data = s.get("hsa04660")
# dict_data = s.parse(data)
# print(dict_data['gene'])

# res = s.get("hsa04660", "kgml")
# print(res)

# res = s.parse_kgml_pathway("hsa04660")
# # print(res)
# res['relations']
# print(res['relations'][0])

# #### REACTOME REST TEST

# from TransCellAssay.IO.Rest.Reactome import Reactome
# r = Reactome()
# print(r.get_list_pathways())
# print(r.get_species())
# print(r.biopax_exporter(109581))

# res = r.highlight_pathway_diagram("68875", genes="CDC2", frmt='PDF')
# f = open("reactome.pdf", "w")
# f.write(res)
# f.close()

# res = r.list_by_query("Pathway", name='Apoptosis')
# identifiers = [x['dbId'] for x in res]
# print(identifiers)

# print(r.pathway_hierarchy("homo sapiens"))
# print(r.pathway_participantes(109581))
# print(r.pathway_complexes(109581))
# print(r.query_by_id("Pathway", "109581"))
# print(r.query_hit_pathways('CDC2'))
# print(r.query_hit_pathways(['CDC2']))

# print(r.species_list())
# print(r.SBML_exporter(109581))
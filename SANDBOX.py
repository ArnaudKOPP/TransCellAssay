#!/usr/bin/env python3
# encoding: utf-8
"""
For testing module in actual dev
"""

import os
import sys
import time
import numpy as np
import TransCellAssay as TCA
import pandas as pd


time_start = time.time()

# # reading TEST
time_norm_start = time.time()

screen_test = TCA.Core.Screen()
plaque1 = TCA.Core.Plate(name='Plate 1')
platesetup = TCA.Core.PlateMap(platemap="/home/arnaud/Desktop/antagomir/Pl1PP.csv")
# plaque1.addPlateMap(platesetup)
# # or
plaque1 + platesetup
rep1 = TCA.Core.Replicat(name="rep1", data="/home/arnaud/Desktop/antagomir/Pl1rep_1.csv")
rep2 = TCA.Core.Replicat(name="rep2", data="/home/arnaud/Desktop/antagomir/Pl1rep_2.csv")
rep3 = TCA.Core.Replicat(name="rep3", data="/home/arnaud/Desktop/antagomir/Pl1rep_3.csv")

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
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
np.set_printoptions(linewidth=250)
np.set_printoptions(suppress=True)

time_norm_start = time.time()
TCA.plate_quality_control(plaque1, features=feature, cneg=neg, cpos=pos, sedt=False, sec_data=False, verbose=True)
time_norm_stop = time.time()
print("\033[0;32mQuality Control Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

time_norm_start = time.time()
import profile
# analyse = TCA.compute_plate_analyzis(plaque1, [feature], neg, pos, threshold=50)
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

TCA.systematic_error_detection_test(plaque1.Data, alpha=0.05, verbose=True)
TCA.systematic_error_detection_test(rep1.Data, alpha=0.05, verbose=True)
TCA.systematic_error_detection_test(rep2.Data, alpha=0.05, verbose=True)
TCA.systematic_error_detection_test(rep3.Data, alpha=0.05, verbose=True)

plaque1.systematic_error_correction(method='median', apply_down=True, save=True, verbose=False)
# plaque1.SystematicErrorCorrection(apply_down=False, save=True)  # apply only when replicat are not SE norm
plaque1.compute_data_from_replicat(feature, use_sec_data=True)
print(plaque1.SECData)
TCA.systematic_error_detection_test(plaque1.SECData, alpha=0.05, verbose=True)
time_norm_stop = time.time()
print("\033[0;32mSEC Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

print("\n \033[0;32m     SSMD TESTING \033[0m")
time_norm_start = time.time()
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, sec_data=False, verbose=True)
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, robust_version=False, sec_data=False, verbose=True)
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, variance='equal', sec_data=False, verbose=True)
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, variance='equal', robust_version=False,
                     sec_data=True, verbose=True)
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, sec_data=True, verbose=True)
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, robust_version=False, sec_data=True, verbose=True)
ssmd = TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', sec_data=True, verbose=True)
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', robust_version=False,
                     sec_data=True, verbose=True)
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', sec_data=False, verbose=True,
                     inplate_data=True)
TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', robust_version=False,
                     sec_data=False, verbose=True, inplate_data=True)
print("\033[0;32m    T-Stat TESTING \033[0m")
TCA.plate_tstat_score(plaque1, neg_control=neg, paired=False, variance='equal', sec_data=True, verbose=True)
TCA.plate_tstat_score(plaque1, neg_control=neg, paired=False, variance='equal', sec_data=False, verbose=True)
TCA.plate_tstat_score(plaque1, neg_control=neg, paired=True, sec_data=True, verbose=True)
test = TCA.plate_tstat_score(plaque1, neg_control=neg, paired=True, sec_data=False, verbose=True)

gene = platesetup.platemap.values.flatten().reshape(96, 1)
stat = np.append(gene, test.flatten().reshape(96, 1), axis=1)
stat = np.append(stat, ssmd.flatten().reshape(96, 1), axis=1)
print(stat)

time_norm_stop = time.time()
print("\033[0;32mSSMD T-Stat Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

# TCA.Graphics.plotDistribution('C5', plaque1, feature)
# Graphics.boxplotByWell(rep1.Dataframe, feature)
# Graphics.PlateHeatmap(rep1.Data)
# Graphics.SystematicError(rep1.Data)
# Graphics.plotSurf3D_Plate(rep1.Data)
# Graphics.plotScreen(screen_test)
TCA.plotSurf3D_Plate(ssmd)

# clustering = TCA.k_mean_clustering(plaque1)
# clustering.do_cluster()

time_stop_comp = time.time()
print("\033[0;32m ->Computation Executed in {0:f}s\033[0m".format(float(time_stop_comp - time_start_comp)))

'''
from TransCellAssay.IO.Rest.Service import REST

s = REST("test", "https://www.ebi.ac.uk/chemblws")
res = s.get_one("targets/CHEMBL5246.json", "json")
target = res['target']
print(target['organism'])

from TransCellAssay.IO.Rest.KEGG import KEGG, KEGGParser

k = KEGG()
k.list('organism')
print(k.organismIds)
k.organism = "hsa"
print(k.pathwayIds)
print(k.get("hsa:7535"))

s = KEGGParser()
data = s.get("hsa:7535")
dict_data = s.parse(data)
print(dict_data)

data = s.get("hsa04660")
dict_data = s.parse(data)
print(dict_data['gene'])

res = s.get("hsa04660", "kgml")
print(res)

res = s.parse_kgml_pathway("hsa04660")
# print(res)
res['relations']
print(res['relations'][0])
'''

'''
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
import pandas as pd

pd.set_option('display.width', 1000)
print(pd.DataFrame(result))
'''

time_stop = time.time()
print("\033[0;32m   ----> TOTAL TIME : {0:f}s\033[0m".format(float(time_stop - time_start)))
#!/usr/bin/env python3
# encoding: utf-8
"""
For testing module in actual dev
"""
import pandas as pd
import numpy as np
import time

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
np.set_printoptions(linewidth=300)
np.set_printoptions(suppress=True)

import TransCellAssay as TCA


def do_384():
    platemap = TCA.PlateMap(platemap="/home/arnaud/Desktop/HDV_plaque_Z/Pl1PP.csv")

    plaque1 = TCA.Plate('plaque1')
    plaque1 + platemap
    plaque2 = TCA.Plate('plaque2')
    plaque2 + platemap

    plaque1 + TCA.Replica(name='rep1', data='/home/arnaud/Desktop/HDV_plaque_Z/150121 Eloi1.csv', datatype='mean')
    plaque2 + TCA.Replica(name='rep1', data='/home/arnaud/Desktop/HDV_plaque_Z/150121 Eloi2.csv', datatype='mean')

    print(platemap)

    channel = 'AvgIntenCh2'
    neg = 'Neg 1'
    pos = 'SiNTCP'

    # time_start = time.time()
    # ana = TCA.plate_analysis(plaque1, [channel], neg, pos, threshold=400, percent=False)
    # # ana = TCA.plate_analysis(plaque1, [channel], neg, pos)
    # print(ana)
    # time_stop = time.time()
    # print("\033[0;32mTOTAL EXECUTION TIME  {0:f}s \033[0m".format(float(time_stop - time_start)))

    plaque1.normalization(channel=channel, method='Zscore', neg=platemap.get_well(neg),
                          pos=platemap.get_well(pos))
    plaque2.normalization(channel=channel, method='Zscore', neg=platemap.get_well(neg),
                          pos=platemap.get_well(pos))

    # TCA.plate_channel_scaling(plaque2, channel, mean_scaling=True)

    # plaque1.compute_data_from_replicat(channel)
    # plaque2.compute_data_from_replicat(channel)

    # TCA.heatmap_map_p(plaque1, plaque2)

    TCA.plate_quality_control(plaque1, channel=channel, cneg=neg, cpos=pos, use_raw_data=False, verbose=True)
    TCA.plate_quality_control(plaque2, channel=channel, cneg=neg, cpos=pos, use_raw_data=False, verbose=True)

    # # Keep only neg or pos in 3D plot
    # test1_neg = TCA.get_masked_array(plaque1.array, platemap.platemap.values, to_keep=neg)
    # test2_neg = TCA.get_masked_array(plaque2.array, platemap.platemap.values, to_keep=neg)
    # test1_pos = TCA.get_masked_array(plaque1.array, platemap.platemap.values, to_keep=pos)
    # test2_pos = TCA.get_masked_array(plaque2.array, platemap.platemap.values, to_keep=pos)
    # TCA.plot_plate_3d(test1_neg)
    # TCA.plot_plate_3d(test2_neg)
    # TCA.plot_plate_3d(test1_pos)
    # TCA.plot_plate_3d(test2_pos)

    plaque1.systematic_error_correction(algorithm="PMP", apply_down=True, save=True, verbose=False, alpha=0.1)
    plaque2.systematic_error_correction(algorithm="PMP", apply_down=True, save=True, verbose=False, alpha=0.1)

    # plaque1.systematic_error_correction(algorithm="MEA", apply_down=True, save=True, verbose=False, alpha=0.1)
    # plaque2.systematic_error_correction(algorithm="MEA", apply_down=True, save=True, verbose=False, alpha=0.1)

    # TCA.plate_ssmd_score(plaque1, neg_control=neg, robust_version=True, sec_data=True, verbose=True)
    # TCA.plate_ssmd_score(plaque1, neg_control=neg, robust_version=True, sec_data=True, method='MM', verbose=False)
    # TCA.plate_ssmd_score(plaque1, neg_control=neg, robust_version=False, sec_data=True, verbose=True)
    # TCA.plate_ssmd_score(plaque1, neg_control=neg, robust_version=False, sec_data=True, method='MM', verbose=True)

    # TCA.plot_plate_3d(plaque1.sec_array)
    # TCA.plot_plate_3d(plaque2.sec_array)
    # TCA.plate_heatmap_p(plaque1)
    # TCA.plate_heatmap_p(plaque2)
    # TCA.heatmap_map_p(plaque1, plaque2, usesec=True)
    # TCA.plate_heatmap_p(plaque1, both=True)
    # TCA.plate_heatmap_p(plaque2, both=True)
    # TCA.plot_multiple_plate(plaque1, plaque2, usesec=True)
    TCA.plot_wells(plaque1, plaque2, neg=neg, pos=pos)
    # TCA.dual_flashlight_plot(plaque1.array, ssmd)
    # TCA.boxplot_by_wells(plaque1['rep1'].rawdata.df, channel=channel)
    # TCA.plot_distribution(wells=['B5', 'B6'], plate=plaque1, channel=channel)

# do_384()


def do_it(plate_nb, verbose=False):
    plaque = TCA.Core.Plate(name='Plate' + plate_nb)
    platesetup = TCA.Core.PlateMap(platemap="/home/arnaud/Desktop/Toulouse_12_2014/Pl"+plate_nb+"PP.csv")
    plaque + platesetup
    rep1 = TCA.Core.Replica(name="rep1",
                            data="/home/arnaud/Desktop/Toulouse_12_2014/toulouse pl " + plate_nb + ".1.csv")
    rep2 = TCA.Core.Replica(name="rep2",
                            data="/home/arnaud/Desktop/Toulouse_12_2014/toulouse pl " + plate_nb + ".2.csv")
    rep3 = TCA.Core.Replica(name="rep3",
                            data="/home/arnaud/Desktop/Toulouse_12_2014/toulouse pl " + plate_nb + ".3.csv")

    plaque + rep1
    plaque + rep2
    plaque + rep3
    channel = "ROI_B_Target_I_ObjectTotalInten"
    neg = "Neg"
    pos = "F1 ATPase A"

    plaque.check_data_consistency()
    rep1.datatype = "mean"
    rep2.datatype = "mean"
    rep3.datatype = "mean"

    time_start = time.time()
    ana = TCA.plate_analysis(plaque, [channel], neg, pos)
    print(ana)
    time_stop = time.time()
    print("\033[0;32mTOTAL EXECUTION TIME  {0:f}s \033[0m".format(float(time_stop - time_start)))

    # plaque.normalization(channel, method='PercentOfControl', log=False, neg=platesetup.get_well(neg),
    #                      pos=platesetup.get_well(pos), skipping_wells=True)

    # time_start = time.time()
    # ana = TCA.plate_analysis(plaque, [channel], neg, pos)
    # print(ana)
    # time_stop = time.time()
    # print("\033[0;32mTOTAL EXECUTION TIME  {0:f}s \033[0m".format(float(time_stop - time_start)))

    # TCA.plate_channel_scaling(plaque, channel, mean_scaling=True)

    plaque.normalization(channel, method='PercentOfControl', log=False, neg=platesetup.get_well(neg),
                         pos=platesetup.get_well(pos))

    TCA.plate_quality_control(plaque, channel=channel, cneg=neg, cpos=pos, use_raw_data=False, skipping_wells=True,
                              verbose=True)

    # TCA.ReferenceDataWriter(plaque, plaque, plaque, plaque, plaque, plaque, plaque, plaque, filepath='/home/arnaud/Desktop/test.xlsx', ref=['Neg', 'F1 ATPase A', 'F1 ATPase B'], channels=["ROI_B_Target_I_ObjectTotalInten", "ROI_A_Target_I_ObjectTotalInten"])

    # TCA.systematic_error_detection_test(plaque.array, alpha=0.1, verbose=True)
    plaque.systematic_error_correction(algorithm="MEA", apply_down=True, save=True, verbose=True, alpha=0.1)

    # TCA.independance(plaque, neg='Neg', channel=channel)
    # TCA.rank_product(plaque, secdata=True, verbose=True)

    # ssmd1 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=True,
    #                              verbose=verbose)
    # TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=False, verbose=verbose)
    # ssmd2 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=True,
    #                              variance="equal", verbose=verbose)
    # TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=False, variance="equal",
    #                      verbose=verbose)
    # ssmd3 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=True,
    #                              verbose=verbose)
    # TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=False, verbose=verbose)
    # ssmd4 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=True,
    #                              method='MM', verbose=verbose)
    # TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=False, method='MM',
    #                      verbose=verbose)
    # tstat1 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, variance='equal', sec_data=True,
    #                                verbose=verbose)
    # TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, variance='equal', sec_data=False, verbose=verbose)
    # tstat2 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, sec_data=True, verbose=verbose)
    # TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, sec_data=False, verbose=verbose)
    # tstat3 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=True, sec_data=True, verbose=verbose)
    # TCA.plate_tstat_score(plaque, neg_control=neg, paired=True, sec_data=False, verbose=verbose)

    __SIZE__ = 96

    # gene = plaque.PlateMap.platemap.values.flatten().reshape(__SIZE__, 1)
    # final_array = np.append(gene, plaque.Data.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, plaque['rep1'].Data.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, plaque['rep2'].Data.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, plaque['rep3'].Data.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ssmd1.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ssmd2.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ssmd3.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ssmd4.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, tstat1.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, tstat2.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, tstat3.flatten().reshape(__SIZE__, 1), axis=1)

    # to_save = pd.DataFrame(final_array)
    # to_save.to_csv("/home/arnaud/Desktop/ssmd_tstat_poc2.csv", index=False, header=False)

    # plaque.save_raw_data("/home/arnaud/Desktop/plaque1_poc/")
    # print(ssmd3)

    # TCA.dual_flashlight_plot(plaque.array, ssmd3)
    TCA.plot_wells(plaque, plaque, neg=neg, pos=pos)
    # TCA.Graphics.plot_distribution(('C1', 'D1'), plaque, channel, rep='rep2')
    # TCA.Graphics.plot_distribution(('C1', 'D1'), plaque, channel, rep='rep1')
    # TCA.boxplot_by_wells(rep1.rawdata.df, channel)
    # TCA.heatmap(rep1.array)
    # print(rep2.array)
    # TCA.heatmap(rep1.array)
    # TCA.heatmap(rep2.array, pretty=False)
    # TCA.heatmap(rep3.array, pretty=False)
    # TCA.plate_heatmap(plaque, both=False)
    # TCA.heatmap_map_p(plaque, plaque, plaque, plaque)
    # TCA.systematic_error(plaque.array)
    # TCA.systematic_error(plaque.sec_array)
    # TCA.plot_plate_3d(rep1.array, surf=True)
    # TCA.plot_plate_3d(plaque.array, surf=True)
    # TCA.plot_plate_3d(plaque.sec_array, surf=True)
    # TCA.plate_heatmap(plaque, both=False)
    # TCA.plot_multiple_plate(plaque, plaque)
    # TCA.plot_raw_data(rep1.rawdata)
    # clustering = TCA.k_mean_clustering(plaque)
    # clustering.do_cluster()

# do_it(plate_nb="1", verbose=False)


def go():
    """
    Go Enrichment testing
    """
    # import TransCellAssay.Stat.Omics.GO_enrichment as GO
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
    # enrichment = GO.EnrichmentStudy(study="/home/arnaud/Desktop/study.txt", pop="/home/arnaud/Desktop/pop.txt",
    #                                 assoc="/home/arnaud/Desktop/assoc.csv", compare=False)
    # result = enrichment.to_dataframe()
    # print(pd.DataFrame(result))

# go()


def rest():
    """
    Rest test function
    """

    # ### Biomart REST TEST
    # from TransCellAssay.IO.Rest.Biomart import BioMart
    # s = BioMart(verbose=True)
    # print(s.portal())
    # marts = s.available_marts()
    # import json
    # print(json.dumps(marts, indent=4, separators=(',', ':')))

    # dataset = s.datasets_for_marts(config='snp_config')
    # import json
    # print(json.dumps(dataset, indent=4, separators=(',', ':')))

    # print(s.filter_for_datasets(config='snp_config', datasets='btaurus_snp'))
    # print(s.attributs_for_datasets(config='snp_config', datasets='btaurus_snp'))
    # print(s.container_for_marts(config='snp_config', datasets='btaurus_snp'))

    # ### Eutils REST TEST
    # from TransCellAssay.IO.Rest.Eutils import EUtils, EUtilsParser
    # eutils = EUtils(email='kopp@igbmc.fr', verbose=True)

    # db = eutils.available_databases
    # print(db)

    # einfo = eutils.EInfo(db='bioproject', retmode='json')
    # import json
    # print(json.dumps(einfo, indent=4, separators=(',', ': ')))

    # einfo = eutils.EInfo(db='protein')
    # print(EUtilsParser(einfo))

    # esearch = eutils.ESearch(db='protein', term='human', retmax=5)
    # print(esearch)

    # ### Encode REST TEST
    # from TransCellAssay.IO.Rest.Encode import Encode
    # encode = Encode()
    # response = encode.biosample('ENCBS000AAA')
    # encode.show_response(response)

    # ### String REST TEST
    # from TransCellAssay.IO.Rest.String import String
    # string = String(identity='kopp@igbmc.fr')

    # ### Array Express REST TEST
    # from TransCellAssay.IO.Rest.ArrayExpress import ArrayExpress
    # ae = ArrayExpress(verbose=True)
    # res = ae.queryExperiments(species="Homo sapiens", ef="organism_part", efv="liver")
    # print(res)
    # res = ae.retrieveExperiment("E-MEXP-31")
    # print(res)

    # res = ae.queryExperiments(array="A-AFFY-33", species="Homo Sapiens", sortby="releasedate")
    # print(res)

    # ### Ensembl REST TEST
    # from TransCellAssay.IO.Rest.Ensembl import Ensembl
    # s = Ensembl(verbose=True)
    # print(s.get_rest_version())
    # print(s.get_api_version())
    # print(s.get_archive("AT3G52430"))
    # print(s.post_archive(["AT3G52430", "AT1G01160"]))
    # print(s.get_gene_family_information_by_id('MF_01687'))
    # print(s.get_info_analysis('arabidopsis_thaliana'))
    # print(s.get_info_assembly('arabidopsis_thaliana'))
    # print(s.get_info_assembly_by_region('arabidopsis_thaliana', region=1))
    # print(s.get_info_compara_methods())

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
    # b = Biogrid(acceskey="dc589cabccb374194e060d3586b31349")
    # print(b.get_biogrid_version())
    # print(b._supported_organism_list())
    # print(b.SupportedOrganismId)
    # print(b.SupportedOrganismId["9606"])
    # res = b.interaction(geneList="31623", searchbiogridids="true", includeInteractors="true", caca="grzefg")
    # print(res)
    # import pandas as pd
    # from io import StringIO
    # data = pd.read_table(StringIO(res), header=None)
    # print(data)

    # #### UNIPROT REST TEST

    from TransCellAssay.IO.Rest.Uniprot import UniProt
    u = UniProt(user='kopp@igbmc.fr', verbose=True)
    print(u.mapping("ACC", "KEGG_ID", query='P43403 P29317'))
    res = u.search("P43403")
    print(res)
    # u.download_flat_files()
    # Returns sequence on the ZAP70_HUMAN accession Id
    sequence = u.search("ZAP70_HUMAN", columns="sequence")
    print(sequence)
    fasta = u.retrieve([u'P29317', u'Q5BKX8', u'Q8TCD6'], frmt='fasta')
    print(fasta[0])
    res = u.retrieve("P09958", frmt="xml")
    print(res)
    res = u.get_fasta("P09958")
    print(res)
    print(u.get_fasta_sequence("P09958"))
    print(u.search('zap70+AND+organism:9606', frmt='list'))
    print(u.search("zap70+and+taxonomy:9606", frmt="tab", limit=3, columns="entry name,length,id, genes"))

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

    # from TransCellAssay.IO.Rest.Reactome import Reactome, ReactomeAnalysis
    # r = Reactome()
    # print(r.front_page_items("homo sapiens"))
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
    # print(r.query_by_ids("Pathway", "CDC2"))
    # print(r.query_pathway_for_entities(170075))
    # print(r.query_hit_pathways('CDC2'))
    # print(r.query_hit_pathways(['CDC2']))
    # print(r.species_list())
    # print(r.SBML_exporter(109581))
    # ra = ReactomeAnalysis()
    # res = ra.identifiers('TP53')
    # import json
    # print(json.dumps(res, indent=4, separators=(',', ': ')))

    # res = ra.identifier(170075)
    # import json
    # print(json.dumps(res, indent=4, separators=(',', ': ')))

    # res = ra.species(48895)
    # import json
    # print(json.dumps(res, indent=4, separators=(',', ': ')))

rest()

print('FINISH')
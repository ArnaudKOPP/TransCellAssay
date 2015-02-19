#!/usr/bin/env python3
# encoding: utf-8
"""
For testing module in actual dev
"""
import pandas as pd
import numpy as np
import os
import json
import logging

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
np.set_printoptions(linewidth=300)
np.set_printoptions(suppress=True, precision=4)

import TransCellAssay as TCA


def HDV():
    plate_nb = '2'
    plaque = TCA.Core.Plate(name='Plate' + plate_nb)
    platemap = TCA.Core.PlateMap(platemap="/home/arnaud/Desktop/HDV/RawdataClean/Pl"+plate_nb+"PP.csv")
    plaque + platemap
    try:
        file = "/home/arnaud/Desktop/HDV/RawdataClean/HDV_" + plate_nb + ".1.csv"
        if os.path.isfile(file):
            plaque + TCA.Core.Replica(name="rep1",
                                      data=file,
                                      datatype='mean')
    except:
        pass
    try:
        file = "/home/arnaud/Desktop/HDV/RawdataClean/HDV_" + plate_nb + ".2.csv"
        if os.path.isfile(file):
            plaque + TCA.Core.Replica(name="rep2",
                                      data=file,
                                      datatype='mean')
    except:
        pass
    try:
        file = "/home/arnaud/Desktop/HDV/RawdataClean/HDV_" + plate_nb + ".3.csv"
        if os.path.isfile(file):
            plaque + TCA.Core.Replica(name="rep3",
                                      data=file,
                                      datatype='mean')
    except:
        pass

    channel = 'AvgIntenCh2'
    neg = 'Neg i'
    pos = 'SiNTCP i'

    # plaque.check_data_consistency()
    # TCA.plate_quality_control(plaque, channel=channel, cneg=neg, cpos=pos, use_raw_data=True, verbose=True)
    # TCA.ReferenceDataWriter(plaque,
    #                         filepath='/home/arnaud/Desktop/test.xlsx',
    #                         ref=['Neg', 'F1 ATPase A', 'F1 ATPase B'],
    #                         channels=["ROI_B_Target_I_ObjectTotalInten", "ROI_A_Target_I_ObjectTotalInten"])

    # ana = TCA.plate_analysis(plaque, channel, neg, pos, threshold=600, percent=False)
    ana = TCA.plate_analysis(plaque, channel, neg, pos)
    # print(ana)
    # ana.write("/home/arnaud/Desktop/HDV/RawdataClean/Percentvalue"+plate_nb+".csv")

    plaque.normalization_channels(channels=channel,
                                  method='Zscore',
                                  neg=platemap.search_well(neg),
                                  pos=platemap.search_well(pos))

    # plaque.compute_data_from_replicat(channel=channel)
    plaque.cut(1, 15, 1, 23, apply_down=True)
    # print(platemap)
    # plaque.compute_data_from_replicat(channel=channel)

    # # Keep only neg or pos in 3D plot
    # test1_neg = TCA.get_masked_array(plaque.array, platemap.platemap.values, to_keep=neg)
    # test1_pos = TCA.get_masked_array(plaque.array, platemap.platemap.values, to_keep=pos)
    # TCA.plot_plate_3d(test1_neg)
    # TCA.plot_plate_3d(test1_pos)

    alpha = 0.1
    verbose = False
    try:
        TCA.systematic_error_detection_test(plaque['rep1'].array, verbose=verbose, alpha=alpha)
        TCA.systematic_error_detection_test(plaque['rep2'].array, verbose=verbose, alpha=alpha)
        TCA.systematic_error_detection_test(plaque['rep3'].array, verbose=verbose, alpha=alpha)
    except KeyError:
        pass
    plaque.systematic_error_correction(algorithm="PMP", apply_down=True, save=True, verbose=verbose, alpha=alpha,
                                       max_iterations=50)

    # TEST Diffusion Model
    # TCA.diffusion_model(plaque.array.copy(), max_iterations=120, verbose=verbose)

    # ### not Single Cell
    # TCA.plate_ssmd_score(plaque, neg_control=neg, robust_version=True, sec_data=True, verbose=verbose)
    # TCA.plate_ssmd_score(plaque, neg_control=neg, robust_version=True, sec_data=True, method='MM', verbose=verbose)
    # TCA.plate_ssmd_score(plaque, neg_control=neg, robust_version=False, sec_data=True, verbose=verbose)
    # TCA.plate_ssmd_score(plaque, neg_control=neg, robust_version=False, sec_data=True, method='MM', verbose=verbose)

    # #### Single Cell
    # TCA.independance(plaque, neg='Neg', channel=channel)
    # TCA.rank_product(plaque, secdata=True, verbose=True)

    sec = True
    TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec, verbose=verbose)
    TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec, variance="equal",
                         verbose=verbose)
    TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=sec, verbose=verbose)
    TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=sec, method='MM',
                         verbose=verbose)
    TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, variance='equal', sec_data=sec, verbose=verbose)
    TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, sec_data=sec, verbose=verbose)
    TCA.plate_tstat_score(plaque, neg_control=neg, paired=True, sec_data=sec, verbose=verbose)

    __SIZE__ = 384
    # ssmd1 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=True,
    #                              verbose=verbose)
    # ssmd2 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=False,
    #                              variance="equal", verbose=verbose)
    # ssmd3 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=True,
    #                              verbose=verbose)
    # ssmd4 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=True,
    #                              method='MM', verbose=verbose)
    # tstat1 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, variance='equal', sec_data=True,
    #                                verbose=verbose)
    # tstat2 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, sec_data=True, verbose=verbose)
    # tstat3 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=True, sec_data=True, verbose=verbose)
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

    # TCA.plate_heatmap_p(plaque, both=True)
    # TCA.plot_wells(plaque, neg=neg, pos=pos)
    # TCA.plot_plate_3d(plaque['rep1'].sec_array, surf=True)
    # TCA.plot_plate_3d(plaque.sec_array)
    # TCA.plot_plate_3d(plaque.array, surf=True)
    # TCA.plate_heatmap_p(plaque)
    # TCA.heatmap_map_p(plaque, usesec=True)
    # TCA.plate_heatmap_p(plaque, both=False)
    # TCA.dual_flashlight_plot(plaque.array, ssmd)
    # TCA.boxplot_by_wells(plaque['rep1'].rawdata.df, channel=channel)
    # TCA.plot_distribution(wells=['B5', 'B6'], plate=plaque, channel=channel)

HDV()


def HCV():
    plate_nb = '2'
    plaque = TCA.Core.Plate(name='Plate' + plate_nb)
    platemap = TCA.Core.PlateMap(platemap="/home/arnaud/Desktop/ANTAGOMIR_MIMIC/antagomir/Pl" + plate_nb + "PP.csv")
    plaque + platemap
    try:
        file = "/home/arnaud/Desktop/ANTAGOMIR_MIMIC/antagomir/Pl" + plate_nb + "rep_1.csv"
        if os.path.isfile(file):
            plaque + TCA.Core.Replica(name="rep1",
                                      data=file,
                                      datatype='mean')
    except:
        pass
    try:
        file = "/home/arnaud/Desktop/ANTAGOMIR_MIMIC/antagomir/Pl" + plate_nb + "rep_2.csv"
        if os.path.isfile(file):
            plaque + TCA.Core.Replica(name="rep2",
                                      data=file,
                                      datatype='mean')
    except:
        pass
    try:
        file = "/home/arnaud/Desktop/ANTAGOMIR_MIMIC/antagomir/Pl" + plate_nb + "rep_3.csv"
        if os.path.isfile(file):
            plaque + TCA.Core.Replica(name="rep3",
                                      data=file,
                                      datatype='mean')
    except:
        pass

    channel = 'Nuc Intensity'
    neg = 'NT'
    pos = 'SINV C'

    TCA.plate_quality_control(plaque, channel=channel, cneg=neg, cpos=pos, use_raw_data=True, verbose=True)

    ana = TCA.plate_analysis(plaque, channel, neg, pos, threshold=50, percent=True)
    # # ana = TCA.plate_analysis(plaque, [channel], neg, pos)
    print(ana)
    # ana.write("/home/arnaud/Desktop/HDV/RawdataClean/Percentvalue"+plate_nb+".csv")

    plaque.normalization_channels(channels=channel,
                                  method='Zscore',
                                  log=True,
                                  neg=platemap.search_well(neg),
                                  pos=platemap.search_well(pos))
    print(platemap)

    alpha = 0.1
    verbose = True
    try:
        TCA.systematic_error_detection_test(plaque['rep1'].array, verbose=verbose, alpha=alpha)
        TCA.systematic_error_detection_test(plaque['rep2'].array, verbose=verbose, alpha=alpha)
        TCA.systematic_error_detection_test(plaque['rep3'].array, verbose=verbose, alpha=alpha)
    except KeyError:
        pass
    plaque.systematic_error_correction(algorithm="MEA", apply_down=True, save=True, verbose=verbose, alpha=alpha,
                                       max_iterations=50, skip_col=[0, 11])

    # #### Single Cell
    # TCA.independance(plaque, neg='Neg', channel=channel)
    # TCA.rank_product(plaque, secdata=True, verbose=True)

    sec = True
    TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec, verbose=verbose)
    TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec, variance="equal",
                         verbose=verbose)
    TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=sec, verbose=verbose)
    TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=sec, method='MM',
                         verbose=verbose)
    TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, variance='equal', sec_data=sec, verbose=verbose)
    TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, sec_data=sec, verbose=verbose)
    TCA.plate_tstat_score(plaque, neg_control=neg, paired=True, sec_data=sec, verbose=verbose)

    __SIZE__ = 96
    # ssmd1 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=True,
    #                              verbose=verbose)
    # ssmd2 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=False,
    #                              variance="equal", verbose=verbose)
    # ssmd3 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=True,
    #                              verbose=verbose)
    # ssmd4 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=True,
    #                              method='MM', verbose=verbose)
    # tstat1 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, variance='equal', sec_data=True,
    #                                verbose=verbose)
    # tstat2 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, sec_data=True, verbose=verbose)
    # tstat3 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=True, sec_data=True, verbose=verbose)
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

    TCA.plate_heatmap_p(plaque, both=True)
    # TCA.plot_wells(plaque, neg=neg, pos=pos)
    # TCA.plot_plate_3d(plaque['rep1'].sec_array, surf=True)
    # TCA.plot_plate_3d(plaque.sec_array)
    # TCA.plot_plate_3d(plaque.array, surf=True)
    # TCA.plate_heatmap_p(plaque)
    # TCA.heatmap_map_p(plaque, usesec=True)
    # TCA.plate_heatmap_p(plaque, both=False)
    # TCA.dual_flashlight_plot(plaque.array, ssmd)
    # TCA.boxplot_by_wells(plaque['rep1'].rawdata.df, channel=channel)
    # TCA.plot_distribution(wells=['B5', 'B6'], plate=plaque, channel=channel)

# HCV()


def go():
    """
    Go Enrichment testing
    """
    import TransCellAssay as TCA
    enrichment = TCA.EnrichmentStudy(study="/home/arnaud/Desktop/TEMP/study.txt",
                                     pop="/home/arnaud/Desktop/TEMP/pop.txt",
                                     assoc="/home/arnaud/Desktop/TEMP/assoc.csv",
                                     compare=False)
    result = enrichment.to_dataframe()
    print(pd.DataFrame(result))

# go()


def rest():
    # k = TCA.KEGG(verbose=True)
    # # target = ["NXF1", "ALAS2", "GPI", "EIF4A3", "RRM2", "RAD51L3", "KIF26A", "CDC5L", "ABCC3", "ATP1B2"]
    # target = ["NXF1"]
    # for gene in target:
    #     try:
    #         # res = k.find("hsa", gene)
    #         # print(res)
    #         des = k.get(":".join(["hsa", gene]))
    #         # print(des)
    #
    #         # res = TCA.KEGGParser(des)
    #         # print(res['PATHWAY'])
    #         # print(json.dumps(res, indent=4))
    #
    #         # path = k.get(res['PATHWAY'][0].split()[0], "kgml")
    #         # print(path)
    #
    #     except:
    #         pass
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    psi = TCA.PSICQUIC()
    psi.TIMEOUT = 10
    psi.RETRIES = 1
    psi.retrieve_all('NXF1')

# rest()

print('FINISH')
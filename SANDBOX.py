#!/usr/bin/env python3
# encoding: utf-8
"""
For testing module in actual dev
"""
import pandas as pd
import numpy as np
import os
import fnmatch
import TransCellAssay as TCA
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)
np.set_printoptions(linewidth=300)
np.set_printoptions(suppress=True, precision=4)


def HDV(plate_nb):
    tag = 'subset'
    path = '/home/arnaud/Desktop/HDV/DATA/'

    plaque = TCA.Core.Plate(name='HDV_' + tag + plate_nb)
    platemap = TCA.Core.PlateMap(platemap=path+tag+"_PP_"+plate_nb+".csv")
    plaque + platemap
    for i in ['1', '2', '3']:
        try:
            file = path+tag+"_" + plate_nb + "."+i+".csv"
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name="rep"+i,
                                          data=file,
                                          datatype='mean')
        except Exception as e:
            print(e)
            pass

    channel = 'AvgIntenCh2'
    neg = 'Neg infecté'
    pos = 'SiNTCP infecté'

    outpath = '/home/arnaud/Desktop/HDV/DATA/Final_Analyze/SCORING/'
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    # TCA.plate_analysis(plaque, channel, neg, pos, threshold=600, percent=False)
    # plaque.normalization_channels(channels=channel,
    #                               log_t=False,
    #                               method='PercentOfSample',
    #                               neg=platemap.search_well(neg),
    #                               pos=platemap.search_well(pos))

    # TCA.plate_filtering(plaque, channel=channel, upper=150, lower=50, include=True, percent=False)

    # plaque.check_data_consistency()
    # TCA.plate_quality_control(plaque, channel=channel, cneg=neg, cpos=pos, use_raw_data=True, verbose=True)
    # TCA.ReferenceDataWriter(plaque,
    #                         filepath='/home/arnaud/Desktop/test.xlsx',
    #                         ref=['Neg', 'F1 ATPase A', 'F1 ATPase B'],
    #                         channels=["ROI_B_Target_I_ObjectTotalInten", "ROI_A_Target_I_ObjectTotalInten"])

    # ana = TCA.plate_analysis(plaque, channel, neg, pos, threshold=85, percent=True, path=outpath)
    # ana = TCA.plate_analysis(plaque, channel, neg, pos, threshold=600, percent=False)
    # ana = TCA.plate_analysis(plaque, channel, neg, pos)
    # print(ana)

    # array = ana.values['PositiveCells']
    # array = array.flatten().reshape(platemap.shape())
    # TCA.heatmap_p(array)

    # plaque.compute_data_from_replicat(channel=channel)

    # plaque.normalization_channels(channels=channel,
    #                               log_t=False,
    #                               method='PercentOfControl',
    #                               neg=platemap.search_well(neg),
    #                               pos=platemap.search_well(pos))

    plaque.compute_data_from_replica(channel=channel)
    plaque.cut(1, 15, 1, 23, apply_down=True)
    # print(platemap)
    plaque.compute_data_from_replica(channel=channel)

    # # Keep only neg or pos in 3D plot
    # test1_neg = TCA.get_masked_array(plaque.array, platemap.platemap.values, to_keep=neg)
    # test1_pos = TCA.get_masked_array(plaque.array, platemap.platemap.values, to_keep=pos)
    # TCA.plot_plate_3d(test1_neg)
    # TCA.plot_plate_3d(test1_pos)

    alpha = 0.1
    verbose = True
    try:
        TCA.systematic_error_detection_test(plaque['rep1'].array, verbose=verbose, alpha=alpha)
        TCA.systematic_error_detection_test(plaque['rep2'].array, verbose=verbose, alpha=alpha)
        TCA.systematic_error_detection_test(plaque['rep3'].array, verbose=verbose, alpha=alpha)
    except KeyError:
        pass
    # plaque.systematic_error_correction(algorithm="PMP", apply_down=True, save=True, verbose=verbose, alpha=alpha,
    #                                    max_iterations=50)

    # #### Single Cell
    # TCA.rank_product(plaque, secdata=True)

    sec = False
    # ssmd1 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec,
    #                              verbose=verbose)
    # ssmd2 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec,
    #                              variance="equal", verbose=verbose)
    # ssmd3 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=sec,
    #                              verbose=verbose)
    # ssmd4 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=sec, method='MM',
    #                              verbose=verbose)
    # tstat1 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, variance='equal', sec_data=sec,
    #                                verbose=verbose, robust=True)
    # tstat2 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, sec_data=sec, verbose=verbose, robust=True)
    # tstat3 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=True, sec_data=sec, verbose=verbose, robust=True)
    #
    # ttest1, fdr1 = TCA.plate_ttest(plaque, neg, verbose=verbose)
    # ttest2, fdr2 = TCA.plate_ttest(plaque, neg, equal_var=True, verbose=verbose)
    #
    # __SIZE__ = len(platemap.platemap.values.flatten())
    #
    # gene = plaque.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
    # final_array = np.append(gene, np.repeat([str(plaque.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, plaque.array.flatten().reshape(__SIZE__, 1), axis=1)
    # try:
    #     final_array = np.append(final_array, plaque['rep1'].array.flatten().reshape(__SIZE__, 1), axis=1)
    # except:
    #     final_array = np.append(final_array, np.repeat([0], __SIZE__).reshape(__SIZE__, 1), axis=1)
    # try:
    #     final_array = np.append(final_array, plaque['rep2'].array.flatten().reshape(__SIZE__, 1), axis=1)
    # except:
    #     final_array = np.append(final_array, np.repeat([0], __SIZE__).reshape(__SIZE__, 1), axis=1)
    # try:
    #     final_array = np.append(final_array, plaque['rep3'].array.flatten().reshape(__SIZE__, 1), axis=1)
    # except:
    #     final_array = np.append(final_array, np.repeat([0], __SIZE__).reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ssmd1.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ssmd2.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ssmd3.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ssmd4.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, tstat1.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, tstat2.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, tstat3.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ttest1.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, fdr1.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, ttest2.flatten().reshape(__SIZE__, 1), axis=1)
    # final_array = np.append(final_array, fdr2.flatten().reshape(__SIZE__, 1), axis=1)
    #
    # to_save = pd.DataFrame(final_array)
    # to_save.to_csv(os.path.join(outpath, plaque.name+'.csv'), index=False, header=False)

    # TCA.plate_heatmap_p(plaque, both=False)
    # TCA.plot_wells(plaque, neg=neg, pos=pos)
    # TCA.plot_plate_3d(plaque['rep1'].sec_array, surf=True)
    # TCA.plot_plate_3d(plaque.sec_array)
    # TCA.plot_plate_3d(plaque.array, surf=True)
    # TCA.plate_heatmap_p(plaque)
    # TCA.heatmap_map_p(plaque, usesec=True)
    # TCA.plate_heatmap_p(plaque, both=False)
    # TCA.dual_flashlight_plot(plaque.array, ssmd)
    # TCA.boxplot_by_wells(plaque['rep1'].rawdata.df, channel=channel)
    # TCA.plot_distribution(wells=['E2', 'F2'], plate=plaque, channel=channel, pool=True)

# for i in range(1, 2, 1):
#     HDV(str(i))


def PRESTWICK():
    path = '/home/arnaud/Desktop/PRESTWICK/Mouse/Repeat2/'

    cell_line = 'Def'
    PlateList_Def = []
    for i in range(1, 17, 1):
        plaque = TCA.Core.Plate(name='Mouse_repeat1_'+cell_line + str(i))
        platemap = TCA.Core.PlateMap(platemap=path+"Pl"+str(i)+"PP.csv")
        plaque + platemap
        for j in range(1, 4, 1):
            try:
                file = path+cell_line+"_PL" + str(i) + "."+str(j)+".csv"
                if os.path.isfile(file):
                    plaque + TCA.Core.Replica(name="rep"+str(j),
                                              data=np.loadtxt(file, delimiter=','),
                                              single=False,
                                              datatype='mean')
            except:
                pass
        PlateList_Def.append(plaque)

    cell_line = 'Pro'
    PlateList_Pro = []
    for i in range(1, 17, 1):
        plaque = TCA.Core.Plate(name='Mouse_repeat1_'+cell_line + str(i))
        platemap = TCA.Core.PlateMap(platemap=path+"Pl"+str(i)+"PP.csv")
        plaque + platemap
        for j in range(1, 4, 1):
            try:
                file = path+cell_line+"_PL" + str(i) + "."+str(j)+".csv"
                if os.path.isfile(file):
                    plaque + TCA.Core.Replica(name="rep"+str(j),
                                              data=np.loadtxt(file, delimiter=','),
                                              single=False,
                                              datatype='mean')
            except:
                pass
        PlateList_Pro.append(plaque)

    # # Control plate
    ControlPlate = TCA.Core.Plate(name='Control')
    platemapC = TCA.Core.PlateMap(platemap=path+"PlXXPP.csv")
    ControlPlate + platemapC
    i = 1
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, '*Control*'):
            ControlPlate + TCA.Core.Replica(name="rep"+str(i),
                                            data=np.loadtxt(os.path.join(path, file), delimiter=','),
                                            single=False,
                                            datatype='mean')
            i += 1

    neg = 'DMSO'

    ControlPlate.compute_data_from_replica(channel='')
    ControlPlate.cut(0, 9, 1, 11, apply_down=True)

    # # median normalized plate
    for plaque in PlateList_Def:
        plaque.compute_data_from_replica(channel='')
        plaque.cut(0, 9, 1, 11, apply_down=True)
        for key, value in plaque.replica.items():
            value.array = value.array/np.median(value.array.flatten())
    for plaque in PlateList_Pro:
        plaque.compute_data_from_replica(channel='')
        plaque.cut(0, 9, 1, 11, apply_down=True)
        for key, value in plaque.replica.items():
            value.array = value.array/np.median(value.array.flatten())

    for key, value in ControlPlate.replica.items():
        value.array = value.array/np.median(value.array.flatten())

    verbose = True
    sec = False

    output_path = os.path.join(path, 'Hit_score_commonContPlate')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for plaque in PlateList_Def:
        ssmd1 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec,
                                     verbose=verbose, control_plate=ControlPlate)
        ssmd2 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec,
                                     variance="equal", verbose=verbose, control_plate=ControlPlate)
        tstat1 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, variance='equal', sec_data=sec,
                                       verbose=verbose, control_plate=ControlPlate)
        tstat2 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, sec_data=sec, verbose=verbose,
                                       control_plate=ControlPlate)
        ttest1, fdr1 = TCA.plate_ttest(plaque, neg, verbose=verbose, control_plate=ControlPlate)
        ttest2, fdr2 = TCA.plate_ttest(plaque, neg, equal_var=True, verbose=verbose, control_plate=ControlPlate)

        __SIZE__ = len(plaque.platemap.platemap.values.flatten())

        gene = plaque.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
        final_array = np.append(gene, np.repeat([str(plaque.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, plaque['rep1'].array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, plaque['rep2'].array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, plaque['rep3'].array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ssmd1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ssmd2.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, tstat1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, tstat2.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ttest1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, fdr1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ttest2.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, fdr2.flatten().reshape(__SIZE__, 1), axis=1)

        to_save = pd.DataFrame(final_array)
        to_save.to_csv(os.path.join(output_path, 'HIT_'+plaque.name+'.csv'), index=False, header=False)

    for plaque in PlateList_Pro:
        ssmd1 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec,
                                     verbose=verbose, control_plate=ControlPlate)
        ssmd2 = TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=sec,
                                     variance="equal", verbose=verbose, control_plate=ControlPlate)
        tstat1 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, variance='equal', sec_data=sec,
                                       verbose=verbose, control_plate=ControlPlate)
        tstat2 = TCA.plate_tstat_score(plaque, neg_control=neg, paired=False, sec_data=sec, verbose=verbose,
                                       control_plate=ControlPlate)
        ttest1, fdr1 = TCA.plate_ttest(plaque, neg, verbose=verbose, control_plate=ControlPlate)
        ttest2, fdr2 = TCA.plate_ttest(plaque, neg, equal_var=True, verbose=verbose, control_plate=ControlPlate)

        __SIZE__ = len(plaque.platemap.platemap.values.flatten())

        gene = plaque.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
        final_array = np.append(gene, np.repeat([str(plaque.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, plaque['rep1'].array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, plaque['rep2'].array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, plaque['rep3'].array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ssmd1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ssmd2.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, tstat1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, tstat2.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ttest1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, fdr1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ttest2.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, fdr2.flatten().reshape(__SIZE__, 1), axis=1)

        to_save = pd.DataFrame(final_array)
        to_save.to_csv(os.path.join(output_path, 'HIT_'+plaque.name+'.csv'), index=False, header=False)

    # TCA.plot_wells(PlateList)
    # TCA.heatmap_map_p(PlateList, usesec=False)

# PRESTWICK()


def Schneider():
    path = '/home/arnaud/Desktop/Schneider/red_green/'

    outpath = os.path.join(path, 'red')
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    channel = 'hetero rouge - bckg rouge'
    neg = 'Scramble'
    pos = 'SUV39POOL'

    PlateList = []
    for i in range(1, 4, 1):
        plaque = TCA.Core.Plate(name='Plaque'+str(i))
        platemap = TCA.Core.PlateMap(platemap=path+"Pl"+str(i)+"PP.csv")
        plaque + platemap
        for j in range(3):
            try:
                file = path+"Pl" + str(i) + "."+str(j)+".csv"
                if os.path.isfile(file):
                    plaque + TCA.Core.Replica(name="rep"+str(j),
                                              data=file,
                                              single=True,
                                              datatype='mean')
            except:
                pass
        PlateList.append(plaque)

    for plate in PlateList:
        TCA.plate_analysis(plate, channel, neg, pos, threshold=50, percent=True, path=outpath)

# Schneider()


def zita():
    path = '/home/arnaud/Desktop/Anne/Zita/'

    outpath = os.path.join(path, 'RES2')
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    channel = 'TargetTotalIntenCh2'
    neg = 'siSCR no UV b'
    pos = 'siSCR UV'

    PlateList = []
    for i in range(1, 3, 1):
        plaque = TCA.Core.Plate(name='Plaque'+str(i))
        platemap = TCA.Core.PlateMap(platemap=path+"Pl"+str(i)+"PP.csv")
        plaque + platemap
        try:
            file = path+"150415 Zita marquage 6-4P Plaque"+str(i)+".csv"
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name="rep1",
                                          data=file,
                                          single=True,
                                          datatype='mean')
        except:
            pass
        PlateList.append(plaque)

    for plate in PlateList:
        TCA.plate_analysis(plate, channel, neg, pos, threshold=5, percent=True, path=outpath)

# zita()


def misc():
    path = '/home/arnaud/Desktop/TargetActivation.V4_04-23-15_01;16;00/'

    outpath = os.path.join(path, '600')
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    channel = 'AvgIntenCh2'
    neg = 'Infectées'
    pos = 'Cyclo i'

    PlateList = []
    for i in range(1, 2, 1):
        plaque = TCA.Core.Plate(name='Plaque'+str(i))
        platemap = TCA.Core.PlateMap(platemap=path+"PP_hdv.csv")
        plaque + platemap
        try:
            file = os.path.join(path+"150423 z factor prestwick.csv")
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name="rep1",
                                          data=file,
                                          single=True,
                                          datatype='mean')
        except:
            pass
        PlateList.append(plaque)

    for plate in PlateList:
        TCA.plate_analysis(plate, channel, neg, pos, threshold=600, percent=False, fixed_threshold=True)
        # TCA.plot_distribution(wells=['E2', 'F2'], plate=plate, channel=channel, pool=True)

misc()
print('FINISH')
#!/usr/bin/env python3
# encoding: utf-8
"""
For testing module in actual dev
"""
import pandas as pd
import numpy as np
import os
import cProfile
import TransCellAssay as TCA
import logging
import copy

logging.basicConfig(level=logging.INFO, format='[%(process)d/%(processName)s] @ [%(asctime)s] - %(levelname)-8s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
pd.set_option('display.max_rows',40)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)
np.set_printoptions(linewidth=300)
np.set_printoptions(suppress=True, precision=4)


def HDV():
    channel = 'AvgIntenCh2'
    neg = 'I'
    pos = 'Cyclosporine I'
    for j in range(1, 2, 1):
        # path = '/home/arnaud/Desktop/HDV/DATA'
        path = '/home/arnaud/Desktop/HDV prestwick/screen/'

        plaque = TCA.Core.Plate(name='HDV prestwick '+str(j),
                                platemap=TCA.Core.PlateMap(fpath=os.path.join(path, "PP_pl"+str(j)+".csv")))
        for i in ['1', '2', '3']:
            try:
                file = os.path.join(path, 'HDV prestwick pl'+str(j)+"."+str(i)+".csv")
                if os.path.isfile(file):
                    plaque + TCA.Core.Replica(name="rep" + i,
                                              fpath=file,
                                              datatype='mean')
            except Exception as e:
                print(e)
                pass
        plaque.agg_data_from_replica_channel(channel=channel)
        # TCA.systematic_error(plaque.array)
        # plaque.cut(1, 15, 1, 23, apply_down=True)
        #
        # arr = plaque.array.copy()
        #
        # a = TCA.lowess_fitting(arr.copy())
        # b = TCA.lowess_fitting(arr.copy(), max_iteration=10)
        # c = TCA.polynomial_fitting(arr.copy())
        # d = TCA.polynomial_fitting(arr.copy(), degree=5)
        # grand_effect, col_effects, row_effects, e, tbl_org = TCA.median_polish(arr.copy())
        # f = TCA.matrix_error_amendmend(arr.copy())
        # g = TCA.partial_mean_polish(arr.copy())
        #
        # TCA.heatmap_p(arr, file_path="/home/arnaud/Desktop/Comparaison_methode_normalisation/org.jpg")
        # TCA.heatmap_p(a, file_path="/home/arnaud/Desktop/Comparaison_methode_normalisation/lowess.jpg")
        # TCA.heatmap_p(b, file_path="/home/arnaud/Desktop/Comparaison_methode_normalisation/lowess_iter10.jpg")
        # TCA.heatmap_p(c, file_path="/home/arnaud/Desktop/Comparaison_methode_normalisation/poly_deg4.jpg")
        # TCA.heatmap_p(d, file_path="/home/arnaud/Desktop/Comparaison_methode_normalisation/poly_deg5.jpg")
        # TCA.heatmap_p(e, file_path="/home/arnaud/Desktop/Comparaison_methode_normalisation/medianpol.jpg")
        # TCA.heatmap_p(f, file_path="/home/arnaud/Desktop/Comparaison_methode_normalisation/mea.jpg")
        # TCA.heatmap_p(g, file_path="/home/arnaud/Desktop/Comparaison_methode_normalisation/pmp.jpg")


        # plaque.check_data_consistency()
        # print(plaque)
        # print(plaque.get_replica_file_location())
        # print(plaque.get_replica_listId())
        # print(plaque.get_file_location())
        # x = plaque.get_raw_data(channel=channel, well='B16')
        # print(x)
        # print(TCA.plate_channel_analysis(plaque, channel=channel, neg=neg, pos=pos, threshold=85, clean=True))
        # TCA.plate_channel_analysis(plaque, channel=channel, neg=neg, pos=pos, threshold=88, percent=True, path=path,
        #                            clean=True, tag='12_%')
        # plaque.agg_data_from_replica_channel(channel=channel)
        # for key, value in plaque.replica.items():
            # print(value.array)
        # print(plaque.get_count())
        TCA.heatmap_p(plaque.array, annot=True)
        # TCA.RepCor(plaque, channel)
        # TCA.plate_heatmap_p(plaque, both=False, size=6.)
        # TCA.systematic_error(plaque.array, file_path=None)
        # TCA.plot_wells(plaque, neg=neg, pos=pos, file_path=os.path.join(path, "Wells "+plaque.name+".pdf"))
        # print(plaque)
        del plaque

# HDV()

def misc2():
    path = '/home/arnaud/Desktop/Anne/150915 V Lamour U2OS Ku80 53BP1 spot/'

    # outpath = os.path.join(path, 'ratio')
    # if not os.path.isdir(outpath):
    #     os.makedirs(outpath)

    PlateList = []

    NameList = ['150914 V Lamour Ku80 53BP1.csv']
    for name in NameList:
        plaque = TCA.Core.Plate(name=name[0:-4],
                                platemap=TCA.Core.PlateMap(),
                                replica=TCA.Core.Replica(name="rep1",
                                                         fpath=os.path.join(path, str(name)),
                                                         singleCells=True,
                                                         datatype='mean'))
        PlateList.append(plaque)


    for plate in PlateList:
        # print(plate)
        TCA.plate_channels_analysis(plate, neg='A1', pos="B10", channels=['SpotCountCh2', 'SpotCountCh3',
        'SpotTotalAreaCh2', 'SpotTotalAreaCh3', 'SpotTotalIntenCh2', 'SpotTotalIntenCh3'], threshold=95, percent=True,
                                    path=path, clean=True)

# misc2()

def misc():
    path = '/home/arnaud/Desktop/TEMP/Amelie/xavier_g/300915/LigneEF_ctrlF2FD3'
    PlateList = []

    # NameList = ['150630 siP150 Xavier Gaume Pl2.csv', '150629 siP150 Xavier Gaume Pl1.csv']
    # NameList = ['150629 siP150 Xavier Gaume Pl1.csv']
    plaque = TCA.Core.Plate(name='150923 test differents serums Gaume ligne EF',
                            platemap=TCA.Core.PlateMap(),
                            replica=TCA.Core.Replica(name="rep1",
                                                     fpath="/home/arnaud/Desktop/TEMP/Amelie/xavier_g/300915/150923 test differents serums Gaume ligne EF.csv",
                                                     singleCells=True,
                                                     datatype='mean'))
    # plaque.agg_data_from_replica_channel(channel='AvgIntenCh3')

    plaque.platemap['F2'] = "neg"
    plaque.platemap['F3'] = "neg"
    # plaque.platemap['C5'] = "neg"
    # plaque.platemap['D5'] = "neg"

    channel1 = ['AvgIntenCh2']
    a = TCA.plate_channels_analysis(plaque, neg="neg", channels=channel1, threshold=99.5, percent=True, clean=True, path=path)
    channel2 = ['AvgIntenCh3']
    b = TCA.plate_channels_analysis(plaque, neg="neg", channels=channel2, threshold=1, percent=True, clean=True, path=path)
    channel3 = ['AvgIntenCh4']
    c = TCA.plate_channels_analysis(plaque, neg="neg", channels=channel3, threshold=2000, percent=False, fixed_threshold=True, clean=True, path=path)

    # write txt file for saving intensities values of threshold
    file = open(os.path.join(path, str(plaque.name)+'_IntensitiesThresholdValues.txt'), 'w')
    file.write(str(channel1[0])+" : " + str(a[channel1[0]][1]) + "\n")
    file.write(str(channel2[0])+" : " + str(b[channel2[0]][1]) + "\n")
    file.write(str(channel3[0])+" : " + str(c[channel3[0]][1]) + "\n")
    file.close()


    plaque.clear_memory(only_cache=True)
    plaqueCP = copy.deepcopy(plaque)
    TCA.channel_filtering(plaqueCP, channel=channel1[0], lower=int(a[channel1[0]][1]), include=True, percent=False)
    TCA.channel_filtering(plaqueCP, channel=channel2[0], upper=int(b[channel2[0]][1]), include=True, percent=False)
    # TCA.channel_filtering(plaqueCP, channel=channel3[0], lower=int(c[channel3[0]][1]), include=True, percent=False)
    gb_data = plaqueCP['rep1'].rawdata.get_groupby_data()
    cnt = gb_data.Well.count().to_frame()
    cnt.columns = ['Count']
    cnt.to_csv(os.path.join(path, "CellCnt_GFP+Oct34-_"+plaque.name+'.csv'))

    plaqueCP = copy.deepcopy(plaque)
    TCA.channel_filtering(plaqueCP, channel=channel1[0], lower=int(a[channel1[0]][1]), include=True, percent=False)
    # TCA.channel_filtering(plaqueCP, channel=channel2[0], upper=int(b[channel2[0]][1]), include=True, percent=False)
    TCA.channel_filtering(plaqueCP, channel=channel3[0], lower=int(c[channel3[0]][1]), include=True, percent=False)
    gb_data = plaqueCP['rep1'].rawdata.get_groupby_data()
    cnt = gb_data.Well.count().to_frame()
    cnt.columns = ['Count']
    cnt.to_csv(os.path.join(path, "CellCnt_GFP+Zscan4+_"+plaque.name+'.csv'))

    plaqueCP = copy.deepcopy(plaque)
    # TCA.channel_filtering(plaqueCP, channel=channel1[0], lower=int(a[channel1[0]][1]), include=True, percent=False)
    TCA.channel_filtering(plaqueCP, channel=channel2[0], upper=int(b[channel2[0]][1]), include=True, percent=False)
    TCA.channel_filtering(plaqueCP, channel=channel3[0], lower=int(c[channel3[0]][1]), include=True, percent=False)
    gb_data = plaqueCP['rep1'].rawdata.get_groupby_data()
    cnt = gb_data.Well.count().to_frame()
    cnt.columns = ['Count']
    cnt.to_csv(os.path.join(path, "CellCnt_Oct34-Zscan4+"+plaque.name+'.csv'))

    plaqueCP = copy.deepcopy(plaque)
    TCA.channel_filtering(plaqueCP, channel=channel1[0], lower=int(a[channel1[0]][1]), include=True, percent=False)
    TCA.channel_filtering(plaqueCP, channel=channel2[0], upper=int(b[channel2[0]][1]), include=True, percent=False)
    TCA.channel_filtering(plaqueCP, channel=channel3[0], lower=int(c[channel3[0]][1]), include=True, percent=False)
    gb_data = plaqueCP['rep1'].rawdata.get_groupby_data()
    cnt = gb_data.Well.count().to_frame()
    cnt.columns = ['Count']
    cnt.to_csv(os.path.join(path, "CellCnt_GFP+Oct34-Zscan4+"+plaque.name+'.csv'))


misc()

# x =TCA.PlateMap(size=1536)
# print(x.platemap.values)

#######################################################################################################################
#######################################################################################################################
#                           COLLECTIONS OF FUNCTIONS                                                                  #
#######################################################################################################################
#######################################################################################################################

# x = TCA.DoseResponseCurve(func='4pl')


# pm = TCA.PlateMap(size=96)
# print(pm)
# pm2 = TCA.PlateMap(fpath='/home/arnaud/Desktop/PP_96.csv')
# print(pm2)
# print(pm['D6'])
# print(pm2['D6'])
# cProfile.run('[TCA.get_opposite_well_format("B12", bignum=True) for i in range(1000)]')
# cProfile.run('[TCA.get_opposite_well_format("B12") for i in range(1000)]')

############################
# ##### FUNCTION POOL ######
############################

# TCA.plate_channel_analysis(plaque, neg=neg, pos=pos, channel=channel, threshold=600, percent=False,
#                            fixed_threshold=True, clean=True, tag='600', path=outpath)
# TCA.plate_channel_analysis(plaque, neg=neg, pos=pos, channel=channel, threshold=85, percent=True,
#                            clean=True, tag='15', path=outpath)

# TCA.plate_channel_analysis(plaque, channel, neg, pos, threshold=600, percent=False)
# plaque.normalization_channels(channels=channel,
#                               log_t=False,
#                               method='PercentOfSample',
#                               neg=platemap.search_well(neg),
#                               pos=platemap.search_well(pos))

# TCA.plate_filtering(plaque, channel=channel, upper=150, lower=50, include=True, percent=False)

# plaque.check_data_consistency()
# TCA.plate_quality_control(plaque, channel=channel, cneg=neg, cpos=pos, use_raw_data=True,
# dirpath="/home/arnaud/Desktop/")
# TCA.ReferenceDataWriter(plaque,
#                         filepath='/home/arnaud/Desktop/test.xlsx',
#                         ref=['Neg infecté', 'SiNTCP infecté'],
#                         channels=['AvgIntenCh2'])

# ana = TCA.plate_channel_analysis(plaque, channel, neg, pos, threshold=85, percent=True)
# ana = TCA.plate_channel_analysis(plaque, channel, neg, pos, threshold=600, percent=False)
# ana = TCA.plate_channel_analysiss(plaque, channel, neg, pos)
# print(ana)

# array = ana.values['PositiveCells']
# array = array.flatten().reshape(platemap.shape())
# TCA.heatmap_p(array)

# plaque.normalization_channels(channels=channel,
#                               log_t=False,
#                               method='PercentOfControl',
#                               neg=platemap.search_well(neg),
#                               pos=platemap.search_well(pos))

# plaque.agg_data_from_replica_channel(channel=channel)
# plaque.cut(1, 15, 1, 23, apply_down=True)
# # print(platemap)
# plaque.agg_data_from_replica_channel(channel=channel)

# # Keep only neg or pos in 3D plot
# test1_neg = TCA.get_masked_array(plaque.array, platemap.platemap.values, to_keep=neg)
# test1_pos = TCA.get_masked_array(plaque.array, platemap.platemap.values, to_keep=pos)
# TCA.plot_plate_3d(test1_neg)
# TCA.plot_plate_3d(test1_pos)

# alpha = 0.1
# verbose = True
# try:
#     ar1 = TCA.systematic_error_detection_test(plaque['rep1'].array, verbose=verbose, alpha=alpha)
#     ar2 = TCA.systematic_error_detection_test(plaque['rep2'].array, verbose=verbose, alpha=alpha)
#     ar3 = TCA.systematic_error_detection_test(plaque['rep3'].array, verbose=verbose, alpha=alpha)
# except KeyError:
#     pass
#
# arr = ar1+ar2+ar3
# TCA.plot_plate_3d(arr, surf=True)

# plaque.systematic_error_correction(algorithm="PMP", apply_down=True, save=True, verbose=verbose, alpha=alpha,
#                                    max_iterations=50)

# #### Single Cell
# TCA.rank_product(plaque, secdata=True)

# sec = False
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
# TCA.plot_plate_3d(plaque['rep1'].array_c, surf=True)
# TCA.plot_plate_3d(plaque.array_c)
# TCA.plot_plate_3d(plaque.array, surf=True)
# TCA.plate_heatmap_p(plaque)
# TCA.heatmap_map_p(plaque, usesec=True)
# TCA.plate_heatmap_p(plaque, both=False)
# TCA.dual_flashlight_plot(plaque.array, ssmd)
# TCA.boxplot_by_wells(plaque['rep1'].rawdata.df, channel=channel)
# TCA.plot_distribution(wells=['E2', 'F2'], plate=plaque, channel=channel, pool=True)
# TCA.RepCor(plaque)
# plate.replica['rep1'].rawdata.df.to_csv(os.path.join(path, 'siRNA_validation.csv'))
# print(plate)
# print(plate['rep1'])
# print(plate.agg_data_from_replica_channels())
# plate.agg_data_from_replica_channel(channel='TotalIntenCh2')
# print(plate.array)
# qc = TCA.plate_quality_control(plate, channel, cneg=neg, cpos=pos)
# print(qc)
# TCA.plate_channels_analysis(plate, neg="A1", pos='B10', channels=('SpotCountCh2', 'SpotTotalAreaCh2',
#                                                                   'SpotTotalIntenCh2'),
#                             threshold=95, percent=True, clean=True)
# TCA.plate_channel_analysis(plate, neg='DMSO noUV', channel='TotalIntenCh2', threshold=200000, percent=False,
#                            fixed_threshold=True, clean=True, path=path, tag='200000')
# TCA.plate_channel_analysis(plate, neg='DMSO noUV', channel='TotalIntenCh2', threshold=180000, percent=False,
#                            fixed_threshold=True, clean=True, path=path, tag='180000')
# TCA.plate_channel_analysis(plate, neg='DMSO noUV', channel='TotalIntenCh2', threshold=50, percent=True,
#                            clean=True, path=path, tag='50percent')
# TCA.ReferenceDataWriter(plate,
#                         filepath='/home/arnaud/Desktop/test.xlsx',
#                         ref=['scramble', 'Suvh1'],
#                         channels=['Target_I_ratio', 'Target_II_ratio'])
# TCA.plot_distribution_hist(wells=['B2', 'G2'], plate=plate, channel='TotalIntenCh2', pool=True, bins=2000)
# TCA.plot_distribution_kde(wells=['B2', 'B3', 'B4', 'G2', 'G3', 'G4'], plate=plate, channel='TotalIntenCh2',
#                           pool=True)
# plate.agg_data_from_replica_channel(channel='TotalIntenCh2')
# print(plate.agg_data_channels_from_replica())
# TCA.array_surf_3d(plate.array)
# print('MAD')
# print(TCA.mad_based_outlier(plate.array, thresh=3.0))
# print('PERCENTILE')
# print(TCA.percentile_based_outlier(plate.array, threshold=95))
# cluster = TCA.k_mean_clustering(plate)
# cluster.do_cluster()
# TCA.systematic_error_detection_test(plate.array, verbose=True)
# TCA.plot_3d_per_well(plate['rep1'].rawdata, x='TotalIntenCh2', y='AvgIntenCh2', z='ObjectAreaCh1',
#                      single_cell=True)

        # TCA.systematic_error(plaque.array)

        # arr = plaque.array.copy()

        # print(plaque)
        # print(plaque.get_count().transpose())
        # outpath = os.path.join(path, '040815_graph')
        # if not os.path.isdir(outpath):
        #     os.makedirs(outpath)
        #
        # def plot(x, y, well):
        #     datax = plaque.get_raw_data(channel=x, well=well)
        #     datay = plaque.get_raw_data(channel=y, well=well)
        #     TCA.dual_flashlight_plot(datax.values, datay.values, label_x=x, label_y=y, y_lim=9000, x_lim=9000,
        #                              marker='o', color='b', file_path=os.path.join(outpath, plaque.name+'_'+str(x)+'_'+
        #                                                                            str(y) +'_'+ str(well)+'.jpg'))
        #
        # for well in ['A2', 'A3', 'A4', 'B2', 'B3', 'B4', 'C2', 'C3', 'C4', 'D2', 'D3', 'D4', 'E2', 'E3', 'E4', 'F2',
        #              'F3', 'F4', 'G2', 'G3', 'G4', 'H2', 'H3', 'H4']:
        #     plot(x="AvgIntenCh3", y="AvgIntenCh4", well=well)
        #     plot(x="AvgIntenCh3", y="AvgIntenCh5", well=well)
        #
        # plot(x="AvgIntenCh3", y="AvgIntenCh4", well=['A2', 'B2', 'C2', 'D2'])
        # plot(x="AvgIntenCh3", y="AvgIntenCh5", well=['A2', 'B2', 'C2', 'D2'])
        # plot(x="AvgIntenCh3", y="AvgIntenCh4", well=['E2', 'F2', 'G2', 'H2'])
        # plot(x="AvgIntenCh3", y="AvgIntenCh5", well=['E2', 'F2', 'G2', 'H2'])
        # plot(x="AvgIntenCh3", y="AvgIntenCh4", well=['A4', 'B4', 'C4', 'D4'])
        # plot(x="AvgIntenCh3", y="AvgIntenCh5", well=['A4', 'B4', 'C4', 'D4'])
        # plot(x="AvgIntenCh3", y="AvgIntenCh4", well=['E4', 'F4', 'G4', 'H4'])
        # plot(x="AvgIntenCh3", y="AvgIntenCh5", well=['E4', 'F4', 'G4', 'H4'])
        # TCA.wells_sorted(plaque, channel="AvgIntenCh4", wells=["A2", "B2", "C2", "D2"], ascending=False, y_lim=9000,
        #                  file_name=os.path.join(path, name[0:-4]+"A2_D2"+".pdf"))
        # TCA.wells_sorted(plaque, channel="AvgIntenCh4", wells=["E2", "F2", "G2", "H2"], ascending=False, y_lim=9000,
        #                  file_name=os.path.join(path, name[0:-4]+"E2_H2"+".pdf"))
        # TCA.wells_sorted(plaque, channel="AvgIntenCh4", wells=["A3", "B3", "C3", "D3"], ascending=False, y_lim=9000,
        #                  file_name=os.path.join(path, name[0:-4]+"A3_D3"+".pdf"))
        # TCA.wells_sorted(plaque, channel="AvgIntenCh4", wells=["E3", "F3", "G3", "H3"], ascending=False, y_lim=9000,
        #                  file_name=os.path.join(path, name[0:-4]+"E3_H3"+".pdf"))
        # TCA.wells_sorted(plaque, channel="AvgIntenCh4", wells=["A4", "B4", "C4", "D4"], ascending=False, y_lim=9000,
        #                  file_name=os.path.join(path, name[0:-4]+"A4_D4"+".pdf"))
        # TCA.wells_sorted(plaque, channel="AvgIntenCh4", wells=["E4", "F4", "G4", "H4"], ascending=False, y_lim=9000,
        #                  file_name=os.path.join(path, name[0:-4]+"E4_H4"+".pdf"))
        # TCA.wells_sorted(plaque, channel="AvgIntenCh4", wells=["A5", "B5", "C5", "D5"], ascending=False, y_lim=9000,
        #                  file_name=os.path.join(path, name[0:-4]+"A5_D5"+".pdf"))
        # TCA.wells_sorted(plaque, channel="AvgIntenCh4", wells=["E5", "F5", "G5", "H5"], ascending=False, y_lim=9000,
        #                  file_name=os.path.join(path, name[0:-4]+"E5_H5"+".pdf"))


    # for gfpvalue in [2000, 2500, 3000]:
    #     for octvalue in [1500, 2000, 2500]:
    #         for zscanvalue in [1500, 2000]:
    #             filtering(PlateList, gfp=gfpvalue)
    #             filtering(PlateList, oct=octvalue)
    #             filtering(PlateList, zscan=zscanvalue)
    #             filtering(PlateList, gfp=gfpvalue, zscan=zscanvalue)
    #             filtering(PlateList, gfp=gfpvalue, oct=octvalue)
    #             filtering(PlateList, gfp=gfpvalue, oct=octvalue, zscan=zscanvalue)
    #             filtering(PlateList, oct=octvalue, zscan=zscanvalue)


        # for well in ['A2', 'A3', 'A4', 'A5', 'B2', 'B3', 'B4', 'B5', 'C2', 'C3', 'C4', 'C5', 'D2', 'D3', 'D4', 'D5',
        #              'E2', 'E3', 'E4', 'E5', 'F2', 'F3', 'F4', 'F5', 'G2', 'G3', 'G4', 'G5', 'H2', 'H3', 'H4', 'H5']:
        #     for chan in ['AvgIntenCh3', 'AvgIntenCh4', 'AvgIntenCh5']:
        #         TCA.well_sorted(plate['rep1'], str(well), channel=str(chan),
        #                         file_path=os.path.join(outpath, str(well)+'_'+str(chan)+'.jpg'))
        # TCA.well_count(plate['rep1'])
        # x = plaque.platemap.platemap.values.flatten().tolist()
        # x.remove('B2')
        # x.remove('F2')
        # TCA.plot_3d_per_well(plaque['rep1'].rawdata, x='AvgIntenCh3', y='AvgIntenCh4', z='AvgIntenCh5', skip_wells=x)

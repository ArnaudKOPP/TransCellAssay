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


def HDV():
    tag = 'pretraitement'
    path = '/home/arnaud/Desktop/HDV prestwick/Prétraitement/'

    plaque = TCA.Core.Plate(name='HDV_' + tag)
    plaque.platemap.set_platemap(file_path="/home/arnaud/Desktop/HDV prestwick/PP_HDV_Prestwick.csv")
    for i in ['1', '2', '3']:
        try:
            file = path + "hdvdrugpre"+str(i)+".csv"
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name="rep" + i,
                                          data_file_path=file,
                                          datatype='mean')
        except Exception as e:
            print(e)
            pass

    channel = 'AvgIntenCh2'
    neg = 'I'
    pos = 'Cyclosporine I'

    outpath = path
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

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
    plaque.agg_data_from_replica_channel(channel=channel)

    # # Keep only neg or pos in 3D plot
    # test1_neg = TCA.get_masked_array(plaque.array, platemap.platemap.values, to_keep=neg)
    # test1_pos = TCA.get_masked_array(plaque.array, platemap.platemap.values, to_keep=pos)
    # TCA.plot_plate_3d(test1_neg)
    # TCA.plot_plate_3d(test1_pos)

    alpha = 0.1
    verbose = True
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
    TCA.RepCor(plaque)


# HDV()


def misc():
    path = '/home/arnaud/Desktop/V Lamour/'

    # outpath = os.path.join(path, '600')
    # if not os.path.isdir(outpath):
    #     os.makedirs(outpath)

    PlateList = []
    plaque = TCA.Core.Plate(name='test',
                            platemap=TCA.Core.PlateMap(file_path=os.path.join(path, "PP_96.csv")),
                            replica=TCA.Core.Replica(name="rep1",
                                                     data_file_path=os.path.join(path + "270515 U2OS DXR 53BP1.csv"),
                                                     is_single_cell=True,
                                                     datatype='mean'))

    PlateList.append(plaque)

    for plate in PlateList:
        # plate.replica['rep1'].rawdata.df.to_csv(os.path.join(path, 'siRNA_validation.csv'))
        # print(plate)
        # print(plate['rep1'])
        # print(plate.agg_data_from_replica_channels())
        plate.agg_data_from_replica_channel(channel='TotalIntenCh2')
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
        # TCA.plot_plate_3d(plate.array)
        # print('MAD')
        # print(TCA.mad_based_outlier(plate.array, thresh=3.0))
        # print('PERCENTILE')
        # print(TCA.percentile_based_outlier(plate.array, threshold=95))
        # cluster = TCA.k_mean_clustering(plate)
        # cluster.do_cluster()
        TCA.plot_3d_per_well(plate['rep1'].rawdata.df, x='TotalIntenCh2', y='AvgIntenCh2', z='ObjectAreaCh1',
                             single_cell=False)


misc()

# import cProfile
# cProfile.run('[TCA.get_opposite_well_format("B12", bignum=True) for i in range(1000)]')
# cProfile.run('[TCA.get_opposite_well_format("B12") for i in range(1000)]')

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
pd.set_option('display.max_rows',50)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 1000)
np.set_printoptions(linewidth=300)
np.set_printoptions(suppress=True, precision=4)

def DUX4_4x():

    DataPath = "/home/akopp/Documents/DUX4_siRNA/DATA_4x/"
    PPPath = '/home/akopp/Documents/DUX4_siRNA/BANK/'
    ResPath = "/home/akopp/Documents/DUX4_siRNA/DATA_4x/RESULTAT"
    if not os.path.isdir(ResPath):
        os.makedirs(ResPath)

    ListDF = []
    for i in range(1, 19, 1):
        plaque = TCA.Core.Plate(name='DTarget '+str(i),
                                platemap = TCA.Core.PlateMap(fpath=os.path.join(PPPath, "PP_Drug_Target"+str(i)+'.csv')))
        DF = pd.DataFrame(plaque.platemap.as_array())
        __SIZE__ = len(plaque.platemap.platemap.values.flatten())
        DF.loc[:, "PlateName"] = np.repeat([str(plaque.name)], __SIZE__).reshape(__SIZE__, 1)

        for j in ['1', '2', '3']:
            file = os.path.join(DataPath, 'DTarget '+str(i)+'.'+str(j)+'.csv')
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name='rep'+str(j), fpath=file)

        for key, value in plaque:
            value.df.loc[:, "TotalArea"] = value.df.loc[:, "ValidObjectCount"] * value.df.loc[:, "MEAN_ObjectAreaCh1"]

            ## control neg traité alias 'Neg1'
            # neg = value.df.query("Well == ['H2', 'J2', 'L2', 'N2', 'C23', 'E23', 'G23', 'I23']")["TotalArea"].values

            ## control neg non traité alias 'Neg'
            # neg = value.df.query("Well == ['D2', 'E2', 'F2', 'H2', 'J23', 'K23', 'L23', 'M23']")["TotalArea"].values



            # value.df.loc[:, "TotalArea_Ratio"] = (value.df.loc[:, "TotalArea"] / (np.mean(neg))) * 100
            value.df = value.df.dropna(axis=0)
            useless = ['PlateNumber', 'Zposition', 'Status']
            for col in useless:
                try:
                    value.df = value.df.drop([col], axis=1)
                except:
                    pass
            DF = pd.merge(DF, value.df, on='Well', how='outer')

        DF = DF.dropna(axis=0)
        # print(DF)
        ListDF.append(DF)

    DF = pd.concat(ListDF)
    # DF.loc[:, "MEAN_TotalArea"] = (DF.loc[:, "TotalArea_x"] + DF.loc[:, "TotalArea_y"] + DF.loc[:, "TotalArea"]) /3
    # DF.loc[:, "MEAN_TotalArea_Ratio"] = (DF.loc[:, "TotalArea_Ratio_x"] + DF.loc[:, "TotalArea_Ratio_y"] + DF.loc[:, "TotalArea_Ratio"]) /3
    print(DF)
    DF.to_csv(os.path.join(ResPath, "DTarget.csv"), header=True, index=False)

    # get CTRL mean by plate
    # y = DF.query("GeneName == 'Non Trans' or GeneName == 'PLK1' or GeneName == 'Neg' or GeneName == 'DUX4+258' or GeneName == 'Neg1'")
    # y.groupby(by=['PlateName', 'GeneName']).mean().to_csv(os.path.join(ResPath, 'ANALYSE_CTRL_mean_ALT.csv'), index=True, header=True)


    ## NPI normalization

    # platelist = DF.loc[:, 'PlateName'].unique()
    # dfList = []
    # for plate in platelist:
    #     df1 = DF[DF.loc[:, 'PlateName'] == plate]
    #     for col in ['MEAN_TotalArea', 'TotalArea_x', 'TotalArea_y', 'TotalArea']:
    #         df1.loc[:, (col+'_NPI')] = ((np.mean(df1.query("GeneName == 'Neg'"))[col] - df1.loc[:, col]) / (np.mean(df1.query("GeneName == 'Neg'"))[col] - np.mean(df1.query("GeneName == 'Neg1'"))[col])) * 100
    #     dfList.append(df1)
    # x = pd.concat(dfList)
    # x.to_csv(os.path.join(ResPath, 'ANALYSE_NPI_A.csv'), index=False, header=True)
    #
    # dfList = []
    # for plate in platelist:
    #     df1 = DF[DF.loc[:, 'PlateName'] == plate]
    #     for col in ['MEAN_TotalArea', 'TotalArea_x', 'TotalArea_y', 'TotalArea']:
    #         df1.loc[:, (col+'_NPI')] = ((np.mean(df1.query("GeneName == 'Neg'"))[col] - df1.loc[:, col]) / (np.mean(df1.query("GeneName == 'Neg'"))[col] - np.mean(df1.query("GeneName == 'DUX4+258'"))[col])) * 100
    #     dfList.append(df1)
    # x = pd.concat(dfList)
    # x.to_csv(os.path.join(ResPath, 'ANALYSE_NPI_B.csv'), index=False, header=True)

# DUX4_4x()

def DUX4():
    channel = 'ObjectAvgIntenCh1'
    neg = 'Neg'
    pos = 'DUX4+258'
    DataPath = '/home/akopp/Documents/DUX4_siRNA/DATA_All_Cells/'
    PPPath = '/home/akopp/Documents/DUX4_siRNA/BANK/'
    ResPath = '/home/akopp/Documents/DUX4_siRNA/DATA_All_Cells/DTarget'
    RatioPath = '/home/akopp/Documents/DUX4_siRNA/DATA_All_Cells/DTarget_ratio'

    if not os.path.isdir(ResPath):
        os.makedirs(ResPath)

    if not os.path.isdir(RatioPath):
        os.makedirs(RatioPath)

    ListDF = []
    ListDF_ratio = []

    PlateList = []

    for i in range(8, 9, 1):
        plaque = TCA.Core.Plate(name='DTarget '+str(i),
                                platemap = os.path.join(PPPath, "PP_Drug_Target"+str(i)+'.csv'))
        for j in ['1', '2', '3']:
            file = os.path.join(DataPath, 'DTarget '+str(i)+'.'+str(j)+'.csv')
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name='rep'+str(j), fpath=file)

        plaque.platemap[(1, 22)] = "DUX4+258_"
        plaque.platemap[(2, 22)] = "Neg_"
        plaque.platemap[(3, 22)] = "DUX4+258_"
        plaque.platemap[(4, 22)] = "Neg_"
        plaque.platemap[(5, 22)] = "DUX4+258_"
        plaque.platemap[(6, 22)] = "Neg_"
        plaque.platemap[(7, 22)] = "DUX4+258_"
        plaque.platemap[(8, 22)] = "Neg_"
        plaque.platemap[(9, 22)] = "Neg1_"
        plaque.platemap[(10, 22)] = "Neg1_"
        plaque.platemap[(11, 22)] = "Neg1_"
        plaque.platemap[(12, 22)] = "Neg1_"
        plaque.platemap[(13, 22)] = "PLK1_"
        plaque.platemap[(14, 22)] = "Non Trans_"

        # print(TCA.getEventsCounts(plaque))
        # for key, value in plaque:
        #     print(key, value)

        # print(plaque.platemap)
        plaque.normalization_channels(channels=channel,
                                      log_t=False,
                                      method='PercentOfControl',
                                      neg=plaque.platemap.search_well(neg),
                                      pos=plaque.platemap.search_well(pos))
        plaque.agg_data_from_replica_channel(channel=channel)
        for key, value in plaque:
            print(value.array)
        print(plaque.array)
        plaque.apply_systematic_error_correction()
        for key, value in plaque:
            print(value.array_c)
        print(plaque.array_c)
        PlateList.append(plaque)


        # print(TCA.plate_quality_control(plaque, channel=channel, cneg=neg, cpos=pos, use_raw_data=True))

        # for key, value in plaque:
        #     print(value.array)
        # print(plaque['rep1'])
        # print(TCA.plate_quality_control(plate=plaque, channel=channel, cneg=neg, cpos=pos))
        # print(plaque.get_raw_data(well=["B10"], channel=channel))
        # print(plaque['rep1'].get_rawdata(well=['B10']))
        # print(plaque['rep1'].get_rawdata(well=['B10'], channel=channel))

        # print(TCA.plate_channel_analysis(plaque, neg=neg, pos=pos, channel=channel, threshold=85, percent=True, clean=True))

        # df = TCA.plate_channel_analysis(plaque)
        # print(df)

        # plaque['rep1'].array = df.values['CellsCount_rep1'].values.reshape((16, 24))
        # plaque['rep2'].array = df.values['CellsCount_rep2'].values.reshape((16, 24))
        # plaque['rep3'].array = df.values['CellsCount_rep3'].values.reshape((16, 24))

        # TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=False,
        #                              verbose=True)
        # TCA.plate_ssmd_score(plaque, neg_control=neg, paired=False, robust_version=True, sec_data=False,
        #                              variance="equal", verbose=True)
        # TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=False,
        #                              verbose=True)
        # TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=False, method='MM',
        #                              verbose=True)

        # for key, value in plaque.replica.items():
        #     value.rawdata.df["TotalIntenCh1"] = value.rawdata.df["ObjectAreaCh1"] * value.rawdata.df["ObjectAvgIntenCh1"]
        # TCA.plot_wells_distribution(plaque, wells=["D2", "E2", "F2", "G2"],
        #                             channel="TotalIntenCh1", pool=True, kind='hist')
        # TCA.plot_wells_distribution(plaque, wells=["H2", "J2", "L2", "N2"],
        #                             channel=channel, pool=True, kind='hist')

        # try:
        #     TCA.heatmap_p(df.values['CellsCount_rep1'].values.reshape(16, 24),
        #                     file_path=os.path.join(ResPath, plaque.name+'rep1'+'.pdf'))
        # except Exception as e:
        #     pass
        # try:
        #     TCA.heatmap_p(df.values['CellsCount_rep2'].values.reshape(16, 24),
        #                     file_path=os.path.join(ResPath, plaque.name+'rep2'+'.pdf'))
        # except Exception as e:
        #     pass
        # try:
        #     TCA.heatmap_p(df.values['CellsCount_rep3'].values.reshape(16, 24),
        #                     file_path=os.path.join(ResPath, plaque.name+'rep3'+'.pdf'))
        # except Exception as e:
        #     pass
        #
        # ListDF.append(copy.deepcopy(df.values))
        #
        # # ### RATIO
        #
        # for col in ['CellsCount', 'CellsCount_rep1', 'CellsCount_rep2', 'CellsCount_rep3']:
        #     try:
        #         df.values[col] = (df.values[col] / (np.mean(df.values[df.values["PlateMap"] == "Neg1"][col]))) * 100
        #     except Exception as e:
        #         pass
        #
        # ListDF_ratio.append(df.values)
        #
        # try:
        #     TCA.heatmap_p(df.values['CellsCount_rep1'].values.reshape(16, 24),
        #                     file_path=os.path.join(RatioPath, plaque.name+'rep1'+'.pdf'), fmt='.1f')
        # except Exception as e:
        #     pass
        # try:
        #     TCA.heatmap_p(df.values['CellsCount_rep2'].values.reshape(16, 24),
        #                     file_path=os.path.join(RatioPath, plaque.name+'rep2'+'.pdf'), fmt='.1f')
        # except Exception as e:
        #     pass
        # try:
        #     TCA.heatmap_p(df.values['CellsCount_rep3'].values.reshape(16, 24),
        #                     file_path=os.path.join(RatioPath, plaque.name+'rep3'+'.pdf'), fmt='.1f')
        # except Exception as e:
        #     pass
    # TCA.HeatMap(plaque, render="seaborn", fmt='.1f', title=plaque.name)
    # TCA.HeatMap(plaque, render="matplotlib", title=plaque.name)
    # TCA.Array3D(plaque)
    # TCA.Array3D(plaque, kind="surf")
    # TCA.Arrays3D(plaque, plaque['rep1'], plaque['rep2'], plaque['rep3'])
    # TCA.systematic_error(plaque)
    # TCA.wells_sorted(plaque, wells=['D2', "F15"], channel=channel)
    # TCA.boxplot_by_wells(plaque['rep1'], channel=channel)
    # TCA.well_count(plaque['rep1'])
    # TCA.HeatMapPlate(PlateList[0], sec_data=True, render="seaborn")
    # TCA.HeatMapPlates(PlateList, sec_data=True)
    # TCA.HeatMapPlates(PlateList, sec_data=True, render="seaborn")
    # TCA.plot_wells(PlateList)
    # print(TCA.Binning(PlateList[0], chan='ObjectAvgIntenCh1'))
    # print(PlateList[0].get_count())
    # merge all df
    # DF = pd.concat(ListDF)
    # DF.to_csv(os.path.join(ResPath, 'CellsCount.csv'), header=True, index=False)
    # DF_ratio = pd.concat(ListDF_ratio)
    # DF_ratio.to_csv(os.path.join(RatioPath, 'CellsCount.csv'), header=True, index=False)

DUX4()

def HDV():
    channel = 'AvgIntenCh2'
    neg = 'I'
    pos = 'Cyclosporine I'
    for j in range(1, 2, 1):
        # path = '/home/arnaud/Desktop/HDV/DATA'
        path = '/home/arnaud/Desktop/HDV prestwick/screen/'

        plaque = TCA.Core.Plate(name='HDV prestwick'+str(j),
                                platemap=TCA.Core.PlateMap(fpath=os.path.join(path, "PP_pl"+str(j)+".csv")))
        for i in ['1', '2', '3']:
            try:
                file = os.path.join(path, 'HDV prestwick pl'+str(j)+"."+str(i)+".csv")
                if os.path.isfile(file):
                    plaque + TCA.Core.Replica(name="rep" + i,
                                              fpath=file)
            except Exception as e:
                print(e)
                pass
        plaque.agg_data_from_replica_channel(channel=channel)
        TCA.plate_ssmd_score(plaque, neg_control=neg, paired=True, robust_version=True, sec_data=False, method='MM',
                                     verbose=True)
        TCA.plate_ttest(plaque, neg, verbose=True)
        # print(plaque.platemap)
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
        # TCA.plate_channel_analysis(plaque, channel=channel, neg=neg, pos=pos, threshold=88, clean=True, path=path, tag="12_%")
        # print(plaque.get_count())
        # TCA.plate_channel_analysis(plaque, channel=channel, neg=neg, pos=pos, threshold=600, percent=False, path=path,
                                #    clean=True, tag='_600', fixed_threshold=True)
        # plaque.agg_data_from_replica_channel(channel=channel)
        # for key, value in plaque.replica.items():
        #     print(value.array)
        # print(TCA.plate_quality_control(plaque, channel=channel, cneg=neg, cpos=pos, sedt=False, sec_data=False,
        #     use_raw_data=True, dirpath=None, skipping_wells=True))
        # TCA.wells_sorted(plaque, channel="AvgIntenCh2", wells=["A2", "B2", "C2", "D2"], ascending=False, y_lim=9000)
        # print(plaque.get_count())
        # TCA.heatmap_p(plaque.array, annot=True)
        # TCA.RepCor(plaque, channel)
        # TCA.plate_heatmap_p(plaque, both=False, size=6., file_path=os.path.join(path, plaque.name+'_'+channel+".pdf"))
        # TCA.systematic_error(plaque.array, file_path=None)
        # TCA.plot_wells(plaque, neg=neg, pos=pos, file_path=os.path.join(path, "Wells "+plaque.name+".pdf"))
        # print(plaque)
        del plaque

# HDV()

def misc2():
    path = '/home/akopp/Documents/Anne/data/'

    PlateList = []
    PlateList += [each for each in os.listdir(path) if each.endswith('.csv')]

    for name in PlateList:
        plaque = TCA.Core.Plate(name=name[0:-4],
                                platemap=TCA.Core.PlateMap(fpath="/home/akopp/Documents/Anne/PP.csv"))
        plaque + TCA.Core.Replica(name="rep1", fpath=os.path.join(path, name))

        for chan in ["SpotCountCh2", "SpotCountCh3", "SpotTotalAreaCh2", "SpotTotalAreaCh3", "SpotTotalIntenCh2",
                "SpotTotalIntenCh3", "TotalIntenCh2", "TotalIntenCh3"]:
                TCA.plate_channel_analysis(plaque, channel=chan, neg="NT", threshold=95, percent=True, path=path, clean=True)

# misc2()

def misc():
    path = '/home/arnaud/Desktop/TEMP/Amelie/XG_301015/'

    PlateList = []
    # 'MFGTMP-PC_12:33:47.csv'
    NameList = ['MFGTMP-PC_151029090001.csv']
    for plate in NameList:
        plaque = TCA.Core.Plate(name=plate[0:-4]+"_CTRL_A5_D6",
                                platemap=TCA.Core.PlateMap(),
                                replica=TCA.Core.Replica(name="rep1",
                                                         fpath=os.path.join(path, str(plate))))

        plaque.agg_data_from_replica_channel(channel='AvgIntenCh3')
        print(plaque.array)
        plaque.platemap['A5'] = "neg"
        plaque.platemap['B6'] = "neg"
        plaque.platemap['C5'] = "neg"
        plaque.platemap['D6'] = "neg"
        # plaque.platemap['G9'] = "neg"
        # plaque.platemap['G11'] = "neg"
        # plaque.platemap['H10'] = "neg"
        # plaque.platemap['H12'] = "neg"

        print(plaque.platemap.search_well('neg'))

        channel1 = ['AvgIntenCh3']
        a = TCA.plate_channels_analysis(plaque, neg="neg", channels=channel1, threshold=99.5, percent=True, clean=True, path=path)
        channel2 = ['AvgIntenCh4']
        b = TCA.plate_channels_analysis(plaque, neg="neg", channels=channel2, threshold=1, percent=True, clean=True, path=path)
        channel3 = ['AvgIntenCh5']
        c = TCA.plate_channels_analysis(plaque, neg="neg", channels=channel3, threshold=97, percent=True, clean=True, path=path)

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
        gb_data = plaqueCP['rep1'].rawdata.get_groupby_data()
        cnt = gb_data.Well.count().to_frame()
        cnt.columns = ['Count']
        cnt.to_csv(os.path.join(path, "CellCnt_GFP+Oct34-_"+plaque.name+'.csv'))

        plaqueCP = copy.deepcopy(plaque)
        TCA.channel_filtering(plaqueCP, channel=channel1[0], lower=int(a[channel1[0]][1]), include=True, percent=False)
        TCA.channel_filtering(plaqueCP, channel=channel3[0], lower=int(c[channel3[0]][1]), include=True, percent=False)
        gb_data = plaqueCP['rep1'].rawdata.get_groupby_data()
        cnt = gb_data.Well.count().to_frame()
        cnt.columns = ['Count']
        cnt.to_csv(os.path.join(path, "CellCnt_GFP+Zscan4+_"+plaque.name+'.csv'))

        plaqueCP = copy.deepcopy(plaque)
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

# misc()

# x =TCA.PlateMap(size=1536)
# print(x.platemap)
# x['B48'] = "CACA"
# print(x.platemap)

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

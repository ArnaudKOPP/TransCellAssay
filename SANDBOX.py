#!/usr/bin/env python3
# encoding: utf-8
"""
For testing module in actual dev
"""
import pandas as pd
import numpy as np
import os
import profile
import TransCellAssay as TCA
import logging
import copy
import sys
import matplotlib.pyplot as plt
import seaborn

logging.basicConfig(level=logging.INFO, format='[%(process)d/%(processName)s] @ [%(asctime)s] - %(levelname)-8s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

pd.set_option('display.max_rows',75)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 1000)
np.set_printoptions(linewidth=300)
np.set_printoptions(suppress=True, precision=4)



def AnaPAx7Prest():
    DataPath = '/home/akopp/Documents/AnagenesisPax7Prestwick/DATA_2Chan/'
    BankPath = '/home/akopp/Documents/AnagenesisPax7Prestwick/BANK/'
    RES = '/home/akopp/Documents/AnagenesisPax7Prestwick/ANALYSE_2Chan/'

    ListDF = []

    for i in range(1, 9, 1):
        plate = TCA.Core.Plate(name='Plate'+str(i),
                                platemap=os.path.join(BankPath, 'PP_pl'+str(i)+'.csv'))
        file = os.path.join(DataPath, '29102015 0'+str(i)+' Prestwick Pax7 5x.csv')
        if os.path.isfile(file):
            plate + TCA.Core.Replica(name='Rep1', fpath=file)

        for key, value in plate:
            value.df.loc[:, "TotalAreaPhalloidin"] = value.df.loc[:, "ValidObjectCount"] * value.df.loc[:, "MEAN_ObjectAreaCh1"]
            value.df.loc[:, "TotalAreaDesmin"] = value.df.loc[:, "ValidObjectCount"] * value.df.loc[:, "MEAN_SpotFiberTotalAreaCh3"]


        # plate.clear_memory()
        # plate.agg_data_from_replica_channel(channel=chan, forced_update=True)
        # TCA.HeatMapPlate(plate, fpath=os.path.join(RES, plate.name+str(chan)+"_Ratio.pdf"), render="seaborn", size=6.)

        # x = TCA.ScoringPlate(plate, channel=chan, neg='DMSO')
        # ListDF.append(x)
        # print(TCA.plate_quality_control(plate,channel="TotalArea", cneg="DMSO", cpos="SB203580"))

        for chan in ["TotalAreaPhalloidin", "TotalAreaDesmin"]:
            plate.normalization_channels(channels=chan, log_t=False, method='PercentOfControl',
                                        neg=plate.platemap.search_well('DMSO'))

        __SIZE__ = len(plate.platemap.platemap.values.flatten())
        gene = plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
        final_array = np.append(gene, plate.platemap._fill_empty(plate.platemap._generate_empty(384)).values.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, np.repeat([str(plate.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)
        x = pd.DataFrame(final_array)
        x.columns = ['PlateMap', 'Well', 'PlateName']

        # df = pd.merge(x, plate['Rep1'].df, on="Well")

        plate.agg_data_from_replica_channel(channel="TotalAreaPhalloidin", forced_update=True)
        x['TotalAreaPhalloidin'] = plate.array.flatten()

        # plate.clear_memory()
        plate.agg_data_from_replica_channel(channel="TotalAreaDesmin", forced_update=True)
        x['TotalAreaDesmin'] = plate.array.flatten()

        ListDF.append(x)

    DF = pd.concat(ListDF)
    # print(DF)
    # TCA.D2Plot(x=DF['TotalAreaDesmin'].values, y=DF['TotalAreaPhalloidin'].values, label_x="Desmin", label_y="Phalloidin")

    # DF.to_csv(os.path.join(RES, "TotalArea_Ratio.csv"), index=False, header=True)
    # DF.query("PlateMap == 'DMSO' or PlateMap == 'SB203580'").groupby(by=['PlateName', 'PlateMap']).mean().to_csv(os.path.join(RES, "TotalArea_CTRL_Ratio.csv"), index=True, header=True)
    x = DF.query("PlateMap == 'DMSO' or PlateMap == 'SB203580'").groupby(by=['PlateName', 'PlateMap']).mean()
    print(x)
    import matplotlib.pyplot as plt
    x.plot(kind='bar')

    plt.show()

# AnaPAx7Prest()

def DUX4_4x():

    DataPath = "/home/akopp/Documents/DUX4_siRNA/DATA_4x/"
    PPPath = '/home/akopp/Documents/DUX4_siRNA/BANK/'

    ListDF = list()

    for i in range(1, 2, 1):
        plaque = TCA.Core.Plate(name='Genome'+str(i),
                                platemap = os.path.join(PPPath, "PP_Genome"+str(i)+'.csv'))

        for j in ['1', '2', '3']:
            file = os.path.join(DataPath, 'Genome '+str(i)+'.'+str(j)+'.csv')
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name='rep'+str(j), fpath=file)

        # DF = pd.DataFrame(plaque.platemap.as_array())
        # __SIZE__ = len(plaque.platemap.platemap.values.flatten())
        # DF.loc[:, "PlateName"] = np.repeat([str(plaque.name)], __SIZE__).reshape(__SIZE__, 1)


        for key, value in plaque:
            value.df.loc[:, "TotalArea"] = value.df.loc[:, "ValidObjectCount"] * value.df.loc[:, "MEAN_ObjectAreaCh1"]

        plaque.normalization_channels(channels="TotalArea", log_t=False, method="PercentOfControl",
                                        neg=plaque.platemap.search_well('Neg'))

        # print(plaque['rep1'].get_rawdata(channel="TotalArea", well=plaque.platemap.search_well('Neg')))
        # print(plaque['rep2'].get_rawdata(channel="TotalArea", well=plaque.platemap.search_well('Neg')))
        # print(plaque['rep3'].get_rawdata(channel="TotalArea", well=plaque.platemap.search_well('Neg')))
        # print(np.mean(plaque['rep1'].get_rawdata(channel="TotalArea", well=plaque.platemap.search_well('Neg'))))
        # print(np.mean(plaque['rep2'].get_rawdata(channel="TotalArea", well=plaque.platemap.search_well('Neg'))))
        # print(np.mean(plaque['rep3'].get_rawdata(channel="TotalArea", well=plaque.platemap.search_well('Neg'))))

        # plaque.clear_memory()
        # for key, value in plaque:
        #     value.array = np.nan_to_num(value.array)
        plaque.agg_data_from_replica_channel(channel='TotalArea', forced_update=True)
        # plaque.array = np.nan_to_num(plaque.array)

        # print(TCA.plate_quality_control(plaque,channel="TotalArea", cneg="Neg", cpos="DUX4+258"))
        # x = plaque.get_raw_data(channel="TotalArea", well=plaque.platemap.search_well('Neg'), as_dict=True)
        # for key, value in x.items():
        #     print(key)
        #     print(value)

        #     print(np.mean(value.df.query("Well== 'H2' or Well == 'J2' or Well == 'L2' or Well == 'N2' or Well == 'C23' or Well == 'E23' or Well == 'G23' or Well == 'I23'")['TotalArea']))
        # TCA.HeatMap(plaque, render='matplotlib')
        # TCA.HeatMapPlate(plaque, render='matplotlib')
        # TCA.HeatMapPlates(plaque, plaque, render='matplotlib')
        # TCA.HeatMap(plaque)
        # TCA.HeatMapPlate(plaque)
        # TCA.HeatMapPlates(plaque, plaque)
        # TCA.Array3D(plaque)
        # TCA.Array3D(plaque, kind="surf")
        TCA.SystematicError(plaque)

        # x = TCA.ScoringPlate(plaque, channel='TotalArea', neg='Neg')
        # x = x.dropna(axis=0)
        # z = x.query("PlateMap == 'Non Trans' or PlateMap == 'PLK1' or PlateMap == 'Neg' or PlateMap == 'DUX4+258' or PlateMap == 'Neg1'").groupby(by=['PlateName', 'PlateMap']).mean()
        # print(z)
        # z.to_csv('/home/akopp/Desktop/test.csv', index=True, header=True)
        # ListDF.append(x)

        # for key, value in plaque:
        #     value.df = value.df.dropna(axis=0)
        #     useless = ['PlateNumber', 'Zposition', 'Status']
        #     for col in useless:
        #         try:
        #             value.df = value.df.drop([col], axis=1)
        #         except:
        #             pass
        #     DF = pd.merge(DF, value.df, on='Well', how='outer')

    # DF = pd.concat(ListDF)
    # print(DF.query("PlateMap != 'Non Trans' or PlateMap != 'PLK1' or PlateMap == 'Neg' or PlateMap != 'DUX4+258' or PlateMap != 'Neg1'").groupby(by=['PlateName', 'PlateMap']).mean())
    # DF.to_csv(os.path.join("/home/akopp/Documents/DUX4_siRNA/DATA_4x/18112015/18112015", "Genome.csv"), header=True, index=False)

# DUX4_4x()

def DUX4_Valid():
    path = "/home/akopp/Documents/DUX4_siRNA/Valid dux4/Analyse proto segmentation B"

    DF= []

    for i in range(1, 2, 1):
        plaque = TCA.Plate(name="DUX4 validation "+str(i), platemap=os.path.join("/home/akopp/Documents/DUX4_siRNA/Valid dux4/", "PP_"+str(i)+".csv"))

        for j in range(1, 4, 1):
            file = os.path.join(path, '150219 Valid dux4 '+str(i)+'.'+str(j)+'.csv')
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name='Rep'+str(j), fpath=file)

        df, thres = TCA.PlateChannelsAnalysis(plaque, channels=["ObjectAvgIntenCh1"], neg="Neg1", clean=True)
        print(df)
        # print(TCA.getEventsCounts(plaque))

        # cnt = TCA.getEventsCounts(plaque).loc[:, "Plate"]
        #
        # # ratio mean col
        # cnt.loc[:, "RatioNeg1"] = (cnt.loc[:, "CellsCount"] / np.mean(cnt.loc[cnt.loc[:, "PlateMap"] == "Neg1",: ].loc[:, "CellsCount"].values)) * 100
        # cnt.loc[:, "RatioNeg1NT"] = (cnt.loc[:, "CellsCount"] / np.mean(cnt.loc[cnt.loc[:, "PlateMap"] == "Neg1 NT",: ].loc[:, "CellsCount"].values)) * 100
        #
        # # ratio sur les replica
        #
        # for col in ["CellsCount_Rep1", "CellsCount_Rep2", "CellsCount_Rep3"]:
        #     cnt.loc[:, "RatioNeg1_"+str(col)] = (cnt.loc[:, col] / np.mean(cnt.loc[cnt.loc[:, "PlateMap"] == "Neg1",: ].loc[:, col].values)) * 100
        #
        # cnt.loc[:, "RatioNeg1_Std"] = cnt.iloc[:, -3:].std(axis=1)
        #
        #
        # x = cnt.iloc[:, -4:-1].apply(TCA.outlier_mad_based, axis=1)
        # X = cnt.iloc[:, -4:-1][x]
        #
        # y = cnt.iloc[:, -4:-1].apply(TCA.without_outlier_mad_based, axis=1)
        # Y = cnt.iloc[:, -4:-1][y]
        #
        # OUTLIERS1 = pd.concat([cnt.iloc[:, -4:-1], X, Y, Y.mean(axis=1), Y.std(axis=1)], axis=1)
        # print(OUTLIERS1)
        #
        #
        # for col in ["CellsCount_Rep1", "CellsCount_Rep2", "CellsCount_Rep3"]:
        #     cnt.loc[:, "RatioNeg1NT_"+str(col)] = (cnt.loc[:, col] / np.mean(cnt.loc[cnt.loc[:, "PlateMap"] == "Neg1 NT", :].loc[:, col].values)) * 100
        #
        # cnt.loc[:, "RatioNeg1NT_Std"] = cnt.iloc[:, -3:].std(axis=1)
        #
        #
        # x = cnt.iloc[:, -4:-1].apply(TCA.outlier_mad_based, axis=1)
        # X = cnt.iloc[:, -4:-1][x]
        #
        # y = cnt.iloc[:, -4:-1].apply(TCA.without_outlier_mad_based, axis=1)
        # Y = cnt.iloc[:, -4:-1][y]
        #
        # OUTLIERS2 = pd.concat([cnt.iloc[:, -4:-1], X, Y, Y.mean(axis=1), Y.std(axis=1)], axis=1)


    #     df = pd.concat([cnt, OUTLIERS1, OUTLIERS2], axis=1)
    #
    #     DF.append(df)
    #
    # x = pd.concat(DF)
    # x.query("PlateMap == 'Neg1' or PlateMap == 'Neg1 NT' or PlateMap == 'Non Trans' or PlateMap == 'DUX4+258' or PlateMap == 'DUX4+483' or PlateMap == 'PLK1'").groupby(["PlateName", "PlateMap"]).mean().to_csv(os.path.join(path, "CTRL_OUTLIERS.csv"), index=True, header=True)
    # x[x["PlateMap"].notnull()].to_csv(os.path.join(path, "CellsCount_OUTLIERS.csv"), index=False, header=True)

# DUX4_Valid()

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
        # plaque.normalization_channels(channels=channel,
        #                               log_t=False,
        #                               method='PercentOfControl',
        #                               neg=plaque.platemap.search_well(neg),
        #                               pos=plaque.platemap.search_well(pos))
        print(plaque.get_agg_data_from_replica_channels())
        print(TCA.Binning(plaque, chan=channel))
        # for key, value in plaque:
        #     print(value.array)
        # print(plaque.array)
        # plaque.apply_systematic_error_correction()
        # for key, value in plaque:
        #     print(value.array_c)
        # print(plaque.array_c)
        # PlateList.append(plaque)


        # print(TCA.plate_quality_control(plaque, channel=channel, cneg=neg, cpos=pos, use_raw_data=True))

        # for key, value in plaque:
        #     print(value.array)
        # print(plaque['rep1'])
        # print(TCA.plate_quality_control(plate=plaque, channel=channel, cneg=neg, cpos=pos))
        # print(plaque.get_raw_data(well=["B10"], channel=channel))
        # print(plaque['rep1'].get_rawdata(well=['B10']))
        # print(plaque['rep1'].get_rawdata(well=['B10'], channel=channel))

        # print(pd.DataFrame(plaque.platemap.as_array()))
        # print(pd.DataFrame(np.repeat([plaque.name], 384), columns=['PlateName']))
        # print(pd.concat([pd.DataFrame(np.repeat([plaque.name], 384), columns=['PlateName']), pd.DataFrame(plaque.platemap.as_array())], axis=1))
        # print(plaque.get_count())
        # df, ThresVal = TCA.plate_channel_analysis(plaque, neg=neg, pos=pos, channel=channel, threshold=85, percent=True, clean=True)
        # TCA.plot_wells_distribution(plaque, wells=["D2"], channel=channel, kind="hist")
        # TCA.channel_filtering(plaque, channel, ThresVal, thres="lower")
        # TCA.plot_wells_distribution(plaque, wells=["D2"], channel=channel, kind="kde")
        # print(plaque.get_count())
        # TCA.well_sorted(plaque['rep1'], well="D2", channel=channel)

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

# DUX4()

def HDVValidation():
    path = "/home/akopp/Documents/HDV validation2 SiRNA/"
    plaque = TCA.Plate(name="Eloi 20nM vs 40 nM", platemap=TCA.PlateMap(size=384))
    plaque + TCA.Replica(name='Rep1', fpath=os.path.join(path, "151202 20nM vs 40nM Eloi.csv"))

    plaque.platemap["C3"] = "Non Trans"
    plaque.platemap["C4"] = "Non Trans"
    plaque.platemap["C5"] = "Non Trans"
    plaque.platemap["D3"] = "Cell Death"
    plaque.platemap["D4"] = "Cell Death"
    plaque.platemap["D5"] = "Cell Death"
    plaque.platemap["E3"] = "Neg E"
    plaque.platemap["E4"] = "Neg E"
    plaque.platemap["E5"] = "Neg E"
    plaque.platemap["F3"] = "NTCP"
    plaque.platemap["F4"] = "NTCP"
    plaque.platemap["F5"] = "NTCP"
    plaque.platemap["G3"] = "Neg G"
    plaque.platemap["G4"] = "Neg G"
    plaque.platemap["G5"] = "Neg G"
    plaque.platemap["H3"] = "NTCP"
    plaque.platemap["H4"] = "NTCP"
    plaque.platemap["H5"] = "NTCP"
    plaque.platemap["I3"] = "Non Trans"
    plaque.platemap["I4"] = "Non Trans"
    plaque.platemap["I5"] = "Non Trans"
    plaque.platemap["J3"] = "Cell Death"
    plaque.platemap["J4"] = "Cell Death"
    plaque.platemap["J5"] = "Cell Death"
    plaque.platemap["K3"] = "Neg K"
    plaque.platemap["K4"] = "Neg K"
    plaque.platemap["K5"] = "Neg K"
    plaque.platemap["L3"] = "NTCP"
    plaque.platemap["L4"] = "NTCP"
    plaque.platemap["L5"] = "NTCP"
    plaque.platemap["M3"] = "Neg M"
    plaque.platemap["M4"] = "Neg M"
    plaque.platemap["M5"] = "Neg M"
    plaque.platemap["N3"] = "NTCP"
    plaque.platemap["N4"] = "NTCP"
    plaque.platemap["N5"] = "NTCP"

    channel = 'AvgIntenCh2'

    # df, thres = TCA.plate_channel_analysis(plaque, channel=channel, neg="Neg G", pos="NTCP", threshold=85, clean=True)
    # df.to_csv(os.path.join(path, plaque.name+"_"+chan+"_"+"Neg_G_15_%"+".csv"), index=False, header=True)
    #
    # df, thres = TCA.plate_channel_analysis(plaque, channel=channel, neg="Neg M", pos="NTCP", threshold=85, clean=True)
    # df.to_csv(os.path.join(path, plaque.name+"_"+chan+"_"+"Neg_M_15_%"+".csv"), index=False, header=True)

    x = TCA.getEventsCounts(plaque)
    print(x[x['CellsCount'] > 0 ])

# HDVValidation()

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
    path = '/home/akopp/Documents/Analyse Eloi/2_06_2016/'

    for File in ['160602 hdv 5.csv', '160602 HDV 7.csv']:

        Plaque = TCA.Plate(name=File[:-4],
                            platemap=TCA.Core.PlateMap(size=384))

        Plaque + TCA.Replica(name='rep1', fpath=os.path.join(path,File))

        for i in [100,200,300,4]:
            df, thres = TCA.PlateChannelsAnalysis(Plaque, channels="AvgIntenCh2",
                                                    threshold=i, percent=False,
                                                    fixed_threshold=True, clean=True)
            df.to_csv(os.path.join(path, "{0}_{1}.csv".format(Plaque.name, i)), header=True, index=False)

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

def Federica():
    Whole =      "/home/akopp/Documents/Anne/raw data tert"
    Peripheral = "/home/akopp/Documents/Anne/Raw datas Federica HeLa peripheral spot detector"

    DF = []

    for plt in ['Federica HeLa HU 8h.csv', 'Federica HeLa NCS 2h.csv', 'Federica HeLa NCS 8h.csv',
                'Federica HeLa NCS 16h.csv', 'Federica HeLa no drug.csv']:

        to_add = pd.read_csv(os.path.join(Whole, plt))
        final = pd.read_csv(os.path.join(Peripheral, plt))

        print(np.mean(final.query("Well == 'B11'")['SpotTotalIntenCh2']))

        for i in ["B11", "D11", "F11"]:
            final= final[final['Well'] != i]
            final = final.append(to_add[to_add['Well'] == i])

        print(np.mean(final.query("Well == 'B11'")['SpotTotalIntenCh2']))

        plaque = TCA.Core.Plate(name=plt[0:-4], platemap="/home/akopp/Documents/Anne/PP.csv")
        plaque + TCA.Core.Replica(name='Rep1', fpath=final)

        df, thres = TCA.PlateChannelsAnalysis(plaque, channels=['SpotTotalIntenCh2', 'SpotCountCh3'],
                                            neg='NT', threshold=95, clean=True)
        DF.append(df)

    x = pd.concat(DF)
    print(x)
    # x.to_csv('/home/akopp/Documents/Anne/FedericaDataNegExchange.csv', header=True, index=False)

# Federica()

def FedericaRatio():
    # import matplotlib.pyplot as plt
    # import seaborn as sns
    Whole = "/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/whole/"
    Peripheral = "/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/peripheral/"

    # plateNameList = [each for each in os.listdir(Whole) if each.endswith('.csv')]
    plateNameList = ['Federica HeLa NCS 2h.csv']

    for plateName in plateNameList:
        df1 = pd.read_csv(os.path.join(Peripheral, plateName))
        df2 = pd.read_csv(os.path.join(Whole, plateName))

        DF = pd.merge(df1, df2, on=['Well', 'X', 'Y'])
        print(len(DF))
        print(len(df1))
        print(len(df2))

        DF.loc[:, "Ratio_Ch2_SpotTotalInten"] = DF.loc[:, "SpotTotalIntenCh2_x"] / DF.loc[:, "SpotTotalIntenCh2_y"]
        DF.loc[:, "Ratio_Ch3_SpotCount"] = DF.loc[:, "SpotCountCh3_x"] / DF.loc[:, "SpotCountCh3_y"]
        # print(DF)
        DF.to_csv("/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/RatioData2h.csv", index=False, header=True)

        # DF = DF[DF['Ratio_Ch3_SpotCount'] > 0]
        # DF = DF[DF['Ratio_Ch2_SpotTotalInten'] > 0]
        # DF = DF[DF['Ratio_Ch3_SpotCount'] < 1]
        # DF = DF[DF['Ratio_Ch2_SpotTotalInten'] < 1]

        # x = DF.groupby(by=["Well", pd.cut(DF["Ratio_Ch3_SpotCount"], np.array([0,0.25,0.5,0.75,0.8,1]))]).count()["Ratio_Ch3_SpotCount"]
        # y = x.unstack()
        # y = y.iloc[:, :].apply(lambda a: a / y.sum(axis=1) * 100)
        # print(y)
        # y.to_csv('/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/PercentBytIntervalRatioCh3_'+plateName+'.csv', index=True, header=True)
        #
        # x = DF.groupby(by=["Well", pd.cut(DF["Ratio_Ch2_SpotTotalInten"], np.array([0,0.25,0.5,0.75,0.8,1]))]).count()["Ratio_Ch2_SpotTotalInten"]
        # y = x.unstack()
        # y = y.iloc[:, :].apply(lambda a: a / y.sum(axis=1) * 100)
        # print(y)
        # y.to_csv('/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/PercentBytIntervalRatioCh2_'+plateName+'.csv', index=True, header=True)

        # DF = DF.rename(columns = {'Well_x':'Well'})
        # plaque = TCA.Plate(name="Test", platemap=TCA.PlateMap(size=96))
        # plaque + TCA.Replica(name="Rep1", fpath=DF)
        # bins = TCA.Binning(plaque, chan="Ratio_Ch2_SpotTotalInten", bins=np.linspace(0, 1, 6))
        # print(bins['Rep1'])

        # DF.groupby(by='Well_x').mean().to_csv("/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/Ratio_Mean.csv", index=True, header=True)

        # for well in DF['Well_x'].unique():
        #     x = DF[DF['Well_x'] == str(well)].fillna(0)
        #     sns.distplot(x['Ratio_Ch3_SpotCount'].values, hist=True)
        #     plt.savefig("/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/Ratio_Graph/"+str(well)+"_Ratio_Ch3_SpotCount.pdf")
        #     plt.close()
        #     sns.distplot(x['Ratio_Ch2_SpotTotalInten'].values, hist=True)
        #     plt.savefig("/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/Ratio_Graph/"+str(well)+"_Ratio_Ch2_SpotTotalInten.pdf")
        #     plt.close()

# FedericaRatio()

def FedericaRatio2():

    whole = TCA.Core.Plate(name='Whole',
                            platemap=TCA.Core.PlateMap(fpath="/home/akopp/Documents/Anne/PP.csv"))
    whole + TCA.Core.Replica(name="rep1", fpath="/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/whole/Federica HeLa NCS 16h.csv")

    peripheral = TCA.Core.Plate(name='Peripheral',
                            platemap=TCA.Core.PlateMap(fpath="/home/akopp/Documents/Anne/PP.csv"))
    peripheral + TCA.Core.Replica(name="rep1", fpath="/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/peripheral/Federica HeLa NCS 16h.csv")

    thres = TCA.getThreshold(whole, ctrl="NT", channels=["SpotTotalIntenCh2", "SpotCountCh3"],
                                threshold=95, percent=True, fixed_threshold=False)
    print(thres)

    filteredWhole = TCA.channel_filtering(whole, channel="SpotTotalIntenCh2", value=thres['SpotTotalIntenCh2'],
                    thres='lower')

    DF = pd.merge(peripheral['rep1'].df, filteredWhole['rep1'].df, on=['Well', 'X', 'Y'])
    print(len(whole['rep1'].df))
    print(len(peripheral['rep1'].df))
    print(len(filteredWhole['rep1'].df))
    print(len(DF))

    ## _x est peripheral et _y est whole
    DF.to_csv("/home/akopp/Documents/Anne/FedericaRationWholePeri05022016/Merge.csv", index=False, header=True)

    DF.loc[:, "CenterCh2SpotTotalInten"] = DF.loc[:, "SpotTotalIntenCh2_y"] - DF.loc[:, "SpotTotalIntenCh2_x"]
    DF.loc[:, "CenterCh3SpotCount"] = DF.loc[:, "SpotCountCh3_y"] - DF.loc[:, "SpotCountCh3_x"]

    DF.loc[:, "Ch2SpotTotalIntenRatio"] = DF.loc[:, "SpotTotalIntenCh2_x"] / DF.loc[:, "CenterCh2SpotTotalInten"]
    DF.loc[:, "Ch3SpotCountRatio"] = DF.loc[:, "SpotCountCh3_x"] / DF.loc[:, "CenterCh3SpotCount"]
    print(DF)
    DF.to_csv("/home/akopp/Documents/Anne/FedericaRationWholePeri05022016/MergeWithRatio.csv", index=False, header=True)

# FedericaRatio2()

def XGScreen():
    path = "/home/akopp/Documents/XavierGaume/Screen/"
    BankPath = os.path.join(path, "Bank")
    DataPath = os.path.join(path, "Data")

    ResPath = os.path.join(path, 'Analyse13_04_2016')
    if not os.path.isdir(ResPath):
        os.makedirs(ResPath)


    DF1 = []
    DF2 = []
    DF3 = []
    DF4 = []
    DF5 = []

    for i in range(1, 2, 1):
        plaque = TCA.Plate(name="XavierGaume_"+str(i), platemap=os.path.join(BankPath, "PP_"+str(i)+".csv"))

        for j in range(1, 4, 1):
            file = os.path.join(DataPath, 'Screening Gaume '+str(i)+'.'+str(j)+'.csv')
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name='Rep'+str(j), fpath=file)

        plaque.platemap["A1"] = "Non Transfecté"
        plaque.platemap["B1"] = "Neg1"
        plaque.platemap["C1"] = "siP150"
        plaque.platemap["D1"] = "Neg1"
        plaque.platemap["E1"] = "siP150"
        plaque.platemap["F1"] = "Neg1"
        plaque.platemap["G1"] = "siP150"
        plaque.platemap["H1"] = "cell death"
        plaque.platemap["A12"] = "cell death"
        plaque.platemap["B12"] = "siP150"
        plaque.platemap["C12"] = "Neg1"
        plaque.platemap["D12"] = "siP150"
        plaque.platemap["E12"] = "Neg1"
        plaque.platemap["F12"] = "siP150"
        plaque.platemap["G12"] = "Neg1"
        plaque.platemap["H12"] = "NT sans ACLaire"

        # x = TCA.Binning(plaque, chan="SpotCountCh2", bins=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 51])
        # lst = []
        # somme = []
        # for key, value in x.items():
        #     somme.append(value.reset_index())
        #     value.columns = [key+col for col in value.columns]
        #     lst.append(value)
        # lst.append(pd.concat(somme).groupby(by="Well").mean())
        # df = pd.concat(lst, axis=1)
        # __SIZE__ = 96
        # df["Well"] = plaque.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
        # df["Plate"] = np.repeat([str(plaque.name)], __SIZE__).reshape(__SIZE__, 1)
        # DF.append(df)

        Threshold = {"AvgIntenCh3": 99.8, "AvgIntenCh4": 2, "AvgIntenCh5" : 98}
        channels=["AvgIntenCh3", "AvgIntenCh4", "AvgIntenCh5"]
        # channels=["AvgIntenCh3"]

        channelsChromo = ["SpotCountCh2", "SpotTotalAreaCh2", "SpotAvgAreaCh2", "SpotAvgIntenCh2"]

        df, thres = TCA.PlateChannelsAnalysis(plaque, neg="Neg1", channels=channels,
                                                threshold=Threshold, percent=True, clean=False, noposcell=False)
        print(df.head(20))
        # DF1.append(df)

        binsdata = TCA.Binning(plaque, chan="AvgIntenCh3")

        channel1 = 'AvgIntenCh3' # GFP
        channel2 = 'AvgIntenCh4' # Oct34
        channel3 = 'AvgIntenCh5' # Zscan4

        ### FILTERING PARTS
        # thres = TCA.getThreshold(plaque, ctrl="Neg1", channels=channels, threshold=Threshold, percent=True)
        # print(thres)


        # plaqueGFPpos = TCA.channel_filtering(plaque, channel=channel1, value=thres[channel1], exclude="lower", include=True, percent=False)
        # plaqueGFPneg = TCA.channel_filtering(plaque, channel=channel1, value=thres[channel1], exclude="upper", include=True, percent=False)
        # plaqueZscan4pos = TCA.channel_filtering(plaque, channel=channel3  , value=thres[channel3], exclude="lower", include=True, percent=False)
        # plaqueZscan4neg = TCA.channel_filtering(plaque, channel=channel3  , value=thres[channel3], exclude="upper", include=True, percent=False)

        # def SaveFilteredPlate(plate, tag, channel):
        #     DF = []
        #     for repname, rep in plate:
        #         DF.append(rep.df)
        #
        #     pd.concat(DF)[channel].to_csv(os.path.join("/home/akopp/Documents/XavierGaume/Screen/Analyse13_04_2016/FilteredRawData",
        #                                     plate.name+str(tag)+".csv"),
        #                                     header=True, index=False)

        # SaveFilteredPlate(plaqueGFPpos, tag="GFPpos", channel=channelsChromo)
        # SaveFilteredPlate(plaqueGFPneg, tag="GFPneg", channel=channelsChromo)
        # SaveFilteredPlate(plaqueZscan4pos, tag="Zscan4pos", channel=channelsChromo)
        # SaveFilteredPlate(plaqueZscan4neg, tag="Zscan4neg", channel=channelsChromo)

        # plaqueCP = TCA.channel_filtering(plaqueCP, channel=channel2, value=thres[channel2], thres="upper", include=True, percent=False)
        # df, thres = TCA.PlateChannelsAnalysis(plaqueCP, neg='Neg1', channels=["AvgIntenCh3", "AvgIntenCh4", "AvgIntenCh5"],
        #                                     threshold={"AvgIntenCh3": 99.8, "AvgIntenCh4": 2, "AvgIntenCh5" : 98},
        #                                     percent=True, clean=False)
        # DF2.append(df)



        # plaqueCP = TCA.channel_filtering(plaque, channel=channel1, value=thres[channel1], thres="lower", include=True, percent=False)
        # plaqueCP = TCA.channel_filtering(plaqueCP, channel=channel3, value=thres[channel3], thres="lower", include=True, percent=False)
        # df, thres = TCA.PlateChannelsAnalysis(plaqueCP, neg='Neg1', channels=["AvgIntenCh3", "AvgIntenCh4", "AvgIntenCh5"],
        #                                     threshold={"AvgIntenCh3": 99.8, "AvgIntenCh4": 2, "AvgIntenCh5" : 98},
        #                                     percent=True, clean=False)
        # DF3.append(df)


        # plaqueCP = TCA.channel_filtering(plaque, channel=channel2, value=thres[channel2], thres="upper", include=True, percent=False)
        # plaqueCP = TCA.channel_filtering(plaqueCP, channel=channel3, value=thres[channel3], thres="lower", include=True, percent=False)
        # df, thres = TCA.PlateChannelsAnalysis(plaqueCP, neg='Neg1', channels=["AvgIntenCh3", "AvgIntenCh4", "AvgIntenCh5"],
        #                                     threshold={"AvgIntenCh3": 99.8, "AvgIntenCh4": 2, "AvgIntenCh5" : 98},
        #                                     percent=True, clean=False)
        # DF4.append(df)


        # plaqueCP = TCA.channel_filtering(plaque, channel=channel1, value=thres[channel1], thres="lower", include=True, percent=False)
        # plaqueCP = TCA.channel_filtering(plaqueCP, channel=channel2, value=thres[channel2], thres="upper", include=True, percent=False)
        # plaqueCP = TCA.channel_filtering(plaqueCP, channel=channel3, value=thres[channel3], thres="lower", include=True, percent=False)
        # df, thres = TCA.PlateChannelsAnalysis(plaqueCP, neg='Neg1', channels=["AvgIntenCh3", "AvgIntenCh4", "AvgIntenCh5"],
        #                                     threshold={"AvgIntenCh3": 99.8, "AvgIntenCh4": 2, "AvgIntenCh5" : 98},
        #                                     percent=True, clean=False)
        # DF5.append(df)


    # pd.concat(DF1).to_csv(os.path.join(ResPath, 'GFPposChromo.csv'), index=False)
    # pd.concat(DF2).to_csv(os.path.join(ResPath, 'GFPnegChromo.csv'), index=False)
    # pd.concat(DF3).to_csv(os.path.join(ResPath, 'Zscan4posChromo.csv'), index=False)
    # pd.concat(DF4).to_csv(os.path.join(ResPath, 'ChannelsOct34-Zscan4+.csv'), index=False)
    # pd.concat(DF5).to_csv(os.path.join(ResPath, 'ChannelsGFP+Oct34-Zscan4+.csv'), index=False)

# XGScreen()

# XavierGaumeValidation()

def Anna():
    FPath = "/home/akopp/Documents/Anna2/"
    plaque = TCA.Core.Plate(name="151216 test Anna", platemap=TCA.PlateMap(size=96))
    plaque + TCA.Core.Replica(name="Rep1", fpath=os.path.join(FPath, "151216 test Anna.csv"))
    x = TCA.getEventsCounts(plaque)
    x.to_csv(os.path.join(FPath, "AllCount.csv"), index=False, header=True)
    # TCA.channel_filtering(plaque, channel='AvgIntenCh2', value={'Rep1' : 1000}, thres="lower")
    TCA.channel_filtering(plaque, channel='AvgIntenCh3', value={'Rep1' : 1000}, thres="lower")
    x = TCA.getEventsCounts(plaque)
    x.to_csv(os.path.join(FPath, "Ch3Filtering.csv"), index=False, header=True)

# Anna()

def Angelique():
    Path = "/home/akopp/Documents/Anne/Angélique réanalyse"

    for i in ["4h.csv"]:
        plaque = TCA.Core.Plate(name=i[0:-4], platemap=os.path.join(Path, i))
        plaque + TCA.Core.Replica(name="Rep1", fpath=os.path.join(Path, "151209 Angelique NSC tubulin.csv"))

        df, thres = TCA.PlateChannelsAnalysis(plaque, channels=['NeuriteTotalLengthCh2', 'NeuriteTotalCountCh2'],
                                            neg='Rien DMSO', pos='Rien DHT',
                                            threshold={'NeuriteTotalCountCh2':95, 'NeuriteTotalLengthCh2': 95})
        # df.to_csv(os.path.join(Path, "Analyse_"+i[0:-4]+".csv"), header=True, index=False)
        print(df)
        print(thres)
        plaque.agg_data_from_replica_channel(channel="NeuriteTotalLengthCh2")
        TCA.PlateWellsDistribution(plaque, wells=['A7', 'B7', 'G7'], channel="NeuriteTotalLengthCh2", kind='hist')

# Angelique()

def Zita():
    Path = "/home/akopp/Documents/Anne/Zita 160520 lacR/"
    # PlateListName = [each for each in os.listdir(Path) if each.endswith('.csv')]
    PlateListName = ['160523 Zita plaque1.csv', '160523 Zita plaque2.csv']


    DF = []

    for name in PlateListName:
        plaque = TCA.Core.Plate(name=name[0:-4],
                                platemap=TCA.Core.PlateMap(size=96))
        plaque + TCA.Core.Replica(name="rep1", fpath=os.path.join(Path, name))

        # plaque["rep1"].df = plaque["rep1"].df[plaque["rep1"].df["SpotTotalAreaCh2"] > 0]
        # df = TCA.PlateChannelsAnalysis(plaque, channels=["SpotTotalAreaCh2"], noposcell=False, multiIndexDF=True)
        # print(df)

        # filtered cell data with no spot
        FilteredPlate = TCA.channel_filtering(plaque, channel="SpotCountCh2", value={"rep1" : 0}, exclude="lower", include=False, percent=False)
        # FilteredPlate.platemap = plaque.platemap

        ## make ratio
        FilteredPlate['rep1'].df.loc[:, "Ratio_SpotTotalAreaCh2_ObjectAreaCh1"] = FilteredPlate['rep1'].df.loc[:, "SpotTotalAreaCh2"] / FilteredPlate['rep1'].df.loc[:, "ObjectAreaCh1"]

        ## Analyse ratio
        df, thres = TCA.PlateChannelsAnalysis(FilteredPlate, channels=["SpotTotalAreaCh2", "Ratio_SpotTotalAreaCh2_ObjectAreaCh1"], noposcell=False, multiIndexDF=True)
        DF.append(df)

        ## Writing FilteredPlate
        # FilteredPlate['rep1'].df.to_csv(os.path.join(Path, "{0}_FilteredCellsData.csv".format(FilteredPlate.name)), index=False, header=True)

    print(pd.concat(DF))
    # pd.concat(DF).to_csv(os.path.join(Path, "Analyse.csv"), index=False, header=True)

# Zita()

def EloiValidation():

    concentration = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
    concentrationVal = np.array([30, 10, 3, 1, 0.3, 0.1, 0.03, 0.01])
    concentrationDict = {"C1": 30, "C2": 10, "C3": 3, "C4":1, "C5":0.3, "C6":0.1, "C7":0.03, "C8":0.01}
    ChemList = ["Tracazolate hydrochloride","Methiazole",
            "Atorvastatin",	"Triflupromazine hydrochloride",
            "Sotalol hydrochloride", "Azathioprine",
            "Guaiacol",	"Ethaverine hydrochloride",
            "Alexidine dihydrochloride", "Betaxolol hydrochloride",
            "Nelfinavir mesylate", "Cladribine",
            "Cycloheximide", "Itraconazole",
            "Naftopidil dihydrochloride", "Nicardipine hydrochloride",
            "Clotrimazole",	"Nadide",
            "Atovaquone", "Diclazuril",
            "Chloroxine", "Etretinate",
            "Fluvoxamine maleate", "Oxibendazol",
            "Fulvestrant", "Albendazole",
            "Cyclosporin A", "Estramustine",
            "Fluvastatin sodium salt", "Artemisinin",
            "Propidium iodide",	"Oxfendazol",
            "Ribavirin", "Ketanserin tartrate hydrate",
            "Mercaptopurine", "Isoconazole",
            "Zardaverine", "Luteolin",
            "Miconazole", "Haloprogin",
            "Trioxsalen", "Nisoldipine",
            "Avermectin B1a", "Prazosin hydrochloride",
            "Beta-Escin", "Bepridil hydrochloride",
            "Chlorambucil",	"Amikacin hydrate",
            "Clioquinol", "Chenodiol",
            "Loperamide hydrochloride",	"Tioconazole",
            "Flubendazol", "Oxiconazole Nitrate",
            "Nifuroxazide",	"Prenylamine lactate",
            "Anethole-trithione", "Bacampicillin hydrochloride",
            "Hydralazine hydrochloride","Oxymetholone",
            "Buflomedil hydrochloride"
            ]

    Path = "/home/akopp/Documents/Eloi/01021989/"

    DF = []
    file = open(os.path.join("/home/akopp/Documents/Eloi/01021989/DoseResponseCurveTotal", 'DoseResponse.csv'), 'w')
    file.write("ChemicalElement, Bottom, HillCoef, EC50, Top \n")

    NEG = "DMSO CTRL"
    CHAN = "AvgIntenCh2"


    # file = open(os.path.join("/home/akopp/Documents/Eloi/01021989/", 'IntensitiesthresholdValues_TotalEloi12.txt'), 'w')
    for i in range(1, 3, 1):
        plaque = TCA.Plate(name="Valid Prestwick Eloi "+str(i),
                            platemap=TCA.Core.PlateMap(fpath=os.path.join(Path, "PP_Total_"+str(i)+".csv")))

        for j in range(1, 2, 1):
            FilePath = os.path.join(Path, "Valid Prestwick Eloi "+str(i)+"."+str(j)+".csv")
            if os.path.isfile(FilePath):
                plaque + TCA.Core.Replica(name='Rep'+str(j), fpath=FilePath)


        df, thres = TCA.PlateChannelsAnalysis(plaque, channels=[CHAN], neg=NEG,
                                                threshold=88, percent=True,
                                                fixed_threshold=False, clean=False)
        # file.write(str(plaque.name)+" : " + str(thres) + "\n")
        # DF.append(df)

        ## Dose Response part with % positive cells
        MEAN = df[CHAN, "PositiveCells"].reshape(plaque.platemap.shape())
        # STD = df[CHAN, "PositiveCells std"].reshape(plaque.platemap.shape())

        for chemElem in ChemList:
            try:
                mean = []
                std = []
                for conc in concentration:
                    pos = plaque.platemap.search_coord(chemElem+" "+conc)
                    mean.append(MEAN[pos[0][0]][pos[0][1]])
                    # std.append(STD[pos[0][0]][pos[0][1]])

                print("Work on : {0} @ {1}".format(chemElem, plaque.name))
                try:
                    dose = TCA.DoseResponseCurve(x_data=concentrationVal, y_data=np.array(mean))

                    file.write(str(chemElem)+","+str(','.join(['%.5f' % num for num in dose['Param']]))+"\n")

                    ## graphics of dose response
                    x = np.linspace(np.min(concentrationVal), np.max(concentrationVal), 500)
                    from TransCellAssay.Stat.ML.CurveFitting import _logistic4
                    y = _logistic4(x, *dose['Param'])
                    fig = plt.figure()
                    ax = fig.add_subplot(111)
                    # ax.errorbar(concentrationVal, np.array(mean), fmt='o', xerr=0, yerr=np.array(std),
                    #             label='Percent positive cells')
                    ax.errorbar(concentrationVal, np.array(mean), fmt='o', xerr=0, yerr=0,
                                label='Percent positive cells')
                    ax.plot(x, y, label='Dose Response curve')
                    ax.set_xscale('log')

                    plt.legend()
                    # plt.show()
                    plt.savefig(os.path.join("/home/akopp/Documents/Eloi/01021989/DoseResponseCurveTotal", str(chemElem)+".pdf"),
                                dpi=200)
                    plt.close()

                except RuntimeError:
                    print("DoseResponse Not found for {}".format(chemElem))
                    continue

            except KeyError:
                continue


    file.close()
    # x = pd.concat(DF)
    # print(x)
    # x.to_csv(os.path.join(Path, "CriblageTotalEloi_12.csv"), index=False, header=True)

# EloiValidation()

def EloiValidationPrestwick():
    path = "/home/akopp/Documents/HDV prestwick/V2 sans backgrnd removal/"

    DF = []
    Threshold = 2000
    # thresfile = open(os.path.join(path, 'ThresholdValue.txt'), 'a')

    for i in range(1,3,1):
        plaque = TCA.Plate(name="Valid Prestwick{}".format(i), platemap=os.path.join(path, "PP_{0}.csv".format(i)))

        for j in range(1, 3, 1):
            datafile = os.path.join(path, "160317 Valid Prestwick Eloi {0}.{1}.csv".format(i, j))
            if os.path.isfile(datafile):
                plaque + TCA.Core.Replica(name="Rep{}".format(j), fpath=datafile)


        df, thres = TCA.PlateChannelsAnalysis(plaque, channels=["AvgIntenCh2"], neg="DMSO CTRL",
                                                threshold=(Threshold),
                                                percent=False,
                                                fixed_threshold=True, clean=False)
        DF.append(df)
        # thresfile.write("{0} @ {1}%: {2}\n".format(plaque.name, Threshold, thres))

    pd.concat(DF).to_csv(os.path.join(path, "AnalyseValidPrestwick_{0}.csv".format(Threshold)), index=False, header=True)
    # thresfile.close

# EloiValidationPrestwick()

def Edwige():
    path = "/home/akopp/Documents/Anne/Edwige/09062016/Edwige FISH 07062016.csv"

    plate = TCA.Core.Plate(name='Edwige FISH', platemap=TCA.Core.PlateMap(size=96))
    plate + TCA.Core.Replica(name="rep1", fpath=os.path.join(path, "080316 Edwige FISH.csv"))
    before = TCA.getEventsCounts(plate)
    DF = []


    gbdata = plate['rep1'].get_groupby_data()

    for line in ['A', 'B', 'C', 'D', 'E', 'F']:
        ctrldata = gbdata.get_group(line+'2')
        median = ctrldata.loc[:,"SpotFiberCountCh3"].median()
        mad = TCA.mad2(ctrldata.loc[:,"SpotFiberCountCh3"].values)
        thresholdValue = (median+2*mad)

        for well in range(1, 13, 1):
            value = gbdata.get_group(line+str(well))

            mask = value.loc[:, "SpotFiberCountCh3"] > (median+2*mad)
            DF.append(value.loc[mask,:].copy())

    # for key, value in plate['rep1']:
    #     median = value.loc[:,"SpotFiberCountCh3"].median()
    #     mad = TCA.mad2(value.loc[:,"SpotFiberCountCh3"].values)
    #     mask = value.loc[:, "SpotFiberCountCh3"] > (median+2*mad)
    #     DF.append(value.loc[mask,:].copy())

    DF = pd.concat(DF)
    plate['rep1'].df = DF
    plate.clear_cache()
    after = TCA.getEventsCounts(plate)

    percent = after["Plate"].loc[:, "rep1 CellsCount"] / before["Plate"].loc[:, "rep1 CellsCount"] * 100

    final = before["Plate"].iloc[:, 0:3]
    final.loc[:, "Before CellsCount"] = before["Plate"].loc[:, "rep1 CellsCount"]
    final.loc[:, "After CellsCount"] = after["Plate"].loc[:, "rep1 CellsCount"]
    final.loc[:, "Percent positive CellsCount"] = percent

    print(final)
    final.to_csv(os.path.join(path, "PercentOverThreshold.csv"), index=False,header=True)
    # plate['rep1'].df.loc[:, "Ratio_SpotFiberCh3_ObjectCh1"] = plate['rep1'].df.loc[:, "SpotFiberCountCh3"] / plate['rep1'].df.loc[:, "ObjectAreaCh1"]

    # df, thres = TCA.PlateChannelsAnalysis(plate, channels=["SpotFiberCountCh3", "Ratio_SpotFiberCh3_ObjectCh1"], neg="B10", threshold=95, percent=True,
    #                                         fixed_threshold=False, clean=True)

    # df.to_csv(os.path.join(path, "Analyse.csv"), index=False, header=True)

# Edwige()

def EdwigeBinning():
    path = "/home/akopp/Documents/Anne/Edwige/13062016/"
    LstFile = ["Edwige FISH 07062016.csv"]

    for FILE in LstFile:
        plaque = TCA.Plate(name=FILE[0:-4], platemap=TCA.Core.PlateMap(size=96))
        plaque + TCA.Replica(name="rep1", fpath=os.path.join(path, FILE))

        for chan in ["SpotFiberCountCh3", "AvgIntenCh3"]:
            x = TCA.Binning(plaque, chan=chan, nbins=25, percent=False)
            x['rep1'].to_csv(os.path.join(path, "{0}_{1}_AutoBins.csv".format(plaque.name, chan)), header=True, index=True)

            x = TCA.Binning(plaque, chan=chan, bins=[0,20,40,60,80,100,150,200,300,400,500,600,700,800,900], percent=False)
            x['rep1'].to_csv(os.path.join(path, "{0}_{1}_CustomBins.csv".format(plaque.name, chan)), header=True, index=True)

# EdwigeBinning()

def EloiSiRNAVal():
    Path = "/home/akopp/Documents/Analyse siRNA Eloi/V1/"

    DF = []
    Threshold = 20

    thresfile = open(os.path.join(Path, 'ThresholdValueDown.txt'), 'a')

    for i in range(1,5,1):
        plaque = TCA.Plate(name="Valid Eloi siRNA pl"+str(i), platemap=os.path.join(Path, "PP_"+str(i)+".csv"))

        for j in range(1, 4, 1):
            file = os.path.join(Path, 'Valid siRNA HDV {0}.{1}.csv'.format(i, j))
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name='Rep'+str(j), fpath=file)

        plaque.platemap["L4"] = "Neg i out"
        plaque.platemap["L6"] = "Neg i out"
        plaque.platemap["L8"] = "Neg i out"
        plaque.platemap["L10"] = "Neg i out"
        plaque.platemap["L12"] = "Neg i out"
        plaque.platemap["L14"] = "Neg i out"
        plaque.platemap["L16"] = "Neg i out"
        plaque.platemap["L18"] = "Neg i out"
        plaque.platemap["L20"] = "Neg i out"

        # plaque.platemap["M5"] = "Neg i out"
        # plaque.platemap["M7"] = "Neg i out"
        # plaque.platemap["M9"] = "Neg i out"
        # plaque.platemap["M11"] = "Neg i out"
        # plaque.platemap["M13"] = "Neg i out"
        # plaque.platemap["M15"] = "Neg i out"
        # plaque.platemap["M17"] = "Neg i out"
        # plaque.platemap["M19"] = "Neg i out"
        # plaque.platemap["M21"] = "Neg i out"

        df, thres = TCA.PlateChannelsAnalysis(plaque, channels=["AvgIntenCh2"], neg="Neg i", clean=True,
                                                threshold=(100-Threshold),
                                                percent=True, fixed_threshold=False)
        thresfile.write("{0} @ {1}%: {2}\n".format(plaque.name, Threshold, thres))
        DF.append(df)

    pd.concat(DF).to_csv(os.path.join(Path, "Resultat_Down_{0}.csv".format(Threshold)), index=False, header=True)
    thresfile.close

# EloiSiRNAVal()

def Nelly():
    Path = "/home/akopp/Documents/Nelly/"
    fpathfile = ["160321 Gab analyse 6w.csv"]

    for plate in fpathfile:
        plaque = TCA.Core.Plate(name=plate[:-4],
                                platemap=TCA.Core.PlateMap(),
                                replica=TCA.Core.Replica(name="rep1",
                                                         fpath=os.path.join(Path, str(plate))))

        plaque.platemap['B2'] = "neg"
        plaque.platemap['A2'] = "pos"
        df, thres = TCA.PlateChannelsAnalysis(plaque, neg="neg", channels=["AvgIntenCh2"], threshold=400, percent=False,
                                            fixed_threshold=True, clean=True)

        df.to_csv(os.path.join(Path, "{0}_400_Result.csv".format(plaque.name)), index=False, header=True)

# Nelly()

def joanna():
    path = "/home/akopp/Documents/Joanna/Analyse sans background/"

    plate = TCA.Core.Plate(name="Joanna 4ch sans background", platemap=TCA.Core.PlateMap(size=96))
    plate + TCA.Core.Replica(name="rep1", fpath=os.path.join(path, "160412 Joanna 4 ch.csv"))

    df, thres = TCA.PlateChannelsAnalysis(plate, channels=["AvgIntenCh2", "AvgIntenCh3", "AvgIntenCh4"], clean=True,
                                            threshold={"AvgIntenCh2": 1000, "AvgIntenCh3": 1000, "AvgIntenCh4": 1000},
                                            percent=False, fixed_threshold=True)

    df.to_csv(os.path.join(path, "Analyse@1000.csv"), header=True, index=False)

    df, thres = TCA.PlateChannelsAnalysis(plate, channels=["AvgIntenCh2", "AvgIntenCh3", "AvgIntenCh4"], clean=True,
                                            threshold={"AvgIntenCh2": 500, "AvgIntenCh3": 500, "AvgIntenCh4": 500},
                                            percent=False, fixed_threshold=True)

    df.to_csv(os.path.join(path, "Analyse@500.csv"), header=True, index=False)

# joanna()

def EloiSiPoolValidation():
    Path = "/home/akopp/Documents/Analyse siRNA Eloi/20052016Background removed/"
    # thresfile = open(os.path.join(Path, 'ThresholdValue.txt'), 'a')

    plate = TCA.Plate(name="EloiSiRNA", platemap=os.path.join(Path, "PP.csv"))

    for i in range(1,4,1):
        RepFilePath = os.path.join(Path, "160518 Valid Eloi {0}.csv".format(i))
        if os.path.isfile(RepFilePath):
            plate + TCA.Core.Replica(name="Rep{}".format(i), fpath=RepFilePath)


    # TCA.PlateWellsSorted(plate, wells=plate.platemap.search_well('Neg i'), channel="AvgIntenCh2", rep="Rep1")
    # TCA.PlateWellsSorted(plate, wells=plate.platemap.search_well('Neg i'), channel="AvgIntenCh2", rep="Rep2")
    # TCA.PlateWellsSorted(plate, wells=plate.platemap.search_well('Neg i'), channel="AvgIntenCh2", rep="Rep3")
    for thres in [300,400,500,600]:
        df, ThresVal = TCA.PlateChannelsAnalysis(plate, channels=['AvgIntenCh2'],
                                                neg="Neg i", threshold=thres,
                                                percent=False, fixed_threshold=True, clean=True)
        # thresfile.write("{0} @ {1}%: {2}\n".format(plate.name, thres, ThresVal))
        df.to_csv(os.path.join(Path, "VEloiSiRNA@{0}.csv".format(thres)), index=False, header=True)
            # print(df)
            # plate.agg_data_from_replica_channel(channel="AvgIntenCh2")
            # print(TCA.plate_quality_control(plate, channel="AvgIntenCh2", cneg="Neg i", cpos="SiNTCP i", use_raw_data=False))

            # for key, value in plate:
            #     x = plate.get_count()[key+' CellsCount'].values.reshape((16,24))
            #     value.array = x
            #
            # TCA.HeatMapPlate(plate)


        # for thres in [12,15]:
        #     df, ThresVal = TCA.PlateChannelsAnalysis(plate, channels=['AvgIntenCh2'],
        #                                                 neg="Neg i", threshold=(100-thres),
        #                                                 percent=True, fixed_threshold=False, clean=True)
        #
        #     thresfile.write("{0} @ {1}%: {2}\n".format(plate.name, thres, ThresVal))
        #
        #     df.to_csv(os.path.join(Path, "ValidEloiSiPool@{0}nM@{1}%.csv".format(con, thres)), index=False, header=True)

    # thresfile.close()

# EloiSiPoolValidation()

def test():
    path = "/home/akopp/Documents/XavierGaume/Validation/"

    for i in range(6, 7, 1):
        plaque = TCA.Plate(name="XavierGaume_Validation_{}".format(i), platemap=TCA.Core.PlateMap(fpath=os.path.join(path, "PP_{0}.csv".format(i))))

        for j in range(1, 4, 1):
            file = os.path.join(path, 'Valid Gaume{0}.{1}.csv'.format(i, j))
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name='Rep'+str(j), fpath=file)

        # print(TCA.PlateChannelsAnalysis(plaque, channels="AvgIntenCh3", multiIndexDF=True))
        # TCA.PlateWellsSorted(plaque, wells=plaque.platemap.search_well('Neg1'), channel="AvgIntenCh3")
        # TCA.PlateWellsSorted(plaque, wells=plaque.platemap.search_well('siP150'), channel="AvgIntenCh3")
        #
        # TCA.PlateWellsSorted(plaque, wells=plaque.platemap.search_well('Neg1'), channel="AvgIntenCh4")
        # TCA.PlateWellsSorted(plaque, wells=plaque.platemap.search_well('siP150'), channel="AvgIntenCh4")
        #
        # TCA.PlateWellsSorted(plaque, wells=plaque.platemap.search_well('Neg1'), channel="AvgIntenCh5")
        # TCA.PlateWellsSorted(plaque, wells=plaque.platemap.search_well('siP150'), channel="AvgIntenCh5")


        # plaque.agg_data_from_replica_channel(channel="AvgIntenCh3")
        # plaque.use_count_as_data()
        #
        from TransCellAssay.Stat.Score.SSMD2 import plate_ssmdTEST
        print(plate_ssmdTEST(plaque, neg_control="Neg1", chan="AvgIntenCh3", outlier=True))

        from TransCellAssay.Stat.Score.TTest2 import plate_ttestTEST
        print(plate_ttestTEST(plaque, neg_control="Neg1", chan="AvgIntenCh3", outlier=True))

        from TransCellAssay.Stat.Score.TStat2 import plate_tstatTEST
        print(plate_tstatTEST(plaque, neg_control="Neg1", chan="AvgIntenCh3", outlier=True))

        from TransCellAssay.Stat.Score.ZScore import plate_zscoreTEST
        print(plate_zscoreTEST(plaque, neg_control="Neg1", chan="AvgIntenCh3", outlier=True))

# test()

def ElisaCriblage():
    path = "/home/akopp/Documents/Criblage ELISA Eric Champagne/"
    datapath = os.path.join(path, "Data")
    pppath = os.path.join(path, "PlateMap")

    lstPlt = []
    outlier=False
    norm=True

    for i in range(1,12,1):
        plaque = TCA.Plate(name="Elisa Eric Champagne Toul{}".format(i), platemap=os.path.join(pppath, "Toul{}.csv".format(i)))

        for j in range(1,4,1):
            if norm:
                InputFile = os.path.join(datapath, "NormToul{0}-{1}.csv".format(i, j))
            else:
                InputFile = os.path.join(datapath, "Toul{0}-{1}.csv".format(i, j))
            if os.path.isfile(InputFile):
                x = pd.read_csv(InputFile, header=None).values.reshape((8,12))
                plaque + TCA.Replica(name='Rep{}'.format(j), fpath=x, FlatFile=False)

        plaque._mean_array()
        tmp = []


        # from TransCellAssay.Stat.Score.SSMD2 import plate_ssmdTEST
        # ssmd = plate_ssmdTEST(plaque, neg_control="Neg3", outlier=outlier)
        # tmp.append(ssmd)
        #
        # from TransCellAssay.Stat.Score.TTest2 import plate_ttestTEST
        # ttest = plate_ttestTEST(plaque, neg_control="Neg3", outlier=outlier)
        # tmp.append(ttest.iloc[:, 8:])
        #
        # from TransCellAssay.Stat.Score.TStat2 import plate_tstatTEST
        # tstat = plate_tstatTEST(plaque, neg_control="Neg3", outlier=outlier)
        # tmp.append(tstat.iloc[:, 8:])
        #
        # from TransCellAssay.Stat.Score.ZScore import plate_zscoreTEST
        # zscore = plate_zscoreTEST(plaque, neg_control="Neg3", outlier=outlier)
        # tmp.append(zscore.iloc[:, 8:])

        from TransCellAssay.Stat.Score.KZscore import plate_kzscoreTEST
        zscore = plate_kzscoreTEST(plaque, outlier=outlier)
        tmp.append(zscore)

        df = pd.concat(tmp, axis=1)
        lstPlt.append(df)

    for i in range(1,3,1):
        plaque = TCA.Plate(name="Elisa Eric Champagne HMT{}".format(i), platemap=os.path.join(pppath, "HMT{}.csv".format(i)))

        for j in range(1,4,1):
            if norm:
                InputFile = os.path.join(datapath, "NormHMT{0}-{1}.csv".format(i, j))
            else:
                InputFile = os.path.join(datapath, "HMT{0}-{1}.csv".format(i, j))
            if os.path.isfile(InputFile):
                x = pd.read_csv(InputFile, header=None).values.reshape((8,12))
                plaque + TCA.Replica(name='Rep{}'.format(j), fpath=x, FlatFile=False)

        plaque._mean_array()
        tmp = []

        # from TransCellAssay.Stat.Score.SSMD2 import plate_ssmdTEST
        # ssmd = plate_ssmdTEST(plaque, neg_control="Neg3", outlier=outlier)
        # tmp.append(ssmd)
        #
        # from TransCellAssay.Stat.Score.TTest2 import plate_ttestTEST
        # ttest = plate_ttestTEST(plaque, neg_control="Neg3", outlier=outlier)
        # tmp.append(ttest.iloc[:, 8:])
        #
        # from TransCellAssay.Stat.Score.TStat2 import plate_tstatTEST
        # tstat = plate_tstatTEST(plaque, neg_control="Neg3", outlier=outlier)
        # tmp.append(tstat.iloc[:, 8:])
        #
        # from TransCellAssay.Stat.Score.ZScore import plate_zscoreTEST
        # zscore = plate_zscoreTEST(plaque, neg_control="Neg3", outlier=outlier)
        # tmp.append(zscore.iloc[:, 8:])

        from TransCellAssay.Stat.Score.KZscore import plate_kzscoreTEST
        zscore = plate_kzscoreTEST(plaque, outlier=outlier)
        tmp.append(zscore)

        df = pd.concat(tmp, axis=1)
        lstPlt.append(df)

    DF = pd.concat(lstPlt)

    DF2 = pd.read_csv("/home/akopp/Documents/Criblage ELISA Eric Champagne/CellsCntPreviousScreen.csv")
    DF = pd.merge(DF, DF2, on=['PlateMap', 'Well'], how='outer')
    DF.to_csv(os.path.join(path, "Elisa_BScoreNormr.csv"), index=False, header=True)

    # ctrl = DF.query("PlateMap == 'Neg3' or PlateMap == 'Neg3 NT' or PlateMap == '0' or PlateMap == '125' or PlateMap == '250' or PlateMap == '500' or PlateMap == '1000'")
    # ctrl.groupby(by=['PlateName', 'PlateMap']).mean().to_csv('/home/akopp/Documents/Criblage ELISA Eric Champagne/Elisa_BScoreNorm_CtrlMean.csv')
    # ctrl.groupby(by=['PlateName', 'PlateMap']).std().to_csv('/home/akopp/Documents/Criblage ELISA Eric Champagne/Elisa_BScoreNorm_CtrlStd.csv')

# ElisaCriblage()

def Sergey():
    path = "/home/akopp/Documents/sergey/6062016"

    for exp in ['160603 Sergey cherry.csv']:

        plaque = TCA.Plate(name=exp[:-4], platemap=TCA.Core.PlateMap(fpath=os.path.join(path, "PP.csv")))
        DF = []

        for j in range(1, 2, 1):
            plaque + TCA.Core.Replica(name='Rep'+str(j), fpath=os.path.join(path, exp))


        percent = 90
        channel = 'AvgIntenCh2'


        ## puits par 4
        # for i in range(1,10,1):
        #
        #     x = plaque['Rep1'].df.query("Well == 'A{0}' or Well == 'B{0}' or Well == 'C{0}' or Well == 'D{0}'".format(i))
        #     x.loc[:, "Well"] = "A{}".format(i)
        #     x = x[x[channel] >= np.percentile(x[channel], percent)]
        #     DF.append(x)
        #
        #     x = plaque['Rep1'].df.query("Well == 'E{0}' or Well == 'F{0}' or Well == 'G{0}' or Well == 'H{0}'".format(i))
        #     x.loc[:, "Well"] = "E{}".format(i)
        #     x = x[x[channel] >= np.percentile(x[channel], percent)]
        #     DF.append(x)

        ## puits par 2
        # for i in range(1,10,1):
        #
        #     x = plaque['Rep1'].df.query("Well == 'A{0}' or Well == 'B{0}'".format(i))
        #     x.loc[:, "Well"] = "A{}".format(i)
        #     x = x[x[channel] >= np.percentile(x[channel], percent)]
        #     DF.append(x)
        #
        #     x = plaque['Rep1'].df.query("Well == 'C{0}' or Well == 'D{0}'".format(i))
        #     x.loc[:, "Well"] = "C{}".format(i)
        #     x = x[x[channel] >= np.percentile(x[channel], percent)]
        #     DF.append(x)
        #
        #
        #     x = plaque['Rep1'].df.query("Well == 'E{0}' or Well == 'F{0}'".format(i))
        #     x.loc[:, "Well"] = "E{}".format(i)
        #     x = x[x[channel] >= np.percentile(x[channel], percent)]
        #     DF.append(x)
        #
        #     x = plaque['Rep1'].df.query("Well == 'G{0}' or Well == 'H{0}'".format(i))
        #     x.loc[:, "Well"] = "G{}".format(i)
        #     x = x[x[channel] >= np.percentile(x[channel], percent)]
        #     DF.append(x)

        for i in range(1,10,1):
            for well in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                x = plaque['Rep1'].df.query("Well == '{0}{1}'".format(well, i))
                x.loc[:, "Well"] = "{0}{1}".format(well, i)
                x = x[x[channel] >= np.percentile(x[channel], percent)]
                DF.append(x)


        plaque['Rep1'].df = pd.concat(DF)

        df = TCA.PlateChannelsAnalysis(plaque, channels=["AvgIntenCh2", "AvgIntenCh3"], noposcell=True)
        df.to_csv(os.path.join(path, '{0}_UpperValue_singleWells_{1}.csv'.format(plaque.name, percent)), index=False, header=True)

# Sergey()

def DUX4_2():
    Path = "/home/akopp/Documents/Dux4Juin2016/"
    PPath = os.path.join(Path, "BANK")
    DPath = os.path.join(Path, "Data")
    GPath = os.path.join(Path, "Graph")

    LST_Plaque = []
    DF = []
    QC = []

    removeBG = True
    ratioNeg1NT = False
    ratioNeg1 = True
    outlier = False
    ifQC = False

    ## Druggable subset
    for i in range(1,11,1):
        plaque = TCA.Plate(name="D- Subset - pl- {0}".format(i), platemap=os.path.join(PPath, "PP_Druggable_Subset{}.csv".format(i)))

        for j in range(1,4,1):
            InputFile = os.path.join(DPath, "D- Subset - pl- {0}-{1}.csv".format(i, j))
            if os.path.isfile(InputFile):
                x = pd.read_csv(InputFile, header=None).values
                if removeBG:
                    x = x - np.mean(x[0:2,0:2].flatten())
                if ratioNeg1NT:
                    x = x / np.mean(np.concatenate([x[9:13, 22],x[3:7, 1]])) * 100
                if ratioNeg1:
                    x = x / np.mean([x[7, 1], x[9, 1], x[11, 1], x[13, 1], x[2,22], x[4,22], x[6,22], x[8,22]]) * 100
                plaque + TCA.Replica(name='Rep{}'.format(j), fpath=x, FlatFile=False)
        plaque._mean_array()

        LST_Plaque.append(plaque)


        x = []

        from TransCellAssay.Stat.Score.SSMD2 import plate_ssmdTEST
        ssmd = plate_ssmdTEST(plaque, neg_control="Neg1", outlier=outlier)
        x.append(ssmd)

        from TransCellAssay.Stat.Score.TTest2 import plate_ttestTEST
        ttest = plate_ttestTEST(plaque, neg_control="Neg1", outlier=outlier)
        x.append(ttest.iloc[:, 8:])

        from TransCellAssay.Stat.Score.TStat2 import plate_tstatTEST
        tstat = plate_tstatTEST(plaque, neg_control="Neg1", outlier=outlier)
        x.append(tstat.iloc[:, 8:])

        from TransCellAssay.Stat.Score.ZScore import plate_zscoreTEST
        zscore = plate_zscoreTEST(plaque, neg_control="Neg1", outlier=outlier)
        x.append(zscore.iloc[:, 8:])

        from TransCellAssay.Stat.Score.KZscore import plate_kzscoreTEST
        kzscore = plate_kzscoreTEST(plaque, outlier=outlier)
        x.append(kzscore.iloc[:, 8:])

        DF.append(pd.concat(x, axis=1))


        if ifQC:
            qc = TCA.plate_quality_control(plaque, channel=None, use_raw_data=False, cneg="Neg1", cpos="DUX4+484")
            qc.loc[:, "PlateName"] = plaque.name
            QC.append(qc)


    ## Human Genome
    for i in range(1,21,1):
        plaque = TCA.Plate(name="H Genome - pl- {0}".format(i), platemap=os.path.join(PPath, "PP_Genome{}.csv".format(i)))

        for j in range(1,4,1):
            InputFile = os.path.join(DPath, "H Genome - pl- {0}-{1}.csv".format(i, j))
            if os.path.isfile(InputFile):
                x = pd.read_csv(InputFile, header=None).values
                if removeBG:
                    x = x - np.mean(x[0:2,0:2].flatten())
                if ratioNeg1NT:
                    x = x / np.mean(np.concatenate([x[9:13, 22],x[3:7, 1]])) * 100
                if ratioNeg1:
                    x = x / np.mean([x[7, 1], x[9, 1], x[11, 1], x[13, 1], x[2,22], x[4,22], x[6,22], x[8,22]]) * 100
                plaque + TCA.Replica(name='Rep{}'.format(j), fpath=x, FlatFile=False)
        plaque._mean_array()

        LST_Plaque.append(plaque)

        x = []

        from TransCellAssay.Stat.Score.SSMD2 import plate_ssmdTEST
        ssmd = plate_ssmdTEST(plaque, neg_control="Neg1", outlier=outlier)
        x.append(ssmd)

        from TransCellAssay.Stat.Score.TTest2 import plate_ttestTEST
        ttest = plate_ttestTEST(plaque, neg_control="Neg1", outlier=outlier)
        x.append(ttest.iloc[:, 8:])

        from TransCellAssay.Stat.Score.TStat2 import plate_tstatTEST
        tstat = plate_tstatTEST(plaque, neg_control="Neg1", outlier=outlier)
        x.append(tstat.iloc[:, 8:])

        from TransCellAssay.Stat.Score.ZScore import plate_zscoreTEST
        zscore = plate_zscoreTEST(plaque, neg_control="Neg1", outlier=outlier)
        x.append(zscore.iloc[:, 8:])

        from TransCellAssay.Stat.Score.KZscore import plate_kzscoreTEST
        kzscore = plate_kzscoreTEST(plaque, outlier=outlier)
        x.append(kzscore.iloc[:, 8:])

        DF.append(pd.concat(x, axis=1))

        if ifQC:
            qc = TCA.plate_quality_control(plaque, channel=None, use_raw_data=False, cneg="Neg1", cpos="DUX4+484")
            qc.loc[:, "PlateName"] = plaque.name
            QC.append(qc)

    if ifQC:
        QC = pd.concat(QC)
        QC.to_csv(os.path.join(Path, "QC_BGRemoved_RatioNeg1.csv"), header=True, index=False)

    df = pd.concat(DF)
    df = df[~df.PlateMap.isnull()]
    FileName = 'ANALYSIS_BGRemoved_RatioNeg1.csv'
    df.to_csv(os.path.join(Path, FileName), header=True, index=False)


DUX4_2()
#######################################################################################################################
#######################################################################################################################
#                           TEST                                                                                      #
#######################################################################################################################
#######################################################################################################################

# gb = df.groupby(by=)
#
# df.apply(lambda x: (x['AvgIntenCh3']['PositiveCells'] - df[df['Plate']['PlateName'] == x['Plate']['PlateName']]['AvgIntenCh3']['PositiveCells'].mean())
#  / df[df['Plate']['PlateName'] == x['Plate']['PlateName']]['AvgIntenCh3']['PositiveCells'].std())


## enlever des outliers
# df = pd.read_csv("/home/akopp/Documents/Analyse siRNA Eloi/V1/Resultat_15.csv", header=[0,1])
# y = df.iloc[:, 0:3]["Plate"]
# x = df.iloc[:, 31:34][df.iloc[:, 31:34].apply(without_outlier_mad_based, axis=1)]["AvgIntenCh2"]
# DF = pd.concat([y, x, x.mean(axis=1)], axis=1)
# DF.to_csv("/home/akopp/Documents/Analyse siRNA Eloi/V1/Resultat_15WithoutOutliers.csv", header=True, index=False)

# x =TCA.PlateMap(size=1536)
# print(x.platemap)
# x['B48'] = "CACA"
# print(x.platemap)

# x = TCA.DoseResponseCurve(func='4pl')
# import scipy.special
# 2 * (scipy.special.gamma(((3 + 6 - 2) / 2) / scipy.special.gamma((3 + 6 - 3) / 2))) ** 2
# import math
# (math.gamma(3/2)/ math.gamma(1))*np.sqrt(3/2)*(2.15/0.4025543)
# (gamma(3/2)/ gamma(1))*sqrt(3/2)*(2.15/0.4025543)

# pm = TCA.PlateMap(size=96)
# print(pm)
# pm2 = TCA.PlateMap(fpath='/home/arnaud/Desktop/PP_96.csv')
# print(pm2)
# print(pm['D6'])
# print(pm2['D6'])
# cProfile.run('[TCA.get_opposite_well_format("B12", bignum=True) for i in range(1000)]')
# cProfile.run('[TCA.get_opposite_well_format("B12") for i in range(1000)]')
# cProfile.run('[TCA.get_opposite_well_format((20,20), bignum=True) for i in range(1000)]')
# cProfile.run('[TCA.get_opposite_well_format((4,6)) for i in range(1000)]')


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

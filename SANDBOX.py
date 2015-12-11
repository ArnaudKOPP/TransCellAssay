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
pd.set_option('display.max_columns', 13)
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
        plaque.agg_data_from_replica_channel(channel=channel)
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
        TCA.well_sorted(plaque['rep1'], well="D2", channel=channel)

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
    path = '/home/akopp/Documents/Anne/Raw datas Federica HeLa peripheral spot detector/'

    PlateListName = [each for each in os.listdir(path) if each.endswith('.csv')]
    PlateList = []

    for name in PlateListName:
        plaque = TCA.Core.Plate(name=name[0:-4],
                                platemap=TCA.Core.PlateMap(fpath="/home/akopp/Documents/Anne/PP.csv"))
        plaque + TCA.Core.Replica(name="rep1", fpath=os.path.join(path, name))

        PlateList.append(plaque)

    for chan in ["SpotCountCh2","SpotTotalAreaCh2","SpotTotalIntenCh2","SpotCountCh3","SpotTotalAreaCh3","SpotTotalIntenCh3"]:
        DFList = []
        for plaque in PlateList:
            df , thres = TCA.plate_channel_analysis(plaque, channel=chan, neg="NT", threshold=95, percent=True, clean=True)
            DFList.append(df.values)

        df = pd.concat(DFList)
        df.groupby(by=["PlateName", "PlateMap"]).mean()["PositiveCells"].to_csv(os.path.join(path, chan+'_Mean.csv'), header=True, index=True)
        df.groupby(by=["PlateName", "PlateMap"]).std()["PositiveCells"].to_csv(os.path.join(path, chan+'_STD.csv'), header=True, index=True)

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

def FedericaRatio():
    import matplotlib.pyplot as plt
    # import seaborn as sns
    Whole = "/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/whole/"
    Peripheral = "/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/peripheral/"

    plateNameList = [each for each in os.listdir(Whole) if each.endswith('.csv')]
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
        # DF.to_csv("/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/RatioData.csv", index=False, header=True)

        # DF = DF[DF['Ratio_Ch3_SpotCount'] > 0]
        # DF = DF[DF['Ratio_Ch2_SpotTotalInten'] > 0]
        # DF = DF[DF['Ratio_Ch3_SpotCount'] < 1]
        # DF = DF[DF['Ratio_Ch2_SpotTotalInten'] < 1]

        # print(DF.head())
        x = DF.groupby(by=["Well", pd.cut(DF["Ratio_Ch3_SpotCount"], np.linspace(0, 1, 6))]).count()["Ratio_Ch3_SpotCount"]
        y = x.unstack()
        # print(y)
        y = y.iloc[:, :].apply(lambda a: a / y.sum(axis=1) * 100)
        print(y)
        y.to_csv('/home/akopp/Documents/Anne/RawData_Ratio_peripheral_Whole/PercentBytIntervalRatioCh3NCS2h.csv', index=True, header=True)

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

FedericaRatio()

def XGScreen():
    path = "/home/akopp/Documents/XavierGaume/"
    plateNameList = [each for each in os.listdir(path) if each.endswith('.csv')]

    DF1 = []
    DF2 = []
    DF3 = []
    CNT1 = []
    CNT2 = []
    CNT3 = []
    CNT4 = []
    for PltName in plateNameList:
        plaque = TCA.Plate(name=PltName[0:-4], platemap=TCA.PlateMap(size=96))
        plaque + TCA.Replica(name='rep1', fpath=os.path.join(path, PltName))

        plaque.platemap["B1"] = "Neg"
        plaque.platemap["D1"] = "Neg"
        plaque.platemap["F1"] = "Neg"
        plaque.platemap["C12"] = "Neg"
        plaque.platemap["E12"] = "Neg"
        plaque.platemap["G12"] = "Neg"

        ResPath = os.path.join(path, 'Analyse8')
        if not os.path.isdir(ResPath):
            os.makedirs(ResPath)

        channel1 = 'AvgIntenCh3'
        df1, thres1 = TCA.plate_channel_analysis(plaque, neg="Neg", channel=channel1, threshold=99.5, percent=True, clean=True)
        DF1.append(df1)

        channel2 = 'AvgIntenCh4'
        df2, thres2 = TCA.plate_channel_analysis(plaque, neg="Neg", channel=channel2, threshold=1, percent=True, clean=True)
        DF2.append(df2)

        channel3 = 'AvgIntenCh5'
        df3, thres3 = TCA.plate_channel_analysis(plaque, neg="Neg", channel=channel3, threshold=99, percent=True, clean=True,)
        DF3.append(df3)

        file = open(os.path.join(ResPath, str(plaque.name)+'_IntensitiesThresholdValues.txt'), 'w')
        file.write(str(channel1)+" : " + str(thres1) + "\n")
        file.write(str(channel2)+" : " + str(thres2) + "\n")
        file.write(str(channel3)+" : " + str(thres3) + "\n")
        file.close()

        plaque.clear_memory()

        plaqueCP = copy.deepcopy(plaque)
        plaqueCP.platemap = plaque.platemap
        TCA.channel_filtering(plaqueCP, channel=channel1, value=thres1, thres="lower", include=True, percent=False)
        TCA.channel_filtering(plaqueCP, channel=channel2, value=thres2, thres="upper", include=True, percent=False)
        cnt = TCA.getEventsCounts(plaqueCP)
        CNT1.append(cnt)

        plaqueCP = copy.deepcopy(plaque)
        plaqueCP.platemap = plaque.platemap
        TCA.channel_filtering(plaqueCP, channel=channel1, value=thres1, thres="lower", include=True, percent=False)
        TCA.channel_filtering(plaqueCP, channel=channel3, value=thres3, thres="lower", include=True, percent=False)
        cnt = TCA.getEventsCounts(plaqueCP)
        CNT2.append(cnt)

        plaqueCP = copy.deepcopy(plaque)
        plaqueCP.platemap = plaque.platemap
        TCA.channel_filtering(plaqueCP, channel=channel2, value=thres2, thres="upper", include=True, percent=False)
        TCA.channel_filtering(plaqueCP, channel=channel3, value=thres3, thres="lower", include=True, percent=False)
        cnt = TCA.getEventsCounts(plaqueCP)
        CNT3.append(cnt)

        plaqueCP = copy.deepcopy(plaque)
        plaqueCP.platemap = plaque.platemap
        TCA.channel_filtering(plaqueCP, channel=channel1, value=thres1, thres="lower", include=True, percent=False)
        TCA.channel_filtering(plaqueCP, channel=channel2, value=thres2, thres="upper", include=True, percent=False)
        TCA.channel_filtering(plaqueCP, channel=channel3, value=thres3, thres="lower", include=True, percent=False)
        cnt = TCA.getEventsCounts(plaqueCP)
        CNT4.append(cnt)


    pd.concat(DF1).to_csv(os.path.join(ResPath, 'AvgIntenCh3.csv'), index=False)
    pd.concat(DF2).to_csv(os.path.join(ResPath, 'AvgIntenCh4.csv'), index=False)
    pd.concat(DF3).to_csv(os.path.join(ResPath, 'AvgIntenCh5.csv'), index=False)
    pd.concat(CNT1).to_csv(os.path.join(ResPath, 'GFP+Oct34-.csv'), index=False)
    pd.concat(CNT2).to_csv(os.path.join(ResPath, 'GFP+Zscan4+.csv'), index=False)
    pd.concat(CNT3).to_csv(os.path.join(ResPath, 'Oct34-Zscan4+.csv'), index=False)
    pd.concat(CNT4).to_csv(os.path.join(ResPath, 'GFP+Oct34-Zscan4+.csv'), index=False)

# XGScreen()

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

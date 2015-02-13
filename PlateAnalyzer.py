#!/usr/bin/env python3
# encoding: utf-8
"""
UNIVERSAL ANALYSIS PIPELINE THAT USE TransCellAssay Toolbox
"""

import os
import time
import numpy as np
import TransCellAssay as TCA
import pandas as pd
import multiprocessing as mp

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def plate_analyzis(plateid):
    """
    Do the defined pipeline for plate with given plateid
    :param plateid:
    :return: 0 or 1
    """
    try:
        time_start = time.time()
        plaque = TCA.Core.Plate(name='Plate' + str(plateid))

        created = mp.Process()
        current = mp.current_process()
        print('created:', created.name, created._identity, 'running on :', current.name, current._identity,
              "for analyzis of ", plaque.name)

        print(__INPUT__, __OUTPUT__, __NBPLATE__, __NBREP__, __THRES__, __CHAN__, __NEG__, __POS__, __TOX__,
              __VERB__, __PROC__)

        output_data_plate_dir = os.path.join(__OUTPUT__, plaque.name)
        if not os.path.exists(output_data_plate_dir):
            os.makedirs(output_data_plate_dir)

        # Want to skip some Well, key is plateid and rep id and give use a list of well to skip
        to_skip = {(1, 1): ((3, 0), (4, 0), (5, 11)),
                   (1, 2): ((6, 11)),
                   (1, 3): (),
                   (2, 1): ((3, 0), (4, 11), (5, 11)),
                   (2, 2): (),
                   (2, 3): ((4, 11), (5, 11)),
                   (3, 1): ((2, 0), (3, 0), (4, 0), (5, 0)),
                   (3, 2): ((3, 0), (1, 11)),
                   (3, 3): (),
                   (4, 1): ((5, 0), (0, 11), (2, 11), (3, 11), (5, 11)),
                   (4, 2): ((1, 11)),
                   (4, 3): ((3, 0)),
                   (5, 1): ((3, 0)),
                   (5, 2): ((3, 0), (7, 0)),
                   (5, 3): ((2, 0), (3, 0), (2, 11)),
                   (6, 1): ((0, 11), (2, 11), (3, 11)),
                   (6, 2): ((3, 0), (5, 0)),
                   (6, 3): ((5, 0)),
                   (7, 1): ((3, 0), (4, 11), (5, 11)),
                   (7, 2): ((3, 0), (0, 11), (1, 11), (3, 11)),
                   (7, 3): ((5, 0)),
                   (8, 1): ((5, 0), (1, 11), (2, 11)),
                   (8, 2): ((0, 11), (1, 11), (2, 11), (5, 11)),
                   (8, 3): ((4, 0), (5, 0), (1, 11), (2, 11)),
                   (9, 1): ((0, 11)),
                   (9, 2): ((0, 11), (1, 11), (5, 0), (7, 0)),
                   (9, 3): ((0, 11), (2, 11), (4, 11)),
                   (10, 1): ((4, 0), (6, 0), (7, 0)),
                   (10, 2): ((6, 0), (0, 11), (1, 11), (3, 11)),
                   (10, 3): ((3, 0), (5, 0)),
                   (11, 1): ((7, 0), (0, 11), (1, 11), (3, 11)),
                   (11, 2): ((5, 0), (0, 11)),
                   (11, 3): ((5, 0), (7, 0), (1, 11), (4, 11), (5, 11))}

        # # CREATE PLATE OBJECT HERE
        plaque + TCA.Core.PlateMap(platemap=os.path.join(__INPUT__, "Pl" + str(plateid) + "PP.csv"))
        for i in range(1, __NBREP__ + 1):
            """
            data = pd.read_csv(os.path.join(__INPUT__, "toulouse pl " + str(plateid) + "." + str(i) + ".csv"))
            array = df_to_array(data, __CHANNEL__)
            # np.savetxt(fname=os.path.join(output_data_plate_dir, "rep" + str(i)) + ".csv", X=array, delimiter=",",
            # fmt='%1.4f')
            # plaque + TCA.Core.Replicat(name="rep" + str(i), data=array, single=False, skip=to_skip_HMT[(plateid, i)])
            plaque + TCA.Core.Replicat(name="rep" + str(i), data=array, single=False)
            """
            file = os.path.join(__INPUT__, "Pl" + str(plateid) + "rep_" + str(i) + ".csv")
            if os.path.isfile(file):
                plaque + TCA.Core.Replica(name="rep" + str(i), data=file, datatype='mean')
        # # BEGIN ANALYZIS HERE

        __SIZE__ = 96
        try:
            analyse = TCA.plate_analysis(plaque, __CHAN__, __NEG__, __POS__, threshold=__THRES__)
            analyse.write(os.path.join(output_data_plate_dir, "BasicsResults.csv"))
        except:
            pass

        # TCA.feature_scaling(plaque, __CHANNEL__, mean_scaling=True)
        plaque.normalization_channels(__CHAN__, method='Zscore', log=True, neg=plaque.platemap.search_well(__NEG__),
                                      pos=plaque.platemap.search_well(__POS__), skipping_wells=True)

        # for key, value in plaque.replicat.items():
        #     np.savetxt(fname=os.path.join(output_data_plate_dir, str(value.name)) + ".csv", X=value.Data, delimiter=",",
        #                fmt='%1.4f')

        try:
            TCA.plate_quality_control(plaque, channel=__CHAN__, cneg=__NEG__, cpos=__POS__, sedt=False, sec_data=False,
                                      skipping_wells=True, use_raw_data=False, verbose=False,
                                      dirpath=output_data_plate_dir)
        except:
            pass

        # plaque.check_data_consistency()

        plaque.systematic_error_correction(algorithm="MEA", apply_down=True, save=True, verbose=False, skip_col=[0, 11])

        # For multiple Replicat Workflow
        ssmd1 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=False, robust_version=True, sec_data=True,
                                     verbose=False)
        ssmd2 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=False, robust_version=True, sec_data=True,
                                     variance="equal", verbose=False)
        ssmd3 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=True, robust_version=True, sec_data=True,
                                     verbose=False)
        ssmd4 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=True, robust_version=True, sec_data=True,
                                     method='MM', verbose=False)
        tstat1 = TCA.plate_tstat_score(plaque, neg_control=__NEG__, paired=False, variance='equal', sec_data=True,
                                       verbose=False)
        tstat2 = TCA.plate_tstat_score(plaque, neg_control=__NEG__, paired=False, sec_data=True, verbose=False)
        tstat3 = TCA.plate_tstat_score(plaque, neg_control=__NEG__, paired=True, sec_data=True, verbose=False)

        gene = plaque.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
        final_array = np.append(gene, plaque.array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, plaque['rep1'].array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, plaque['rep2'].array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, plaque['rep3'].array.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ssmd1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ssmd2.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ssmd3.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, ssmd4.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, tstat1.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, tstat2.flatten().reshape(__SIZE__, 1), axis=1)
        final_array = np.append(final_array, tstat3.flatten().reshape(__SIZE__, 1), axis=1)

        to_save = pd.DataFrame(final_array)
        to_save.to_csv(os.path.join(output_data_plate_dir, "ssmd_tstat.csv"), index=False, header=False)
        #
        # rank = TCA.rank_product(plaque, secdata=True)
        # to_save = pd.DataFrame(rank)
        # to_save.to_csv(os.path.join(output_data_plate_dir, "rank_product.csv"), index=False, header=False)

        # # CLEAR PLATE OBJECT FOR MEMORY SAVING AND AVOID CRAPPY EFFECT
        plaque = None

        time_stop = time.time()
        print("\033[0;32m   ----> TOTAL TIME  {0:f}s for plate :\033[0m".format(float(time_stop - time_start)), plateid)
        return 1
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)
        return 0

__INPUT__ = "/home/arnaud/Desktop/ANTAGOMIR_MIMIC/antagomir"
__OUTPUT__ = "/home/arnaud/Desktop/ANTAGOMIR_MIMIC/TCA_MIMIC_ANTAGO/antagomir"
__NBPLATE__ = 26
__NBREP__ = 3
__THRES__ = 50
__CHAN__ = "Nuc Intensity"
__NEG__ = "NT"
__POS__ = "SINV C"
__TOX__ = None
__VERB__ = False
__PROC__ = 4

if __OUTPUT__ is None:
    __OUTPUT__ = os.path.join(__INPUT__, "Analyze/")
    if os.path.exists(__OUTPUT__):
        print('\033[0;33m[WARNING] !!!! PREVIOUS ANALYSIS WILL BE ERASE !!!!\033[0m')

if not os.path.exists(__OUTPUT__):
    os.makedirs(__OUTPUT__)

if __TOX__ is None:
    __TOX__ = __POS__


print(__INPUT__)

# # write txt file for saving parameters
file = open(os.path.join(__OUTPUT__, 'Analyse_Parameters.txt'), 'w')
file.write("INPUT : " + str(__INPUT__) + "\n")
file.write("OUTPUT : " + str(__OUTPUT__) + "\n")
file.write("NBPLATE : " + str(__NBPLATE__) + "\n")
file.write("NBREP : " + str(__NBREP__) + "\n")
file.write("CHANNEL : " + str(__CHAN__) + "\n")
file.write("THRESHOLD : " + str(__THRES__) + "\n")
file.write("NEG : " + str(__NEG__) + "\n")
file.write("POS : " + str(__POS__) + "\n")
file.write("TOX : " + str(__TOX__) + "\n")
file.close()


time_start = time.time()
# # Do process with multiprocessing
pool = mp.Pool(processes=__PROC__)
results = pool.map_async(plate_analyzis, range(1, __NBPLATE__ + 1))
print(results.get())
print("1 for sucess, 0 for fail")
time_stop = time.time()
print("\033[0;32mTOTAL EXECUTION TIME  {0:f}s \033[0m".format(float(time_stop - time_start)))
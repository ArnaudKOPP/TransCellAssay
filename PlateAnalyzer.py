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
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


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

        output_data_plate_dir = os.path.join(__OUTPUT__, plaque.name)
        if not os.path.exists(output_data_plate_dir):
            os.makedirs(output_data_plate_dir)

        # Want to skip some Well, key is plateid and rep id and give use a list of well to skip
        to_skip = {(1, 1): ((5, 11)),
                   (1, 2): ((5, 11)),
                   (2, 1): ((1, 11)),
                   (2, 2): ((1, 11)),
                   (2, 3): ((1, 11)),
                   (3, 1): ((1, 11), (2, 0)),
                   (3, 2): ((1, 11), (2, 0)),
                   (3, 3): ((1, 11), (2, 0))}

        # # CREATE PLATE OBJECT HERE
        plaque + TCA.Core.PlateMap(file_path=os.path.join(__INPUT__, "PL" + str(plateid) + "PP.csv"))
        for i in range(1, __NBREP__ + 1):
            file_path = os.path.join(__INPUT__, "PL" + str(plateid) + "." + str(i) + ".csv")
            if os.path.isfile(file_path):
                plaque + TCA.Replica(name="rep"+str(i), data_file_path=file_path, datatype='mean', skip=to_skip[(plateid, i)])

        # # BEGIN ANALYZIS HERE

        # plaque.normalization_channels(__CHAN__, method='PercentOfControl', log_t=False,
        #                               neg=plaque.platemap.search_well(__NEG__),
        #                               pos=plaque.platemap.search_well(__POS__),
        #                               skipping_wells=True)

        try:
            analyse = TCA.plate_channel_analysis(plaque, __CHAN__, __NEG__, __POS__, threshold=__THRES__, percent=True)
            # analyse.write(os.path.join(output_data_plate_dir, "BasicsResults.csv"))
        except Exception as e:
            logging.error(e)
            pass

        # # for key, value in plaque.replicat.items():
        # #     np.savetxt(fname=os.path.join(output_data_plate_dir, str(value.name)) + ".csv", X=value.Data, delimiter=",",
        # #                fmt='%1.4f')

        # try:
        #     # TCA.ReferenceDataWriter(plaque,
        #     #                         filepath=os.path.join(output_data_plate_dir, 'ControlValue.xlsx'),
        #     #                         ref=['Neg', 'F1 ATPase A', 'F1 ATPase B'],
        #     #                         channels=["ROI_A_Target_I_ObjectTotalInten", "ROI_B_Target_I_ObjectTotalInten"])
        #
        #     TCA.plate_quality_control(plaque, channel=__CHAN__, cneg=__NEG__, cpos=__POS__, sedt=False, sec_data=False,
        #                               skipping_wells=True, use_raw_data=False, verbose=False,
        #                               dirpath=output_data_plate_dir)
        # except:
        #     pass

        # plaque.systematic_error_correction(algorithm="MEA", apply_down=True, save=True, verbose=False, skip_col=[0, 11])

        # verbose = __VERB__
        # sec = False
        # robust = True
        # ssmd1 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=False, robust_version=robust, sec_data=sec,
        #                              verbose=verbose)
        # ssmd2 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=False, robust_version=robust, sec_data=sec,
        #                              variance="equal", verbose=verbose)
        # ssmd3 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=True, robust_version=robust, sec_data=sec,
        #                              verbose=verbose)
        # ssmd4 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=True, robust_version=robust, sec_data=sec,
        #                              method='MM', verbose=verbose)
        # tstat1 = TCA.plate_tstat_score(plaque, neg_control=__NEG__, paired=False, variance='equal', sec_data=sec,
        #                                verbose=verbose, robust=robust)
        # tstat2 = TCA.plate_tstat_score(plaque, neg_control=__NEG__, paired=False, sec_data=sec, verbose=verbose,
        #                                robust=robust)
        # tstat3 = TCA.plate_tstat_score(plaque, neg_control=__NEG__, paired=True, sec_data=sec, verbose=verbose,
        #                                robust=robust)
        #
        # ttest1, fdr1 = TCA.plate_ttest(plaque, __NEG__, verbose=verbose)
        # ttest2, fdr2 = TCA.plate_ttest(plaque, __NEG__, equal_var=True, verbose=verbose)
        #
        # __SIZE__ = len(plaque.platemap.platemap.values.flatten())
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
        # to_save.to_csv(os.path.join(output_data_plate_dir, "SCORING.csv"), index=False, header=False)

        # TCA.heatmap_map_p(plaque, usesec=False)
        # TCA.plot_wells(plaque)

        # # CLEAR PLATE OBJECT FOR MEMORY SAVING AND AVOID CRAPPY EFFECT
        plaque = None

        time_stop = time.time()
        print("\033[0;32m   ----> TOTAL TIME  {0:f}s for plate :\033[0m".format(float(time_stop - time_start)), plateid)
        return 1
    except Exception as e:
        logging.error(e)
        return 0

__INPUT__ = "/home/arnaud/Desktop/TOULOUSE/CONFIRMATION/RemovedData/"
__OUTPUT__ = "/home/arnaud/Desktop/TOULOUSE/CONFIRMATION/RemovedData/ROI_A/"
__NBPLATE__ = 3
__NBREP__ = 3
__THRES__ = 50
__CHAN__ = 'ROI_A_Target_I_ObjectTotalInten'
__NEG__ = 'Neg'
__POS__ = 'F1 ATPase A'
__TOX__ = None
__VERB__ = False
__PROC__ = 3

if __OUTPUT__ is None:
    __OUTPUT__ = os.path.join(__INPUT__, "Analyze/")
    if os.path.exists(__OUTPUT__):
        logging.warning('!!!! PREVIOUS ANALYSIS WILL BE ERASE !!!!')

if not os.path.exists(__OUTPUT__):
    os.makedirs(__OUTPUT__)

if __TOX__ is None:
    __TOX__ = __POS__

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
results = pool.map_async(plate_analyzis, range(1, 1+__NBPLATE__, 1))
print(results.get())
print("1 for success, 0 for fail")
time_stop = time.time()
print("\033[0;32mTOTAL EXECUTION TIME  {0:f}s \033[0m".format(float(time_stop - time_start)))
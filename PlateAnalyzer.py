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

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s',
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
        plaque + TCA.Core.PlateMap(fpath=os.path.join(__INPUT__, "PL" + str(plateid) + "PP.csv"))
        for i in range(1, __NBREP__ + 1):
            file_path = os.path.join(__INPUT__, "PL" + str(plateid) + "." + str(i) + ".csv")
            if os.path.isfile(file_path):
                plaque + TCA.Replica(name="rep"+str(i), fpath=file_path, datatype='mean', skip=to_skip[(plateid, i)])

        # # BEGIN ANALYZIS HERE

        # plaque.normalization_channels(__CHAN__, method='PercentOfControl', log_t=False,
        #                               neg=plaque.platemap.search_well(__NEG__),
        #                               pos=plaque.platemap.search_well(__POS__),
        #                               skipping_wells=True)

        analyse = TCA.plate_channel_analysis(plaque, __CHAN__, __NEG__, __POS__, threshold=__THRES__, percent=True)
        # analyse.write(os.path.join(output_data_plate_dir, "BasicsResults.csv"))

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

        # sec = False
        # robust = True
        # to_save = TCA.ScoringPlate(plaque, channel=__CHAN__, neg=__NEG__, robust=robust, data_c=sec, verbose=__VERB__)
        # to_save.to_csv(os.path.join(output_data_plate_dir, "SCORING.csv"), index=False, header=False)


        # # CLEAR PLATE OBJECT FOR MEMORY SAVING AND AVOID CRAPPY EFFECT
        del plaque

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
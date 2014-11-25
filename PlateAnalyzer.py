#!/usr/bin/env python3
# encoding: utf-8
"""
UNIVERSAL ANALYSIS PIPELINE THAT USE TransCellAssay Toolbox
"""

import os
import sys
import time
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import numpy as np
import TransCellAssay as TCA
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"
__date__ = '2014-09-28'
__updated__ = '2014-10-28'

DEBUG = 1


class CLIError(Exception):
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):  # IGNORE:C0111
    """Command line options."""
    time_start = time.time()

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = __import__('__main__').__doc__
    program_license = '''%s

  Created by Arnaud on %s. Updated on %s
  Copyright 2014 KOPP. All rights reserved.
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.
  VERSION = %s

USAGE
''' % (program_shortdesc, str(__date__), str(__updated__), str(__version__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-i", "--inputFileDirectory", dest="input", action="store",
                            help="Input path of data file ")
        # parser.add_argument("-o", "--outputFileDirectory", dest="output", action="store",
        # help="Output path for result file", required=True)
        #
        InArgs = parser.parse_args()
        InputFileDirectory = InArgs.input

        # # reading TEST
        time_norm_start = time.time()

        screen_test = TCA.Core.Screen()
        plaque1 = TCA.Core.Plate(name='Plate 1')
        platesetup = TCA.Core.PlateMap(platemap="/home/arnaud/Desktop/TEST/Pl1PP.csv")
        # plaque1.addPlateMap(platesetup)
        # # or
        plaque1 + platesetup
        rep1 = TCA.Core.Replicat(name="rep1", data="/home/arnaud/Desktop/TEST/Pl1rep_1.csv")
        rep2 = TCA.Core.Replicat(name="rep2", data="/home/arnaud/Desktop/TEST/Pl1rep_2.csv")
        rep3 = TCA.Core.Replicat(name="rep3", data="/home/arnaud/Desktop/TEST/Pl1rep_3.csv")

        # listing = list()
        # listing.append(rep1)
        # listing.append(rep2)
        # listing.append(rep3)
        # plaque1 + listing
        # # or
        plaque1 + rep1
        plaque1 + rep2
        plaque1 + rep3

        ## or
        # plaque1.addReplicat(rep1)
        #plaque1.addReplicat(rep2)
        #plaque1.addReplicat(rep3)
        screen_test.add_plate(plaque1)

        feature = "Nuc Intensity"
        neg = "Neg2"
        pos = "SINVc"

        time_norm_stop = time.time()
        print(
            "\033[0;32m ->Reading input data Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

        time_start_comp = time.time()
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        np.set_printoptions(linewidth=250)
        np.set_printoptions(suppress=True)
        """
        time_norm_start = time.time()
        TCA.plate_quality_control(plaque1, features=feature, cneg=neg, cpos=pos, sedt=False, sec_data=False,
                                  verbose=True)
        time_norm_stop = time.time()
        print("\033[0;32mQuality Control Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

        time_norm_start = time.time()
        analyse = TCA.compute_plate_analyzis(plaque1, [feature], neg, pos, threshold=50)
        print(analyse)
        time_norm_stop = time.time()
        print("\033[0;32mCompute Plate Analyzis Executed in {0:f}s\033[0m".format(
            float(time_norm_stop - time_norm_start)))

        time_norm_start = time.time()
        plaque1.normalization(feature, method='Zscore', log=True, neg=neg, pos=pos)
        time_norm_stop = time.time()
        print("\033[0;32mNormalization Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

        time_norm_start = time.time()
        plaque1.compute_data_from_replicat(feature)
        print(plaque1.Data)

        TCA.systematic_error_detection_test(plaque1.Data, alpha=0.05, verbose=True)
        TCA.systematic_error_detection_test(rep1.Data, alpha=0.05, verbose=True)
        TCA.systematic_error_detection_test(rep2.Data, alpha=0.05, verbose=True)
        TCA.systematic_error_detection_test(rep3.Data, alpha=0.05, verbose=True)

        plaque1.systematic_error_correction(method='median', apply_down=True, save=True, verbose=False)
        # plaque1.SystematicErrorCorrection(apply_down=False, save=True)  # apply only when replicat are not SE norm
        plaque1.compute_data_from_replicat(feature, use_sec_data=True)
        print(plaque1.SECData)
        TCA.systematic_error_detection_test(plaque1.SECData, alpha=0.05, verbose=True)
        time_norm_stop = time.time()
        print("\033[0;32mSEC Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

        print("\n \033[0;32m     SSMD TESTING \033[0m")
        time_norm_start = time.time()
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, sec_data=False, verbose=True)
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, robust_version=False, sec_data=False, verbose=True)
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, variance='equal', sec_data=False, verbose=True)
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=False, variance='equal', robust_version=False,
                             sec_data=True, verbose=True)
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, sec_data=True, verbose=True)
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, robust_version=False, sec_data=True, verbose=True)
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', sec_data=True, verbose=True)
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', robust_version=False,
                             sec_data=True, verbose=True)
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', sec_data=False, verbose=True,
                             inplate_data=True)
        TCA.plate_ssmd_score(plaque1, neg_control=neg, paired=True, method='UMVUE', robust_version=False,
                             sec_data=False, verbose=True, inplate_data=True)
        print("\033[0;32m    T-Stat TESTING \033[0m")
        TCA.plate_tstat_score(plaque1, neg_control=neg, paired=False, variance='equal', sec_data=True, verbose=True)
        TCA.plate_tstat_score(plaque1, neg_control=neg, paired=False, variance='equal', sec_data=False, verbose=True)
        TCA.plate_tstat_score(plaque1, neg_control=neg, paired=True, sec_data=True, verbose=True)
        test = TCA.plate_tstat_score(plaque1, neg_control=neg, paired=True, sec_data=False, verbose=True)

        gene = platesetup.platemap.values.flatten().reshape(96, 1)
        stat = np.append(gene, test.flatten().reshape(96, 1), axis=1)
        print(stat)

        time_norm_stop = time.time()
        print("\033[0;32mSSMD T-Stat Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

        # TCA.Graphics.plotDistribution('C5', plaque1, feature)
        # Graphics.boxplotByWell(rep1.Dataframe, feature)
        # Graphics.PlateHeatmap(rep1.Data)
        # Graphics.SystematicError(rep1.Data)
        # Graphics.plotSurf3D_Plate(rep1.Data)
        # Graphics.plotScreen(screen_test)
        # Graphics.plotSurf3D_Plate(A)
        """
        clustering = TCA.k_mean_clustering(plaque1)
        clustering.do_cluster()

        time_stop_comp = time.time()
        print("\033[0;32m ->Computation Executed in {0:f}s\033[0m".format(float(time_stop_comp - time_start_comp)))
    except KeyboardInterrupt:
        # ## handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG:
            raise e
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    time_stop = time.time()
    print("\033[0;32m   ----> TOTAL TIME (reading input + computation): {0:f}s\033[0m".format(
        float(time_stop - time_start)))


if __name__ == "__main__":
    main()
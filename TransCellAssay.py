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
import ScreenPlateReplicatPS
import Statistic
import numpy as np
import Statistic.Normalization
import Statistic.Score
import Statistic.Test
import Statistic.QC
from Utils import Graphics

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

        screen_test = ScreenPlateReplicatPS.Screen()
        plaque1 = ScreenPlateReplicatPS.Plate()
        plaque1.setName('Plate 1')
        platesetup = ScreenPlateReplicatPS.PlateSetup()
        platesetup.setPlateSetup("/home/akopp/Bureau/test/Pl1PP.csv")
        plaque1.addPlateSetup(platesetup)
        rep1 = ScreenPlateReplicatPS.Replicat()
        rep1.setName("rep1")
        rep1.setData("/home/akopp/Bureau/test/Pl1rep_1.csv")
        rep2 = ScreenPlateReplicatPS.Replicat()
        rep2.setName("rep2")
        rep2.setData("/home/akopp/Bureau/test/Pl1rep_2.csv")
        rep3 = ScreenPlateReplicatPS.Replicat()
        rep3.setName("rep3")
        rep3.setData("/home/akopp/Bureau/test/Pl1rep_3.csv")
        plaque1.addReplicat(rep1)
        plaque1.addReplicat(rep2)
        plaque1.addReplicat(rep3)
        screen_test.addPlate(plaque1)

        time_norm_stop = time.time()
        print("\033[0;32mReading input data Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

        # # Computation TEST
        # tmp2 = Statistic.computePlateAnalyzis(plaque1, ['Nuc Intensity'], 'NT')
        # print(tmp2)

        time_start_comp = time.time()
        np.set_printoptions(linewidth=200)
        np.set_printoptions(suppress=True)

        time_norm_start = time.time()
        # plaque1.Normalization('Nuc Intensity', technics='Zscore', log=True)
        time_norm_stop = time.time()
        print("\033[0;32mNormalization Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

        time_norm_start = time.time()
        plaque1.computeDataFromReplicat('Nuc Intensity')
        plaque1.SystematicErrorCorrection(method='average', apply_down=True, save=True, verbose=False)
        plaque1.SystematicErrorCorrection(apply_down=False, save=True)  # # apply only when replicat are not SE norm
        time_norm_stop = time.time()
        print("\033[0;32mSEC Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))

        subplate1 = ScreenPlateReplicatPS.SubPlate(plaque1)
        subplate1.setName("subplate1")
        print(subplate1['rep1'])
        print(subplate1.Name)
        print(platesetup.platesetup.iloc[1: 5, 3: 6])


        # Statistic.QC.PlateQualityControl(plaque1, features="Nuc Intensity", cneg="NT", cpos="SINV C", SEDT=False,
        # SECdata=False, verbose=True)
        #
        # print("\n \033[0;32m     SSMD TESTING \033[0m")
        # time_norm_start = time.time()
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=False, SECData=True, verbose=True)
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=False, robust_version=False, SECData=True, verbose=True)
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=False, variance='equal', SECData=True, verbose=True)
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=False, variance='equal', robust_version=False,
        #                            SECData=True, verbose=True)
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=True, SECData=False, verbose=True)
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=True, robust_version=False, SECData=False, verbose=True)
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=True, method='UMVUE', SECData=True, verbose=True)
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=True, method='UMVUE', robust_version=False, SECData=True,
        #                            verbose=True)
        #
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=True, method='UMVUE', SECData=True, verbose=True,
        #                            inplate_data=True)
        # Statistic.score.ssmd_score(plaque1, cNeg='NT', paired=True, method='UMVUE', robust_version=False, SECData=True,
        #                            verbose=True, inplate_data=True)
        #
        # print("\033[0;32m    T-Stat TESTING \033[0m")
        # Statistic.score.t_stat_score(plaque1, cNeg='NT', paired=False, variance='equal', SECData=False,
        #                              verbose=True)
        # Statistic.score.t_stat_score(plaque1, cNeg='NT', paired=False, variance='equal', SECData=False, verbose=True)
        # Statistic.score.t_stat_score(plaque1, cNeg='NT', paired=True, SECData=True, verbose=True)
        # Statistic.score.t_stat_score(plaque1, cNeg='NT', paired=True, SECData=True, verbose=True)
        # time_norm_stop = time.time()
        #
        # print("\033[0;32mSSMD T-Stat Executed in {0:f}s\033[0m".format(float(time_norm_stop - time_norm_start)))



        # Graphics.boxplotByWell(rep1.Data, "Nuc Intensity")
        # Graphics.PlateHeatmap(rep1.DataMean)
        # Graphics.SystematicError(rep1.DataMean)
        # Graphics.plotSurf3D_Plate(rep1.DataMean)
        # Graphics.plotScreen(screen_test)
        # rep1.SystematicErrorCorrection(Methods='MEA', verbose=True)
        # Statistic.Test.SystematicErrorDetectionTest(rep1.Data, alpha=0.05, verbose=True)
        # Statistic.Test.SystematicErrorDetectionTest(rep1.Data, alpha=0.05, verbose=True)
        # Statistic.Test.SystematicErrorDetectionTest(plaque1.Data, alpha=0.05, verbose=True)
        # rep1.SpatialNormalization(Methods='DiffusionModel', verbose=True)
        # Graphics.plotSurf3D_Plate(A)
        # Array = np.genfromtxt("/home/akopp/Bureau/testcsv.csv", delimiter=',')
        # Statistic.Test.SystematicErrorDetectionTest(Array, alpha=0.05, verbose=True)
        # Statistic.Normalization.MatrixErrorAmendment(Array.copy(), verbose=True, alpha=0.05)
        # Statistic.Normalization.PartialMeanPolish(Array.copy(), verbose=True, alpha=0.05)

        time_stop_comp = time.time()
        print("\033[0;32mComputation Executed in {0:f}s\033[0m".format(float(time_stop_comp - time_start_comp)))
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
    print("\033[0;32m   ----> Script total time : {0:f}s\033[0m".format(float(time_stop - time_start)))


if __name__ == "__main__":
    main()
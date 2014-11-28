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
import multiprocessing as mp

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

DEBUG = 1


class CLIError(Exception):
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    """Command line options."""
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = __import__('__main__').__doc__
    program_license = """%s

      Copyright 2014 KOPP. All rights reserved.
      Distributed on an "AS IS" basis without warranties
      or conditions of any kind, either express or implied.
      VERSION = %s

    USAGE
    """ % (program_shortdesc, str(__version__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-i", "--inputdir", dest="input", action="store", required=True,
                            help="Input path of data file")
        parser.add_argument("-o", "--outputdir", dest="output", action="store",
                            help="Output path for result file")
        parser.add_argument("-a", "--nbplate", dest="nbplate", type=int, action="store", required=True,
                            help="Number of Plate")
        parser.add_argument("-r", "--nbrep", dest="nbrep", default=3, type=int, action="store", required=True,
                            help="Number of replicat per plate (default: %(default)s)")
        parser.add_argument("-f", "--feat", dest="feat", action="store", type=str, required=True,
                            help="Feature to analyze in simple mode")
        parser.add_argument("-s", "--thres", dest="thres", default=50, type=int, action="store",
                            help="Threshold for determining positive cells (default: %(default)s)")
        parser.add_argument("-n", "--neg", dest="neg", action="store", type=str, required=True,
                            help="Negative Control")
        parser.add_argument("-p", "--pos", dest="pos", action="store", type=str, required=True,
                            help="Positive Control")
        parser.add_argument("-t", "--tox", dest="tox", action="store", type=str,
                            help="Toxic Control")
        parser.add_argument("-v", "--verbose", dest="verbose", default=False, type=bool, action="store",
                            help="Print pipeline (default: %(default)s)")
        parser.add_argument("-j", "--process", dest="process", default=mp.cpu_count(), action="store", type=int,
                            help="Number of process to use (default: %(default)s)")

        input_args = parser.parse_args()
        global __INPUT__, __OUTPUT__, __NBPLATE__, __NBREP__, __FEATURE__, __NEG__, __POS__, __TOX__, __VERBOSE__, __PROCESS__
        __INPUT__ = input_args.input
        __NBPLATE__ = input_args.nbplate
        __NBREP__ = input_args.nbrep
        __FEATURE__ = input_args.feat
        __NEG__ = input_args.neg
        __POS__ = input_args.pos
        __VERBOSE__ = input_args.verbose
        __PROCESS__ = input_args.process

        if input_args.output is None:
            __OUTPUT__ = os.path.join(__INPUT__, "Analyze/")
        else:
            __OUTPUT__ = input_args.output

        if not os.path.exists(__OUTPUT__):
            os.makedirs(__OUTPUT__)

        if input_args.tox is None:
            __TOX__ = __POS__
        else:
            __TOX__ = input_args.tox

        print(__INPUT__)

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


def simple_plate_analyzis(plateid):
    try:
        time_start = time.time()
        plaque = TCA.Core.Plate(name='Plate' + str(plateid))

        created = mp.Process()
        current = mp.current_process()
        print('created:', created.name, created._identity, 'running on :', current.name, current._identity,
              "for analyzis of ", plaque.Name)

        print(__INPUT__, __OUTPUT__, __NBPLATE__, __NBREP__, __FEATURE__, __NEG__, __POS__, __TOX__, __VERBOSE__,
              __PROCESS__)

        output_data_plate_dir = os.path.join(__OUTPUT__, plaque.Name)
        print(output_data_plate_dir)
        if not os.path.exists(output_data_plate_dir):
            os.makedirs(output_data_plate_dir)

        # # CREATE PLATE OBJECT HERE
        plaque + TCA.Core.PlateMap(platemap=os.path.join(__INPUT__, "Pl" + str(plateid) + "PP.csv"))
        for i in range(1, __NBREP__ + 1):
            plaque + TCA.Core.Replicat(name="rep" + str(i),
                                       data=os.path.join(__INPUT__, "Pl" + str(plateid) + "rep_" + str(i) + ".csv"))
        # # BEGIN ANALYZIS HERE
        TCA.plate_quality_control(plaque, features=__FEATURE__, cneg=__NEG__, cpos=__POS__, sedt=False,
                                  sec_data=False, verbose=False, dirpath=output_data_plate_dir)
        analyse = TCA.compute_plate_analyzis(plaque, [__FEATURE__], __NEG__, __POS__, threshold=50)
        analyse.write_csv(os.path.join(output_data_plate_dir, "BasicsResults.csv"))
        plaque.normalization(__FEATURE__, method='Zscore', log=True, neg=__NEG__, pos=__POS__)
        plaque.compute_data_from_replicat(__FEATURE__)
        plaque.systematic_error_correction(method='median', apply_down=True, save=True, verbose=False)
        plaque.compute_data_from_replicat(__FEATURE__, use_sec_data=True)
        ssmd1 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=False, robust_version=True, sec_data=True,
                                     verbose=False)
        ssmd2 = TCA.plate_ssmd_score(plaque, neg_control=__NEG__, paired=False, method='UMVUE', robust_version=True,
                                     sec_data=True, verbose=False)
        tstat1 = TCA.plate_tstat_score(plaque, neg_control=__NEG__, paired=False, variance='equal', sec_data=True,
                                       verbose=False)
        tstat2 = TCA.plate_tstat_score(plaque, neg_control=__NEG__, paired=True, sec_data=False, verbose=False)

        gene = plaque.PlateMap.platemap.values.flatten().reshape(96, 1)
        stat = np.append(gene, ssmd1.flatten().reshape(96, 1), axis=1)
        stat = np.append(stat, ssmd2.flatten().reshape(96, 1), axis=1)
        stat = np.append(stat, tstat1.flatten().reshape(96, 1), axis=1)
        stat = np.append(stat, tstat2.flatten().reshape(96, 1), axis=1)
        to_save = pd.DataFrame(stat)
        to_save.to_csv(os.path.join(output_data_plate_dir, "ssmd_tstat.csv"))

        # # CLEAR PLATE OBJECT FOR MEMORY SAVING AND AVOID CRAPPY EFFECT
        plaque = None

        time_stop = time.time()
        print("\033[0;32m   ----> TOTAL TIME  {0:f}s for plate :\033[0m".format(float(time_stop - time_start)), plateid)
        return 1
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)
        return 0


if __name__ == "__main__":
    main()

    # # Do process with multiprocessing
    pool = mp.Pool(processes=__PROCESS__)
    results = pool.map_async(simple_plate_analyzis, range(1, __NBPLATE__ + 1))
    print(results.get())
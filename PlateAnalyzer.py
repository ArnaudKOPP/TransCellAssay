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
        parser.add_argument("-i", "--inputdir", dest="input", action="store",
                            help="Input path of data file", required=True)
        parser.add_argument("-o", "--outputdir", dest="output", action="store",
                            help="Output path for result file")
        parser.add_argument("-a", "--nbplate", dest="nbplate", type=int, action="store",
                            help="Number of Plate")
        parser.add_argument("-r", "--nbrep", dest="nbrep", default=3, type=int, action="store",
                            help="Number of replicat per plate (default: %(default)s)")
        parser.add_argument("-f", "--feat", dest="feat", action="store", type=str,
                            help="Feature to analyze in simple mode")
        parser.add_argument("-s", "--thres", dest="thres", default=50, type=int, action="store",
                            help="Threshold for determining positive cells (default: %(default)s)")
        parser.add_argument("-n", "--neg", dest="neg", action="store", type=str,
                            help="Negative Control")
        parser.add_argument("-p", "--pos", dest="pos", action="store", type=str,
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

        # plaque + TCA.Core.PlateMap(platemap=os.path.join(__INPUT__, "Pl"+str(plateid)+"PP.csv"))
        # for i in range(1, __NBREP__+1):
        # plaque + TCA.Core.Replicat(name="rep"+str(i), data=os.path.join(__INPUT__, "Pl"+str(plateid)+"rep_"+str(i)+".csv"))

        plaque = None
        print(__INPUT__)
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
    results = pool.map_async(simple_plate_analyzis, range(1, 20 + 1))
    print(results.get())
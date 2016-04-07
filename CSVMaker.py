#!/usr/bin/env python3
# encoding: utf-8
"""
Python File Parser for HTS data file (csv)(single cell data or 1data/well).
give a directory that contains multiple subdirectory that contain Legend.xml, Well.csv and Plate.csv
"""

import os
import os.path
import sys
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import time
import pandas as pd
import TransCellAssay as TCA
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

__author__ = "Arnaud KOPP"
__version__ = "1.0"

DEBUG = 1
PRINT = True

'''Generic exception to raise and log different fatal errors.'''


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

  Created by Arnaud.
  Copyright 2014 KOPP. All rights reserved.
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.
  VERSION = %s

USAGE
''' % (program_shortdesc, str(__version__))

    try:
        # # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-i", "--inputFileDirectory", dest="input", action="store",
                            help="File path of csv data file ", required=True)
        parser.add_argument("-o", "--outputFileDirectory", dest="output", action="store",
                            help="Output path of csv file", default=None)
        parser.add_argument("-t", "--filetarget", dest="dest", action="store",default="Well.csv",
                            help="Create csv from Cells feature or Well feature")
        parser.add_argument('--remove-col', dest='removecol', action='store_true', help="Remove some useless columns")
        parser.add_argument('--remove-nan', dest='removenan', action='store_true', help="Remove rows where is nan")

        # # Process arguments
        args = parser.parse_args()
        input_dir = args.input
        if args.output is None:
            output = input_dir
        else:
            output = args.output
        dest = args.dest

        if not os.path.isdir(output):
            os.makedirs(output)

        print("\n*********** START ***********\n")

        for root, dirs, filenames in os.walk(input_dir):
            if "Plate.csv" in filenames:
                try:
                    well = pd.read_csv((root + "/Plate.csv"))
                except:
                    try:
                        well = pd.read_csv((root + "/Plate.csv"), decimal=",", sep=";")
                    except Exception as e:
                        print("Error in reading  File", e)

                barcode = well['Plate Name'][0]

                try:
                    # # read
                    file = TCA.CSV()
                    file.load(fpath=os.path.join(root, dest))

                    # # create well
                    file.format_well_format()
                    try:
                        if args.removecol:
                            file.remove_col()
                        if args.removenan:
                            file.remove_nan()
                    except:
                        pass
                    outputfilename = barcode
                    file.write_raw_data(path=output, name=outputfilename)
                    print("********************************************")
                except Exception as e:
                    print(e)
        print("\n*********** END ***********\n")
    except KeyboardInterrupt:
        # ## handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG:
            print(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    time_stop = time.time()
    print("Executed in {0:f}s".format(float(time_stop - time_start)))


if __name__ == "__main__":
    main()

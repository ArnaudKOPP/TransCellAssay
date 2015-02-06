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

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

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
                            help="Input path of csv data file ", required=True)
        parser.add_argument("-o", "--outputFileDirectory", dest="output", action="store",
                            help="Output path of csv file", required=True)

        # # Process arguments
        args = parser.parse_args()
        input_dir = args.input
        output = args.output

        print("\n*********** START ***********\n")

        try:
            os.stat(output)
        except:
            os.mkdir(output)
        for root, dirs, filenames in os.walk(input_dir):
            if "Legend.xml" in filenames:
                try:
                    well = pd.read_csv((root + "/Plate.csv"))
                except:
                    try:
                        well = pd.read_csv((root + "/Plate.csv"), decimal=",", sep=";")
                    except Exception as e:
                        print("Error in reading  File", e)

                barcode = well['PlateId/Barcode'][0]

                # # read
                file = TCA.CSV()
                file.load(fpath=os.path.join(root, "Cell.csv"))

                # # create well
                file.format_data()
                file.remove_col()
                file.remove_nan()
                outputfilename = barcode
                file.write_raw_data(path=output, name=outputfilename)
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


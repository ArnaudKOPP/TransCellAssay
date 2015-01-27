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
from TransCellAssay.IO.Input import CSV_Reader, Excel_Reader, TXT_Reader

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
        parser.add_argument("-m", "--oldmode", dest="oldmode", des='mode', action="store_true",
                            help="old mode of directory")

        # # Process arguments
        args = parser.parse_args()
        input = args.input
        output = args.output
        mode = args.mode

        # # Old api and directory style
        if mode:
            i = 1
            # # Process arguments
            args = parser.parse_args()
            filed = args.inputDir
            outputd = args.outputDir
            # # init file parser
            excel_parser = Excel_Reader()
            csv_parser = CSV_Reader()
            txt_parser = TXT_Reader()

            try:
                os.stat(outputd)
            except:
                os.mkdir(outputd)

            print("\n*********** START ***********\n")
            print("READING INPUT DIRECTORY ")

            if filed:
                for root, dirs, filenames in os.walk(filed):
                    try:
                        for input_file_tmp in filenames:
                            extension = input_file_tmp.split(".")[-1]
                            input_file = filed + str(input_file_tmp)
                            try:
                                # # make process for each type of file
                                if extension.lower() == 'XLS':
                                    print("xls file %d opening ..." % i)
                                    output_file = input_file_tmp.split(".")[0] + ".csv"
                                    name_file = os.path.join(outputd, output_file)
                                    excel_parser.read_save_data(input_file, name_file)
                                    print("... xls file %d closing \n" % i)
                                    i += 1
                                elif extension.lower() == 'xls':
                                    print("xls file %d opening ..." % i)
                                    output_file = input_file_tmp.split(".")[0] + ".csv"
                                    name_file = os.path.join(outputd, output_file)
                                    excel_parser.read_save_data(input_file, name_file)
                                    print("... xls file %d closing \n" % i)
                                    i += 1
                                elif extension.lower() == 'CSV':
                                    print("csv file %d opening ..." % i)
                                    name_file = os.path.join(outputd, input_file_tmp)
                                    csv_parser.read_data(input_file)
                                    csv_parser.save_data(name_file)
                                    print("... csv file %d closing \n" % i)
                                    i += 1
                                elif extension.lower() == 'csv':
                                    print("csv file %d opening ..." % i)
                                    name_file = os.path.join(outputd, input_file_tmp)
                                    csv_parser.read_data(input_file)
                                    csv_parser.save_data(name_file)
                                    print("... csv file %d closing \n" % i)
                                    i += 1
                                elif extension.lower() == 'txt':
                                    print("txt file %d opening ..." % i)
                                    output_file_tmp = input_file_tmp.split(".")[0] + ".csv"
                                    name_file = os.path.join(outputd, output_file_tmp)
                                    txt_parser.read_data(input_file)
                                    txt_parser.save_data(name_file)
                                    print("... txt file %d closing \n" % i)
                                    i += 1
                                else:
                                    print("No support of this format for file : %s \n" % (str(input_file_tmp)))
                            except Exception as e:
                                print("Error in reading data dir")
                                print(e)
                    except Exception as e:
                        print(e)
            print("\n*********** END ***********\n")

        else:
            try:
                os.stat(output)
            except:
                os.mkdir(output)
            print("Beging Processing")
            for root, dirs, filenames in os.walk(input):
                if "Legend.xml" in filenames:

                    print("Working on %s" % root)
                    try:
                        well = pd.read_csv((root + "/Plate.csv"))
                    except:
                        try:
                            well = pd.read_csv((root + "/Plate.csv"), decimal=",", sep=";")
                        except Exception as e:
                            print("Error in reading  File", e)

                    barcode = well['PlateId/Barcode'][0]

                    # # read
                    file =TCA.CSV()
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


#!/usr/bin/env python3
# encoding: utf-8
"""
Python File Parser for cleaning HTS data file (csv (HCS explorer) or excel (InCELL 1000))
Prod release with minimal features and error printing
"""

import sys
import os
import os.path
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import time
from TransCellAssay.IO.Input import CSV_Reader, Excel_Reader, TXT_Reader


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"
__date__ = '2014-03-21'
__updated__ = '2014-06-12'

DEBUG = 1
PRINT = True


class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argvalues=None):  # IGNORE:C0111
    """Command line options."""
    time_start = time.time()

    if argvalues is None:
        argvalues = sys.argv
    else:
        sys.argv.extend(argvalues)

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
    i = 1
    try:
        # # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-i", "--inputFileDir", dest="inputDir", action="store",
                            help="Input directory path for data file", required=True)
        parser.add_argument("-o", "--outputFileDir", dest="outputDir", action="store",
                            help="Output directory path for csv data file", required=True)


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
    print("Executed in %f" % (float(time_stop - time_start)))


if __name__ == "__main__":
    main()

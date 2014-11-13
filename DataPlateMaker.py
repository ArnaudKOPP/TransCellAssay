#!/usr/bin/env python3
# encoding: utf-8
"""
Python File Parser for HTS data file (csv)(only data by Well) and output only features data in plate format.
give a directory that contains multiple subdirectory that contain Legend.xml, Well.csv and Plate.csv
"""

import os
import os.path
import sys
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import time
import pandas as pd
import xlsxwriter

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
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


# # **pretty ugly**
def init_plate(worksheet, size):
    """
    Init plate label in excel sheet
    """
    if int(size) == 96:
        # print("96 wells")
        worksheet.write('A1', "")
        worksheet.write('A2', "A")
        worksheet.write('A3', "B")
        worksheet.write('A4', "C")
        worksheet.write('A5', "D")
        worksheet.write('A6', "E")
        worksheet.write('A7', "F")
        worksheet.write('A8', "G")
        worksheet.write('A9', "H")

        worksheet.write('B1', "1")
        worksheet.write('C1', "2")
        worksheet.write('D1', "3")
        worksheet.write('E1', "4")
        worksheet.write('F1', "5")
        worksheet.write('G1', "6")
        worksheet.write('H1', "7")
        worksheet.write('I1', "8")
        worksheet.write('J1', "9")
        worksheet.write('K1', "10")
        worksheet.write('L1', "11")
        worksheet.write('M1', "12")
        return worksheet
    elif int(size) == 384:
        # print("384 Wells")
        worksheet.write('A1', "")
        worksheet.write('A2', "A")
        worksheet.write('A3', "B")
        worksheet.write('A4', "C")
        worksheet.write('A5', "D")
        worksheet.write('A6', "E")
        worksheet.write('A7', "F")
        worksheet.write('A8', "G")
        worksheet.write('A9', "H")
        worksheet.write('A10', "I")
        worksheet.write('A11', "J")
        worksheet.write('A12', "K")
        worksheet.write('A13', "L")
        worksheet.write('A14', "M")
        worksheet.write('A15', "N")
        worksheet.write('A16', "O")
        worksheet.write('A17', "P")

        worksheet.write('B1', "1")
        worksheet.write('C1', "2")
        worksheet.write('D1', "3")
        worksheet.write('E1', "4")
        worksheet.write('F1', "5")
        worksheet.write('G1', "6")
        worksheet.write('H1', "7")
        worksheet.write('I1', "8")
        worksheet.write('J1', "9")
        worksheet.write('K1', "10")
        worksheet.write('L1', "11")
        worksheet.write('M1', "12")
        worksheet.write('N1', "13")
        worksheet.write('O1', "14")
        worksheet.write('P1', "15")
        worksheet.write('Q1', "16")
        worksheet.write('R1', "17")
        worksheet.write('S1', "18")
        worksheet.write('T1', "19")
        worksheet.write('U1', "20")
        worksheet.write('V1', "21")
        worksheet.write('W1', "22")
        worksheet.write('X1', "23")
        worksheet.write('Y1', "24")
        return worksheet


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
                            help="Output path of xlsx file", required=True)

        # # format string to float
        def format(x):
            return (float(x))

        # # Process arguments
        args = parser.parse_args()
        input = args.input
        output = args.output
        try:
            os.stat(output)
        except:
            os.mkdir(output)
        print("Beging Processing")
        for root, dirs, filenames in os.walk(input):
            if "Legend.xml" in filenames:

                try:

                    well = pd.read_csv((root + "/Plate.csv"))
                except:
                    try:
                        well = pd.read_csv((root + "/Plate.csv"), decimal=",", sep=";")
                    except Exception as e:
                        print("Error in reading  File", e)

                barcode = well['PlateId/Barcode'][0]
                nbrow = well['NumberOfRows'][0]
                nbcol = well['NumberOfColumns'][0]

                if nbrow * nbcol > 96:
                    size = 396
                else:
                    size = 96

                try:
                    data = pd.read_csv((root + "/Well.csv"))
                except:
                    try:
                        data = pd.read_csv((root + "/Well.csv"), decimal=",", sep=";")
                    except Exception as e:
                        print("Error in reading File", e)

                skip = ['PlateNumber', 'Status', 'Zposition', 'Row', 'Column']

                # # get all feature (columns)
                all_col = data.columns

                # # create new excel file and worksheet
                workbook = xlsxwriter.Workbook(output + barcode + '-save.xlsx')
                i = 0
                list_sheets = ["%s" % x for x in (all_col - skip)]
                # # put on feature per sheet
                for feat in all_col:
                    if feat in skip:
                        continue

                    if data[feat].dtypes == 'object':
                        data[feat] = data[feat].str.replace(",", ".")
                    data[feat].apply(format)
                    data = data.fillna(0)
                    list_sheets[i] = workbook.add_worksheet(str(feat))
                    list_sheets[i] = init_plate(list_sheets[i], size)
                    # # put value in cell
                    for pos in range(len(data.Row)):
                        row = int(data.Row[pos]) + 1
                        try:
                            col = int(data.Column[pos]) + 1
                        except:
                            try:
                                col = int(data.Column[pos]) + 1
                            except Exception as e:
                                print(e)
                        tmp = data.loc[[pos]]
                        val = float(tmp[str(feat)])
                        list_sheets[i].write_number(row, col, val)
                    i += 1
                workbook.close()

        print("DONE")
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

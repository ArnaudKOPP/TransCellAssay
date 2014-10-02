#!/usr/bin/env python3
# encoding: utf-8
__author__ = 'Arnaud KOPP'
"""
Example of program for use TransCellAssay module
"""
import os
import sys
import time
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from platform import python_version
import TCA
import Statistic
import numpy as np
import Statistic.Normalization

__version__ = 0.01

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
    '''Command line options.'''
    time_start = time.time()

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_license = '''
  Created by Arnaud .
  Copyright 2014 KOPP. All rights reserved.
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.
  VERSION = %s

USAGE
''' % (str(__version__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-i", "--inputFileDirectory", dest="input", action="store",
                            help="Input path of data file ", required=True)
        # parser.add_argument("-o", "--outputFileDirectory", dest="output", action="store",
        # help="Output path for result file", required=True)
        #
        InArgs = parser.parse_args()
        InputFileDirectory = InArgs.input

        # test
        print("")
        print("INPUT READING DATA")
        print("")
        screen_test = TCA.Screen()
        plaque1 = TCA.Plate()
        platesetup = TCA.PlateSetup()
        platesetup.setPlateSetup("/home/akopp/Bureau/test/Pl1PP.csv")
        plaque1.addPlateSetup(platesetup)
        rep1 = TCA.Replicat()
        rep1.setInfo("rep1")
        rep1.setData("/home/akopp/Bureau/test/Pl1rep_1.csv")
        rep2 = TCA.Replicat()
        rep2.setInfo("rep2")
        rep2.setData("/home/akopp/Bureau/test/Pl1rep_2.csv")
        rep3 = TCA.Replicat()
        rep3.setInfo("rep3")
        rep3.setData("/home/akopp/Bureau/test/Pl1rep_3.csv")
        plaque1.addReplicat(rep1)
        plaque1.addReplicat(rep2)
        plaque1.addReplicat(rep3)

        # print('Screen stat :')
        # plaque1.printReplicat()
        # print("Number of replicat : ", plaque1.getNumberReplicat())

        screen_test.addPlate(plaque1)

        print("")
        print("BEGIN COMPUTATION TEST")
        print("")
        tmp2 = Statistic.computePlateAnalyzis(plaque1, ['Cell'])
        print(tmp2)



        array = np.genfromtxt("/home/akopp/Bureau/testmedpol.csv", delimiter=",")
        medpol = Statistic.Normalization.MedianPolish(array)

        ge, ce, re, resid, tbl_org = medpol.median_polish(100)
        print("median polish:")
        print("grand effect = ", ge)
        print("column effects = ", ce)
        print("row effects = ", re)
        print("-----Table of Residuals-------")
        print(resid)
        print("-----Original Table-------")
        print(tbl_org)

        ge, ce, re, resid, tbl_org = medpol.median_polish(100, "average")
        print("average polish:")
        print("grand effect = ", ge)
        print("column effects = ", ce)
        print("row effects = ", re)
        print("-----Table of Residuals-------")
        print(resid)
        print("-----Original Table-------")
        print(tbl_org)


        #IO.parseInputDirectory(InputFileDirectory)

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
    print("Executed in {0:f}s".format(float(time_stop - time_start)))


if __name__ == "__main__":
    print('This Python program is launch with ', python_version(), ' version, it was only tested on > 3.3 plateform')
    main()
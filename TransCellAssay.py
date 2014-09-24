#!/usr/bin/env python3
# encoding: utf-8


__author__ = 'Arnaud KOPP'


import os
import sys
import time
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import TCA

__version__ = 0.01
__date__ = '2014-09-23'
__updated__ = '2014-09-23'
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
        # # Setup argument parser
        # parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        # parser.add_argument("-i", "--inputFileDirectory", dest="input", action="store",
        #                     help="Input path of data file ", required=True)
        # parser.add_argument("-o", "--outputFileDirectory", dest="output", action="store",
        #                     help="Output path for result file", required=True)
        #
        # InArgs = parser.parse_args()


        # test
        plate = TCA.Plate()
        rep1 = TCA.Replicat()
        rep2 = TCA.Replicat()
        rep3 = TCA.Replicat()
        plate.addreplicat("rep1", rep1)
        plate.addreplicat("rep2", rep2)
        plate.addreplicat("rep3", rep3)
        plate.printreplicat()

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
    main()
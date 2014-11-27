"""
Librarie for easy play with HTS csv data file (HCS explorer output style)
"""

import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class CSV_Reader():
    """
    classdocs
    Class for reading data CSV file, cleaning them, and rewrite them.
    """

    # columns that we can remove because useless
    # u'ImageLinkWellID'
    to_remove = [u'Well', u'PlateID', u'ImageLinkWellID', u'UPD', u'Barcode', u'TimePoint', u'TimeInterval'
        , u'FieldID', u'CellID', u'Left', u'Top', u'Height', u'Width', u'FieldIndex', u'CellNum']

    def __init__(self, ):
        """
        Constructor
        """
        self.data = pd.DataFrame()

    # # format string to float
    def format(x):
        return (float(x))

    def read_data(self, input):
        """
        Read csv data file, remove predifined useless features, remove empty row, make good well format.
        """
        print(" -> Start processing")
        try:
            # # read csv file
            try:
                self.data = pd.read_csv(input)
            except:
                try:
                    self.data = pd.read_csv(input, decimal=",", sep=";")
                except Exception as e:
                    print(e)
                    print("Error in reading %s File" % input)
            try:
                # # remove useless features
                self.data = self.data.drop(self.to_remove, axis=1)
                ## remove row with NaN(empty)
                self.data = self.data.dropna(axis=0)
            except Exception as e:
                print(e)

            self.data[['Row', 'Column']] = self.data[['Row', 'Column']].astype(int)


            # # rename row from number to name **pretty ugly**
            self.data = self.data.replace({'Row': {0: 'A'}})
            self.data = self.data.replace({'Row': {1: 'B'}})
            self.data = self.data.replace({'Row': {2: 'C'}})
            self.data = self.data.replace({'Row': {3: 'D'}})
            self.data = self.data.replace({'Row': {4: 'E'}})
            self.data = self.data.replace({'Row': {5: 'F'}})
            self.data = self.data.replace({'Row': {6: 'G'}})
            self.data = self.data.replace({'Row': {7: 'H'}})
            self.data = self.data.replace({'Row': {8: 'I'}})
            self.data = self.data.replace({'Row': {9: 'J'}})
            self.data = self.data.replace({'Row': {10: 'K'}})
            self.data = self.data.replace({'Row': {11: 'L'}})
            self.data = self.data.replace({'Row': {12: 'M'}})
            self.data = self.data.replace({'Row': {13: 'N'}})
            self.data = self.data.replace({'Row': {14: 'O'}})
            self.data = self.data.replace({'Row': {15: 'P'}})
            ## insert Well columns
            self.data.insert(0, "Well", 0)
            ## put Well value from row and col columns
            self.data['Well'] = self.data.apply(lambda x: '%s%.3g' % (x['Row'], x['Column'] + 1), axis=1)
            remove = [u'Row', u'Column']
            # self.data = self.data.drop(remove, axis=1)
            col = self.data.columns

            ## change , to . in float
            for feat in col[1:]:
                self.data[feat].apply(format)
                if self.data[feat].dtypes == 'object':
                    self.data[feat] = self.data[feat].str.replace(",", ".")
        except Exception as e:
            print(e)
        print(" -> DONE")

    def save_data(self, output):
        """
        Save DataFrame into csv file.
        """
        try:
            # save the data into csv file
            self.data.to_csv(output, index=False, index_label=False)
        except Exception as e:
            print(e)
# coding=utf-8
"""
Librarie for easy play with HTS excel data file (InCELL 1000)
"""
from TransCellAssay.IO.Input.InputFile import InputFile
import os
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class EXCEL(InputFile):
    """
    Class for load excel file
    """
    def __init__(self):
        super(EXCEL, self).__init__()

    def load(self, fpath):
        # # obtention des noms de chaque sheet du excel
        """
        Load excel file
        :param fpath:
        """
        xls = pd.ExcelFile(fpath)
        columns_name = xls.sheet_names
        measures = filter(lambda x: 'Cell measures' in x, columns_name)
        data = None
        compt = 0
        for i in measures:
            compt += 1
            print("sheet : %d" % compt)
            if data is None:
                data = pd.read_excel(fpath, i)
            else:
                data = data.append(pd.read_excel(fpath, i))
            data.fillna(0)

        self.dataframe = data


class Excel_Reader():
    """
    classdocs
    Class for reading data excel file, and rewrite them to csv file.
    """

    def __init__(self, ):
        """
        Constructor
        """

    def read_save_data(self, file, output):
        """
        Function for read Excel file and convert them into pandas DataFrame, and save the dataframe into csv.
        """
        try:
            print(" -> Start processing")
            # # obtention des noms de chaque sheet du excel
            xls = pd.ExcelFile(file)
            columns_name = xls.sheet_names
            measures = filter(lambda x: 'Cell measures' in x, columns_name)
            list_files = []
            data = pd.DataFrame()
            compt = 0
            for i in measures:
                compt += 1
                print("sheet : %d" % compt)
                temp_file = file.split(".")[0]
                output_temp = temp_file + str(compt) + ".csv"
                list_files.append(output_temp)
                data = pd.read_excel(file, i)
                data.fillna(0)
                data.to_csv(output_temp, index=False)

            print("   -> Merging multiple csv")
            # # merging of multiple csv
            cmd = "cat "
            output += str()
            for i in list_files:
                print(str(i))
                cmd = cmd + str(i) + " "
            cmd = cmd + "> " + str(output)
            os.system(cmd)
            print("   -> Create Final csv file")
            df = pd.DataFrame()
            df = pd.read_csv(output)
            # # changing well notation
            df["Well"] = df["Well"].str.replace(' - ', '')
            df["Well"] = df["Well"].str.replace(r"\(.*\)", "")
            col = data.columns
            for feat in col[1:]:
                data[feat] = data[feat].str.replace(",", ".")
            df.to_csv(output, index=False)
            print("   -> Remove temp file")
            for i in list_files:
                os.remove(i)
        except Exception as e:
            print(e)
        print(" --> DONE")
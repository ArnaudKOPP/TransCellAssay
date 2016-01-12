#!/usr/bin/env python3
# encoding: utf-8
import tkinter as tk
from tkinter.filedialog import askdirectory
import tkinter.messagebox
import os
import os.path
import sys
import time
import pandas as pd
import xlsxwriter
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


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


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("FormatPlaque")
        self.dirname = None
        self.createWidgets()

    def createWidgets(self):
        tk.Button(self.master, text="Browse", command=self.load_dir).grid(row=0, column=1, sticky=tk.W, pady=4)
        tk.Button(self.master, text="DO", command=self.format_dir).grid(row=1, column=1, sticky=tk.W, pady=4)
        tk.Button(self.master, text='Quit', command=self.master.quit).grid(row=2, column=1, sticky=tk.W, pady=4)

    def load_dir(self):
        self.dirname = askdirectory()
        print(self.dirname)

    def format_dir(self):
        # # format string to float
        def format(x):
            return (float(x))

        if self.dirname is None:
            tkinter.messagebox.showerror(message="You must select a directory")
            return

        input = self.dirname
        output = self.dirname

        if not os.path.isdir(output):
            os.makedirs(output)

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

                logging.info('Work on {}'.format(barcode))

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

                # # get all channel (columns)
                all_col = data.columns

                # # create new excel file and worksheet
                workbook = xlsxwriter.Workbook(output + barcode + '-save.xlsx')
                i = 0
                list_sheets = ["%s" % x for x in (all_col - skip)]
                # # put on channel per sheet
                for chan in all_col:
                    if chan in skip:
                        continue

                    logging.debug('Work on {} channel'.format(chan))

                    if data[chan].dtypes == 'object':
                        data[chan] = data[chan].str.replace(",", ".")
                    data[chan].apply(format)
                    data = data.fillna(0)

                    ## if chan is to long, cut it
                    if len(str(chan)) >= 30:
                        Chan = ''.join(x for x in str(chan) if not x.islower())
                        logging.warning('Channel {0} is writed as {1}'.format(chan, Chan))
                    else:
                        Chan = str(chan)

                    list_sheets[i] = workbook.add_worksheet(Chan)
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
                        val = float(tmp[str(chan)])
                        list_sheets[i].write_number(row, col, val)
                    i += 1
                workbook.close()

                logging.info('Finish {}'.format(barcode))


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()

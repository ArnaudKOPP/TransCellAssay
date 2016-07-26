#!/usr/bin/env python3
# encoding: utf-8
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
# sys.path.append('')
import TransCellAssay as TCA
import tkinter.messagebox
import os
import os.path
import sys
import collections
import logging
import pandas as pd
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


class MainAppFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.__dirpath = ''
        self.master = master
        self.master.title('Analyse de plaque pour screen')
        Label(self.master, text="Neg Ctrl").grid(row=0)
        Label(self.master, text="Pos Ctrl").grid(row=1)
        Label(self.master, text="Channel").grid(row=2)
        Label(self.master, text="Threshold Value").grid(row=3)
        Label(self.master, text="Threshold type").grid(row=4)
        Label(self.master, text="Plate Size").grid(row=5)

        self.NegCtrl = Entry(self.master)
        self.PosCtrl = Entry(self.master)
        self.ChnVal = Entry(self.master)
        self.ThrsVal = Entry(self.master)
        self.NegCtrl.grid(row=0, column=1)
        self.PosCtrl.grid(row=1, column=1)
        self.ChnVal.grid(row=2, column=1)
        self.ThrsVal.grid(row=3, column=1)

        self.plate_size = StringVar()
        Combobox(self.master, textvariable=self.plate_size, values=('96', '384'), state='readonly').grid(row=5, column=1, sticky=W, pady=4)
        self.plate_size.set('96')

        self.threshold_type = StringVar()
        Combobox(self.master, textvariable=self.threshold_type, values=('Percent', 'value'), state='readonly').grid( row=4, column=1, sticky=W, pady=4)
        self.threshold_type.set('Percent')

        # button of bottom line
        Button(self.master, text='Quit', command=self.master.quit).grid(row=6, column=0, sticky=W, pady=4)
        Button(self.master, text="Browse", command=self.load_dir).grid(row=6, column=1, sticky=W, pady=4)
        Button(self.master, text='Launch', command=self.analyse).grid(row=6, column=2, sticky=W, pady=4)

    def analyse(self):
        if self.__dirpath is '':
            tkinter.messagebox.showerror(message="You must select a directory")
            logging.error('Must select a directory')
            return
        logging.info("Format Data : {}".format(self.__dirpath))

        ## Dict for storing plate ant their replica into a 'tree'
        FileDict = collections.OrderedDict()


        for root, dirs, filenames in os.walk(self.__dirpath):
            if "Legend.xml" in filenames:
                try:
                    try:

                        well = pd.read_csv((root + "/Plate.csv"))
                    except:
                        try:
                            well = pd.read_csv((root + "/Plate.csv"), decimal=",", sep=";")
                        except Exception as e:
                            print("Error in reading  File", e)

                    PlateId = well['PlateId/Barcode'][0]

                    ## if file aren't already formatted
                    if not os.path.isfile(os.path.join(self.__dirpath, PlateId+'.csv')):
                        logging.info('Read Plate : {}'.format(PlateId))

                        # # read Data
                        file = TCA.CSV()
                        file.load(fpath=os.path.join(root, "Cell.csv"))

                        #  # create well format
                        file.format_well_format()
                        try:
                            file.remove_col()
                            file.remove_nan()
                        except:
                            pass
                        file.write_raw_data(path=self.__dirpath, name=PlateId, frmt='csv')


                    FileDict[PlateId] = os.path.join(self.__dirpath, PlateId+".csv")

                    print(FileDict)

                except Exception as e:
                    logging.error(e)

        logging.debug(FileDict)

        outpath = os.path.join(self.__dirpath, time.asctime())
        if not os.path.isdir(outpath):
            os.makedirs(outpath)



        NegRef = self.NegCtrl.get()
        if NegRef == '':
            NegRef = None

        PosRef = self.PosCtrl.get()
        if PosRef == '':
            PosRef = None

        ChanRef = self.ChnVal.get()
        if ChanRef== '':
            ChanRef = None
        else:
            ChanRef = [ChanRef]

        noposcell=False
        thresRef = self.ThrsVal.get()
        if thresRef== '':
            thresRef = None
            noposcell=True

        if self.threshold_type.get() == 'Percent':
            thresTypePercent = True
            thresTypeFixedVal = False
        else:
            thresTypePercent = False
            thresTypeFixedVal = True


        logging.info("Launch analyse ")

        # Load a plate with their replica
        for key, value in FileDict.items():
            plaque = TCA.Core.Plate(name=key, platemap=TCA.Core.PlateMap(size=int(self.plate_size.get())))

            plaque + TCA.Core.Replica(name=key, fpath=value, FlatFile=True)

            ## Do your analysis here after plate were created

            if ChanRef is not None and noposcell is False:
                df, thres = TCA.PlateChannelsAnalysis(plaque, channels=ChanRef,
                                            neg=NegRef,
                                            pos=PosRef,
                                            threshold=thresRef,
                                            percent=thresTypePercent,
                                            fixed_threshold=thresTypeFixedVal,
                                            clean=False,
                                            noposcell=noposcell,
                                            multiIndexDF=True)

                df.to_csv(os.path.join(self.__dirpath, key+'.csv'), header=true, index=False)
            else:
                df = TCA.PlateChannelsAnalysis(plaque, channels=ChanRef,
                                            neg=NegRef,
                                            pos=PosRef,
                                            threshold=thresRef,
                                            percent=thresTypePercent,
                                            fixed_threshold=thresTypeFixedVal,
                                            clean=False,
                                            noposcell=noposcell,
                                            multiIndexDF=True)

                df.to_csv(os.path.join(outpath, key+'.csv'), header=True, index=False)

            del plaque

        logging.info("  ----->>>  Finished    \./")

    def load_dir(self):
        self.__dirpath = askdirectory()
        logging.info("Directory loaded : {}".format(self.__dirpath))

def main():
    root = Tk()
    app = MainAppFrame(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()

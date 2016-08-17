#!/usr/bin/env python3
# encoding: utf-8
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
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
        self.master.title('Plate Analyser')
        Label(self.master, text="Neg Ctrl").grid(row=0)
        Label(self.master, text="Channel").grid(row=2)
        Label(self.master, text="Threshold Value").grid(row=3)
        Label(self.master, text="Threshold type").grid(row=4)
        Label(self.master, text="Plate Size").grid(row=5)

        self.NegCtrl = Entry(self.master)
        self.PosCtrl = Entry(self.master)
        self.ChnVal = Entry(self.master)
        self.ThrsVal = Entry(self.master)
        self.NegCtrl.grid(row=0, column=1)
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
        Button(self.master, text="Browse File", command=self.load_dir).grid(row=6, column=1, sticky=W, pady=4)
        Button(self.master, text='Analyse', command=self.Analyse).grid(row=6, column=2, sticky=W, pady=4)
        Button(self.master, text='CellsCount', command=self.CellsCount).grid(row=6, column=3, sticky=W, pady=4)

    def CellsCount(self):
        if self.__dirpath is '':
            tkinter.messagebox.showerror(message="You must select a directory")
            logging.error('Must select a directory')
            return
        logging.info("Format Data : {}".format(self.__dirpath))


        outpath = os.path.join(self.__dirpath, time.asctime())
        if not os.path.isdir(outpath):
            os.makedirs(outpath)



        ChanRef = self.ChnVal.get()
        if ChanRef== '':
            ChanRef = None
        else:
            ChanRef = [ChanRef]


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


                        logging.info("Make Cells Count on {}".format(PlateId))


                        plaque = TCA.Core.Plate(name=PlateId, platemap=TCA.Core.PlateMap(size=int(self.plate_size.get())))

                        plaque + TCA.Core.Replica(name="rep1", fpath=file)

                        ## Do your analysis here after plate were created
                        df = TCA.PlateChannelsAnalysis(plaque, channels=ChanRef,
                                                            neg=None,
                                                            noposcell=True,
                                                            multiIndexDF=True)

                        df.to_csv(os.path.join(outpath, plaque.name+'.csv'), header=True, index=False)

                        del plaque


                except Exception as e:
                    logging.error(e)


        logging.info("  ----->>>  Finished    \./")

    def Analyse(self):
        if self.__dirpath is '':
            tkinter.messagebox.showerror(message="You must select a directory")
            logging.error('Must select a directory')
            return
        logging.info("Format Data : {}".format(self.__dirpath))


        outpath = os.path.join(self.__dirpath, time.asctime())
        if not os.path.isdir(outpath):
            os.makedirs(outpath)


        NegRef = self.NegCtrl.get()
        if NegRef == '':
            NegRef = None


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
        else:
            thresRef = int(thresRef)

        if self.threshold_type.get() == 'Percent':
            thresTypePercent = True
            thresTypeFixedVal = False
        else:
            thresTypePercent = False
            thresTypeFixedVal = True



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


                        logging.info("Launch analyse ")


                        plaque = TCA.Core.Plate(name=PlateId, platemap=TCA.Core.PlateMap(size=int(self.plate_size.get())))

                        plaque + TCA.Core.Replica(name="rep1", fpath=file)

                        if NegRef is not None:
                            NegRef = NegRef.split()
                            for i in NegRef:
                                plaque.platemap[i] = "Neg"
                            NegRef = "Neg"


                        ## Do your analysis here after plate were created

                        if noposcell is False:
                            df, thres = TCA.PlateChannelsAnalysis(plaque, channels=ChanRef,
                                                            neg=NegRef,
                                                            threshold=thresRef,
                                                            percent=thresTypePercent,
                                                            fixed_threshold=thresTypeFixedVal,
                                                            clean=False,
                                                            noposcell=noposcell,
                                                            multiIndexDF=True)

                            df.to_csv(os.path.join(outpath, plaque.name+'.csv'), header=True, index=False)
                        else:
                            df = TCA.PlateChannelsAnalysis(plaque, channels=ChanRef,
                                                            neg=NegRef,
                                                            threshold=thresRef,
                                                            percent=thresTypePercent,
                                                            fixed_threshold=thresTypeFixedVal,
                                                            clean=False,
                                                            noposcell=noposcell,
                                                            multiIndexDF=True)

                            df.to_csv(os.path.join(outpath, plaque.name+'.csv'), header=True, index=False)

                        del plaque


                except Exception as e:
                    logging.error(e)


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

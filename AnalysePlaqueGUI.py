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

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


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

        # Choice for norm
        self.Norm = StringVar()
        Combobox(self.master, textvariable=self.Norm, values=('Zscore', 'RobustZscore', 'PercentOfSample', 'RobustPercentOfSample', 'PercentOfControl', 'RobustPercentOfSample', 'NormalizedPercentInhibition'),
                state='readonly').grid(row=0, column=2, sticky=W, pady=4)

        # Choice for spatial effect norm
        self.SpatNorm = StringVar()
        Combobox(self.master, textvariable=self.SpatNorm, values=('Bscore', 'BZscore', 'PMP', 'MEA'),
                state='readonly').grid(row=1, column=2, sticky=W, pady=4)

        # button of bottom line
        Button(self.master, text='Quit', command=self.master.quit).grid(row=6, column=0, sticky=W, pady=4)
        Button(self.master, text="Browse", command=self.load_dir).grid(row=6, column=1, sticky=W, pady=4)
        Button(self.master, text='Launch', command=self.analyse).grid(row=6, column=2, sticky=W, pady=4)

        # button for log norm or not
        self.LogNorm = BooleanVar()
        Checkbutton(self.master, text="Log Norm",onvalue=True, offvalue=False,variable=self.LogNorm).grid(row=0, column=3)

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

                    # work only with XXXX01.1.csv file name, all replica must have the same XXXX name
                    if (PlateId+'.csv')[0:-6] in FileDict.keys():
                        FileDict[(PlateId+'.csv')[0:-6]]["rep"+(PlateId+'.csv')[-5:-4]] = PlateId+'.csv'
                    else:
                        FileDict[(PlateId+'.csv')[0:-6]] = {"rep"+(PlateId+'.csv')[-5:-4] : PlateId+'.csv'}

                except Exception as e:
                    logging.error(e)

        logging.debug(FileDict)

        outpath = os.path.join(self.__dirpath, time.asctime())
        if not os.path.isdir(outpath):
            os.makedirs(outpath)

        logging.info("Launch analyse :\nneg: {0} \nPos: {1} \nchannel: {2} \nthreshold: {3} \n".format(self.NegCtrl.get(),
            self.PosCtrl.get(), self.ChnVal.get(), self.ThrsVal.get()))

        # Load a plate with their replica
        for key, value in FileDict.items():
            plaque = TCA.Core.Plate(name=key, platemap=TCA.Core.PlateMap(size=int(self.plate_size.get())))

            # load replica into plate
            for key, value in value.items():
                plaque + TCA.Core.Replica(name=key, fpath=os.path.join(self.__dirpath, value), singleCells=True,
                datatype='mean')

            ## Do your analysis here after plate were created

            # First for not normalized data
            if self.threshold_type.get() == 'Percent':
                TCA.plate_channel_analysis(plaque, channel=self.ChnVal.get(), neg=self.NegCtrl.get(), pos=self.PosCtrl.get(),
                                   threshold=int(self.ThrsVal.get()), percent=True, path=outpath,
                                   fixed_threshold=False, tag="_not_normalized")
            else:
                TCA.plate_channel_analysis(plaque, channel=self.ChnVal.get(), neg=self.NegCtrl.get(), pos=self.PosCtrl.get(),
                                   threshold=int(self.ThrsVal.get()), percent=False, path=outpath,
                                   fixed_threshold=True, tag="_not_normalized")

            # normalize your data or not
            if self.Norm.get() is not '':
                plaque.normalization_channels(self.ChnVal.get(), method=self.Norm.get(), log_t=self.LogNorm.get(),
                                                neg=self.NegCtrl.get(), pos=self.PosCtrl.get())

            if self.SpatNorm.get() is not '':
                plaque.systematic_error_correction(algorithm=self.SpatNorm.get(), method='median', apply_down=True, verbose=False,
                                                    save=True, max_iterations=100, alpha=0.05, epsilon=0.01,
                                                    skip_col=[], skip_row=[], trimmed=0.0)

            # Then normalized data
            if self.threshold_type.get() == 'Percent':
                TCA.plate_channel_analysis(plaque, channel=self.ChnVal.get(), neg=self.NegCtrl.get(), pos=self.PosCtrl.get(),
                                   threshold=int(self.ThrsVal.get()), percent=True, path=outpath,
                                   fixed_threshold=False, tag="_normalized")
            else:
                TCA.plate_channel_analysis(plaque, channel=self.ChnVal.get(), neg=self.NegCtrl.get(), pos=self.PosCtrl.get(),
                                   threshold=int(self.ThrsVal.get()), percent=False, path=outpath,
                                   fixed_threshold=True, tag="_normalized")

            file = open(os.path.join(outpath, 'Parameters.txt'), 'w')
            file.write("Input directory         : "+str(self.__dirpath) + "\n")
            file.write("Channel                 : "+str(self.ChnVal.get()) + "\n")
            file.write("Negative ctrl           : "+str(self.NegCtrl.get()) + "\n")
            file.write("Positive ctrl           : "+str(self.PosCtrl.get()) + "\n")
            file.write("Threshold value         : "+str(self.ThrsVal.get()) + "\n")
            file.write("Normalization Method    : "+str(self.Norm.get()) + "\n")
            file.write("Edge effect corection   : "+str(self.SpatNorm.get()) + "\n")
            file.write("Threshold type          : "+str(self.threshold_type.get()) + "\n")
            file.close()

            del plaque

        logging.info("  ----->>>  Finished")

    def load_dir(self):
        self.__dirpath = askdirectory()
        logging.info("Directory loaded : {}".format(self.__dirpath))

def main():
    root = Tk()
    app = MainAppFrame(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()

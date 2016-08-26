#!/usr/bin/env python3
# encoding: utf-8
import tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import TransCellAssay as TCA
import os
import os.path
import sys
import logging
import pandas as pd
import time
import xlsxwriter

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

# # **pretty ugly**
def FP_init_sheet(worksheet, size):
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


class MainAppFrame(tkinter.Frame):

    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        self.master.title('TransCellAssay Main App')

        tkinter.Button(self.master, text='CSV File Formatter', command=self.CSVFFFrame).pack(padx=10, pady=5, fill=BOTH)
        tkinter.Button(self.master, text='Format plaque', command=self.FormatPlaqueFrame).pack(padx=10, pady=5, fill=BOTH)
        tkinter.Button(self.master, text='Analyse', command=self.AnalyseFrame).pack(padx=10, pady=5, fill=BOTH)
        tkinter.Button(self.master, text='QC (beta)', command=self.QualityFrame).pack(padx=10, pady=5, fill=BOTH)
        tkinter.Button(self.master, text='Graph (beta)', command=self.GraphFrame).pack(padx=10, pady=5, fill=BOTH)
        tkinter.Button(self.master, text='EXIT APP', command=self.master.quit, fg="red").pack(padx=10, pady=5, fill=BOTH)

        self.DirPath = None
        self.FilePathToOpen = None

        self.PlateToAnalyse = None


    ### FUNCTION FOR GUI

    def CSVFFFrame(self):
        window = Toplevel(self)
        tkinter.Button(window, text="Browse Directory", command=self.load_dir).pack(padx=10, pady=10, fill=BOTH)
        tkinter.Button(window, text="Do CSV file Formatting", command=self.__DoCSVFile, fg="red").pack(padx=10, pady=10, fill=BOTH)

        self.RemoveCol = IntVar()
        self.RemoveNan = IntVar()
        Checkbutton(window, text = "Remove Useless Columns", variable = self.RemoveCol).pack(padx=10, pady=10, fill=BOTH)
        Checkbutton(window, text = "Remove NaN values", variable = self.RemoveNan).pack(padx=10, pady=10, fill=BOTH)
        self.RemoveCol.set(1)
        self.RemoveNan.set(1)

        Label(window, text="Which csv file use", foreground="black", background="white").pack()

        self.CSV_Target = StringVar()
        Combobox(window, textvariable=self.CSV_Target, values=('Well.csv', 'Cell.csv'), state='readonly').pack(padx=10, pady=10, fill=BOTH)
        self.CSV_Target.set('Cell.csv')

        Label(window, text="Which name to use", foreground="black", background="white").pack()

        self.CSV_OutputName = StringVar()
        Combobox(window, textvariable=self.CSV_OutputName, values=('PlateID/Barcode', 'Plate Name', 'Both'), state='readonly').pack(padx=10, pady=10, fill=BOTH)
        self.CSV_OutputName.set('Both')


    def FormatPlaqueFrame(self):
        window = Toplevel(self)
        tkinter.Button(window, text="Browse Directory", command=self.load_dir).pack(padx=10, pady=10, fill=BOTH)
        tkinter.Button(window, text="Do Format Plaque", command=self.__DoFormatPlaque, fg="red").pack(padx=10, pady=10, fill=BOTH)

        Label(window, text="Which name to use", foreground="black", background="white").pack()

        self.FP_OutputName = StringVar()
        Combobox(window, textvariable=self.FP_OutputName, values=('PlateID/Barcode', 'Plate Name', 'Both'), state='readonly').pack(padx=10, pady=10, fill=BOTH)
        self.FP_OutputName.set('Both')


    def AnalyseFrame(self):
        window = Toplevel(self)

        tkinter.Label(window, text="Neg Ctrl").grid(row=1, column=0)
        tkinter.Label(window, text="Channel").grid(row=2, column=0)
        tkinter.Label(window, text="Threshold Value").grid(row=3, column=0)
        tkinter.Label(window, text="Threshold type").grid(row=4, column=0)
        tkinter.Label(window, text="Plate Size").grid(row=5, column=0)

        self.NegCtrl = tkinter.Entry(window).grid(row=1, column=1)
        self.ChnVal = tkinter.Entry(window).grid(row=2, column=1)
        self.ThrsVal = tkinter.Entry(window).grid(row=3, column=1)


        self.plate_size = StringVar()
        Combobox(window, textvariable=self.plate_size, values=('96', '384'), state='readonly').grid(row=4, column=1)
        self.plate_size.set('96')

        self.threshold_type = StringVar()
        Combobox(window, textvariable=self.threshold_type, values=('Percent', 'value'), state='readonly').grid(row=5, column=1)
        self.threshold_type.set('Percent')



        def donothing():
            filewin = Toplevel(root)
            button = Button(filewin, text="Do nothing button")
            button.pack()


        menubar = tkinter.Menu(window)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Plate", command=self.__init_plate)
        filemenu.add_command(label="Add data file/replica", command=self.__add_replica)
        filemenu.add_command(label="Add platemap file", command=self.__add_platemap)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=window.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tkinter.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Remove replica", command=self.__remove_replica)
        editmenu.add_command(label="Edit Plate", command=self.__edit_plate)
        menubar.add_cascade(label="Edit", menu=editmenu)

        analysemenu = tkinter.Menu(menubar, tearoff=0)
        analysemenu.add_command(label="Do Analyse", command=self.__Analyse)
        analysemenu.add_command(label="Do CellsCount", command=self.__cellsCount)
        menubar.add_cascade(label="Analyse", menu=analysemenu)

        window.config(menu=menubar)


    def QualityFrame(self):
        window = Toplevel(self)
        tkinter.Button(window, text="Browse File", command=self.load_file).pack(padx=10, pady=10)
        tkinter.Button(window, text="Do Quality", fg="red").pack(padx=10, pady=10)


    def GraphFrame(self):
        window = Toplevel(self)
        tkinter.Button(window, text="Browse File", command=self.load_file).pack(padx=10, pady=10)
        tkinter.Button(window, text="Do Quality", fg="red").pack(padx=10, pady=10)


    ## function to open dir and file

    def load_dir(self):
        """
        Function to open a directory
        """
        self.DirPath = tkinter.filedialog.askdirectory()
        logging.debug('Dir loaded : {}'.format(self.DirPath))

    def load_file(self):
        """
        Function to open a file
        """
        self.FilePathToOpen = tkinter.filedialog.askopenfilename()
        logging.debug('File loaded : {}'.format(self.FilePathToOpen))

    def selectFiles(self):
        files = tkinter.filedialog.askopenfilenames(title='Select Input File')
        fileList = root.tk.splitlist(files)
        logging.debug("Selected file : {}".format(fileList))

    def selectFileToSave(self):
        """
        Get a file to save csv file
        """
        self.SaveFilePath = tkinter.filedialog.asksaveasfilename()
        logging.debug('Save file as : {}'.format(self.SaveFilePath))

    ### FUNCTION THAT PERFORM ACTUALLY SOMETHING

    def __DoFormatPlaque(self):
        """
        Function that perform format plaque on selected directory
        """
        if self.DirPath is None:
            tkinter.messagebox.showerror(message="Empty directory, choose one")
            self.load_dir()

        logging.info("Start processing")
        for root, dirs, filenames in os.walk(self.DirPath):
            if "Legend.xml" in filenames:

                try:

                    well = pd.read_csv((root + "/Plate.csv"))
                except:
                    try:
                        well = pd.read_csv((root + "/Plate.csv"), decimal=",", sep=";")
                    except Exception as e:
                        print("Error in reading  File", e)

                if self.FP_OutputName.get() == 'PlateID/Barcode':
                    OutputName = well['PlateId/Barcode'][0]
                elif self.FP_OutputName.get() == 'Plate Name':
                    OutputName = well['Plate Name'][0]
                else:
                    OutputName = "{0}-{1}".format(well['PlateId/Barcode'][0], well['Plate Name'][0])


                nbrow = well['NumberOfRows'][0]
                nbcol = well['NumberOfColumns'][0]

                logging.info('Work on {}'.format(OutputName))

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
                        logging.error("Error in reading File : {}".format(e))

                skip = ['PlateNumber', 'Status', 'Zposition', 'Row', 'Column']

                # # get all channel (columns)
                all_col = data.columns

                # # create new excel file and worksheet
                filename = os.path.join(self.DirPath, OutputName+".xlsx")
                workbook = xlsxwriter.Workbook(filename)

                i = 0
                list_sheets = ["%s" % x for x in (all_col - skip)]
                # # put on channel per sheet

                KnowProblematicChanName = {"MEAN_NeuriteMaxLengthWithoutBranchesCh2":"MEAN_NMLWHBC2"}

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
                        if str(chan) in KnowProblematicChanName:
                            Chan = KnowProblematicChanName[str(chan)]
                            logging.warning('Channel {0} is writed as {1}'.format(chan, Chan))
                        else:
                            Chan = ''.join(x for x in str(chan) if not x.islower())
                            logging.warning('Channel {0} is writed as {1}'.format(chan, Chan))
                    else:
                        Chan = str(chan)

                    list_sheets[i] = workbook.add_worksheet(Chan)
                    list_sheets[i] = FP_init_sheet(list_sheets[i], size)
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

                logging.info('Finish {}'.format(OutputName))

    def __DoCSVFile(self):
        """
        Function that perform conversion to good csv format from output of HCS studio
        """
        if self.DirPath is None:
            tkinter.messagebox.showerror(message="Empty directory, choose one")
            self.load_dir()

        for root, dirs, filenames in os.walk(self.DirPath):
            if "Plate.csv" in filenames:
                try:
                    well = pd.read_csv((root + "/Plate.csv"))
                except:
                    try:
                        well = pd.read_csv((root + "/Plate.csv"), decimal=",", sep=";")
                    except Exception as e:
                        print("Error in reading  File", e)

                if self.CSV_OutputName.get() == 'PlateID/Barcode':
                    OutputName = well['PlateId/Barcode'][0]
                elif self.CSV_OutputName.get() == 'Plate Name':
                    OutputName = well['Plate Name'][0]
                else:
                    OutputName = "{0}-{1}".format(well['PlateId/Barcode'][0], well['Plate Name'][0])

                try:
                    # # read
                    file = TCA.CSV()
                    file.load(fpath=os.path.join(root, self.CSV_Target.get()))

                    # # create well
                    file.format_well_format()
                    try:
                        if self.RemoveCol.get():
                            logging.debug("Remove useless columns")
                            file.remove_col()
                        if self.RemoveNan.get():
                            logging.debug("Remove Nan values")
                            file.remove_nan()
                    except:
                        pass
                    file.write_raw_data(path=self.DirPath, name=OutputName+".csv")
                except Exception as e:
                    logging.error(e)

    def __init_plate(self):
        """
        Init plate
        """
        window = Toplevel(self)

        tkinter.Label(window, text="Plate name").grid(row=1, column=0)
        self.PlateName = StringVar()
        tkinter.Entry(window, textvariable=self.PlateName).grid(row=1, column=1)

        self.plate_size = StringVar()
        Combobox(window, textvariable=self.plate_size, values=('96', '384'), state='readonly').grid(row=2, column=0)
        self.plate_size.set('96')

        tkinter.Button(window, text='Create Plate', command=self.__create_plate).grid(row=2, column=1)
        tkinter.Button(window, text='add file', command=self.selectFiles).grid(row=3, column=0)

    def __create_plate(self):
        """
        create a plate object
        """
        self.PlateToAnalyse = TCA.Plate(name=self.PlateName.get(), platemap=TCA.Core.PlateMap(size=self.plate_size.get()))

    def __edit_plate(self):
        """
        Function for editing plate
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)
        tkinter.Label(window, text="New plate name").grid(row=1, column=0)
        tkinter.Entry(window, textvariable=self.PlateName).grid(row=1, column=1)
        tkinter.Button(window, text='Remove replica', command=lambda: self.PlateToAnalyse.set_name(self.PlateName.get())).grid(row=2, column=0)

    def __add_platemap(self):
        """
        Function for adding a platemap to plate
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)
        tkinter.Button(window, text='Browse file', command=self.load_file).grid(row=1, column=0)
        tkinter.Button(window, text='Add file/replica to plate', command=lambda: self.PlateToAnalyse.add_platemap(TCA.PlateMap(fpath=self.FilePathToOpen))).grid(row=2, column=0)

    def __add_replica(self):
        """
        Function for adding a replica
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)

        tkinter.Button(window, text='Browse file', command=self.load_file).grid(row=1, column=0)

        tkinter.Label(window, text="Replica name").grid(row=2, column=0)
        repname = StringVar()
        tkinter.Entry(window, textvariable=repname).grid(row=2, column=1)
        tkinter.Button(window, text='Add file/replica to plate', command=lambda: self.PlateToAnalyse.add_replica(TCA.Replica(name=repname.get(), fpath=self.FilePathToOpen))).grid(row=3, column=0)

    def __remove_replica(self):
        """
        function for removing a replica
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)
        tkinter.Label(window, text="Replica name to remove").grid(row=1, column=0)
        repname = StringVar()
        tkinter.Entry(window, textvariable=repname).grid(row=1, column=1)
        tkinter.Button(window, text='Remove replica', command=lambda: self.PlateToAnalyse.remove_replica(repname.get())).grid(row=2, column=0)

    def __Analyse(self):
        """
        Do analyse on current plate
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)

        NegRef = self.NegCtrl
        if NegRef == '':
            NegRef = None

        if NegRef is not None:
            NegRef = NegRef.split()
            for i in NegRef:
                plaque.platemap[i] = "Neg"
            NegRef = "Neg"


        ChanRef = self.ChnVal
        if ChanRef== '':
            ChanRef = None
        else:
            ChanRef = [ChanRef]

        noposcell=False
        thresRef = self.ThrsVal
        if thresRef== '':
            thresRef = None
            noposcell=True
        else:
            thresRef = int(thresRef)

        if self.threshold_type == 'Percent':
            thresTypePercent = True
            thresTypeFixedVal = False
        else:
            thresTypePercent = False
            thresTypeFixedVal = True

        if noposcell is False:
            self.CurrentResToSave, thres = TCA.PlateChannelsAnalysis(plaque, channels=ChanRef,
                                            neg=NegRef,
                                            threshold=thresRef,
                                            percent=thresTypePercent,
                                            fixed_threshold=thresTypeFixedVal,
                                            clean=False,
                                            noposcell=noposcell,
                                            multiIndexDF=True)
            logging.info("Threshold value : {}".format(thres))

        else:
            self.CurrentResToSave = TCA.PlateChannelsAnalysis(plaque, channels=ChanRef,
                                            neg=NegRef,
                                            threshold=thresRef,
                                            percent=thresTypePercent,
                                            fixed_threshold=thresTypeFixedVal,
                                            clean=False,
                                            noposcell=noposcell,
                                            multiIndexDF=True)



        tkinter.Button(window, text="Select where to save", fg="red", command=self.selectFileToSave).pack(padx=10, pady=10)
        tkinter.Button(window, text="Save analyse results", fg="red", command=self.__saveFile).pack(padx=10, pady=10)


    def __cellsCount(self):
        """
        Function that perform cellscount
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)

        self.CurrentResToSave = TCA.PlateChannelsAnalysis(self.PlateToAnalyse, channels=None,
                                            neg=None,
                                            noposcell=True,
                                            multiIndexDF=True)



        tkinter.Button(window, text="Select where to save", fg="red", command=self.selectFileToSave).pack(padx=10, pady=10)
        tkinter.Button(window, text="Save cellscount", fg="red", command=self.__saveFile).pack(padx=10, pady=10)

    def __saveFile(self):
        """
        Write csv file
        """
        if self.SaveFilePath is None:
            tkinter.messagebox.showerror(message="No selected file name")
            return

        self.CurrentResToSave.to_csv(self.SaveFilePath, header=True, index=False)


if __name__ == "__main__":
    root = tkinter.Tk()
    view = MainAppFrame(root)
    root.mainloop()

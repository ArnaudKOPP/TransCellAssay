#!/usr/bin/env python3
# encoding: utf-8
import tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import tkinter.filedialog
import TransCellAssay as TCA
import os
import os.path
import logging
import pandas as pd
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

DEBUG = True

#################
## input file col name
Col_PlateIDBarcode = 'PlateId/Barcode'
Col_PlateName = 'Plate Name'
Col_PlateNumber = 'PlateNumber'
Col_Well = 'Well'
Col_CP_PlateName = 'Metadata_Plate'
Col_CP_Well = 'Metadata_Well'
Col_nrows = 'NumberOfRows'
Col_ncol = 'NumberOfColumns'
## Input file name
InputCell = 'Cell.csv'
InputWell = 'Well.csv'
InputPlate = 'Plate.csv'
##col to skip
Skip_FormatPlaque = ['PlateNumber', 'Status', 'Zposition', 'Row', 'Column', 'WellId']
## format plaque
KnowProblematicChanName = {"MEAN_NeuriteMaxLengthWithoutBranchesCh2": "MEAN_NMLWHBC2"}
#################

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

        self.master.title('TCA Analysis App')

        tkinter.Button(self.master, text='CSV File Formatter', command=self.CSVFFFrame).pack(padx=10, pady=5, fill=BOTH)
        tkinter.Button(self.master, text='Format plaque', command=self.FormatPlaqueFrame).pack(padx=10, pady=5,
                                                                                               fill=BOTH)
        tkinter.Button(self.master, text='Plate Analyse', command=self.AnalyseFrame).pack(padx=10, pady=5, fill=BOTH)
        tkinter.Button(self.master, text='BATCH mode', command=self.BatchModeFrame).pack(padx=10, pady=5, fill=BOTH)
        tkinter.Button(self.master, text='EXIT APP', command=self.master.quit, fg="red").pack(padx=10, pady=5,
                                                                                              fill=BOTH)

        self.DirPath = None
        self.FilePathToOpen = None

        self.PlateToAnalyse = None

    # FUNCTION FOR MAIN TASKS

    def CSVFFFrame(self):
        window = Toplevel(self)
        tkinter.Button(window, text="Browse Directory", command=self.load_dir).pack(padx=10, pady=10, fill=BOTH)

        # remove or not useless col
        self.RemoveCol = IntVar()
        Checkbutton(window, text="Remove Useless Columns", variable=self.RemoveCol).pack(padx=5, pady=5, fill=BOTH)
        self.RemoveCol.set(1)

        # remove or not Nan in file, can be dangerous regarding your data
        self.RemoveNan = IntVar()
        Checkbutton(window, text="Remove NaN values", variable=self.RemoveNan).pack(padx=5, pady=5, fill=BOTH)
        self.RemoveNan.set(0)

        self.ReplaceNan = IntVar()
        Checkbutton(window, text="Replace NaN values by 0", variable=self.ReplaceNan).pack(padx=5, pady=5, fill=BOTH)
        self.ReplaceNan.set(0)

        self.Cellprofilerinput = IntVar()
        Checkbutton(window, text="CellProfiler input data", variable=self.Cellprofilerinput).pack(padx=5, pady=5, fill=BOTH)
        self.Cellprofilerinput.set(0)

        Label(window, text="Which csv file use").pack()

        self.CSV_Target = StringVar()
        Combobox(window, textvariable=self.CSV_Target, values=(InputWell, InputCell), state='readonly').pack(padx=10,
                                                                                                               pady=10,
                                                                                                               fill=BOTH)
        self.CSV_Target.set('Cell.csv')

        Label(window, text="Which name to use").pack()

        self.CSV_OutputName = StringVar()
        Combobox(window, textvariable=self.CSV_OutputName, values=(Col_PlateIDBarcode, Col_PlateName, 'Both'),
                 state='readonly').pack(padx=10, pady=10, fill=BOTH)
        self.CSV_OutputName.set('Both')

        tkinter.Button(window, text="Do CSV file Formatting", command=self.__DoCSVFile, fg="red").pack(padx=10, pady=10,
                                                                                                       fill=BOTH)

    def FormatPlaqueFrame(self):
        window = Toplevel(self)
        tkinter.Button(window, text="Browse Directory", command=self.load_dir).pack(padx=10, pady=10, fill=BOTH)

        Label(window, text="Which name to use").pack()

        self.FP_OutputName = StringVar()
        Combobox(window, textvariable=self.FP_OutputName, values=(Col_PlateIDBarcode, Col_PlateName, 'Both'),
                 state='readonly').pack(padx=10, pady=10, fill=BOTH)
        self.FP_OutputName.set('Both')

        tkinter.Button(window, text="Do Format Plaque", command=self.__DoFormatPlaque, fg="red").pack(padx=10, pady=10,
                                                                                                      fill=BOTH)

    def BatchModeFrame(self):
        window = Toplevel(self)

        tkinter.Label(window, text="Input Plate Name").grid(row=1, column=0)
        tkinter.Label(window, text="XXX{0}.{1}.csv").grid(row=1, column=2)

        tkinter.Label(window, text="PlateMap Name").grid(row=2, column=0)
        tkinter.Label(window, text="PP_{0}.csv or PP.csv").grid(row=2, column=2)

        tkinter.Label(window, text="N of plate").grid(row=3, column=0)
        tkinter.Label(window, text="Number of source plate").grid(row=3, column=2)

        tkinter.Label(window, text="N of replica").grid(row=4, column=0)
        tkinter.Label(window, text="Number of replica for each source plate").grid(row=4, column=2)

        tkinter.Label(window, text="Neg Ctrl").grid(row=5, column=0)
        tkinter.Label(window, text="Name of neg reference in platenmap").grid(row=5, column=2)

        tkinter.Label(window, text="Channels").grid(row=6, column=0)
        tkinter.Label(window, text="Which channels to analyse (multiple is possible)").grid(row=6, column=2)

        tkinter.Label(window, text="Threshold Value").grid(row=7, column=0)
        tkinter.Label(window, text="Threshold Value for positive cells").grid(row=7, column=2)

        self.BatchInPlateName = StringVar()
        self.BatchPlateMapName = StringVar()
        self.BatchNPlate = StringVar()
        self.BatchNRep = StringVar()
        self.BatchNegCtrl = StringVar()
        self.BatchChnVal = StringVar()
        self.BatchThrsVal = StringVar()
        tkinter.Entry(window, textvariable=self.BatchInPlateName).grid(row=1, column=1)
        tkinter.Entry(window, textvariable=self.BatchPlateMapName).grid(row=2, column=1)
        tkinter.Entry(window, textvariable=self.BatchNPlate).grid(row=3, column=1)
        tkinter.Entry(window, textvariable=self.BatchNRep).grid(row=4, column=1)
        tkinter.Entry(window, textvariable=self.BatchNegCtrl).grid(row=5, column=1)
        tkinter.Entry(window, textvariable=self.BatchChnVal).grid(row=6, column=1)
        tkinter.Entry(window, textvariable=self.BatchThrsVal).grid(row=7, column=1)

        tkinter.Label(window, text="Threshold type").grid(row=8, column=0)
        self.BatchThrsType = StringVar()
        Combobox(window, textvariable=self.BatchThrsType, values=('Percent', 'value'), state='readonly').grid(row=8,
                                                                                                              column=1)
        self.BatchThrsType.set('Percent')

        self.BatchUseCellCount = IntVar()
        Checkbutton(window, text="Use Cells count for analysis", variable=self.BatchUseCellCount).grid(row=9, column=0)
        self.BatchUseCellCount.set(0)

        tkinter.Button(window, text="Set Directory", command=self.load_dir).grid(row=10, column=1)

        self.Batchlog2Norm = IntVar()
        Checkbutton(window, text="Apply log2 transformation", variable=self.Batchlog2Norm).grid(row=11, column=0)
        self.Batchlog2Norm.set(0)

        tkinter.Label(window, text="Data normalization").grid(row=12, column=0)
        self.BatchdataNorm = StringVar()
        Combobox(window, textvariable=self.BatchdataNorm, values=("", "Zscore", "RobustZscore", "PercentOfSample",
                                                                  "RobustPercentOfSample", "PercentOfControl",
                                                                  "RobustPercentOfControl"),
                 state='readonly').grid(row=12, column=1)
        self.BatchdataNorm.set("")

        tkinter.Label(window, text="Side Effect normalization").grid(row=13, column=0)
        self.BatchSideEffectNorm = StringVar()
        Combobox(window, textvariable=self.BatchSideEffectNorm,
                 values=("", "Bscore", "BZscore", "PMP", "MEA", "Lowess", "Polynomial"),
                 state='readonly').grid(row=13, column=1)
        self.BatchSideEffectNorm.set("")

        tkinter.Label(window, text="Mean and SD choice").grid(row=14, column=0)
        self.BatchMeanSD = StringVar()
        tkinter.Entry(window, textvariable=self.BatchMeanSD).grid(row=14, column=1)

        tkinter.Label(window, text="Pos ctrl").grid(row=15, column=0)
        tkinter.Label(window, text="If you want to get the QC output").grid(row=15, column=2)
        self.BatchPosqc = StringVar()
        tkinter.Entry(window, textvariable=self.BatchPosqc).grid(row=15, column=1)

        self.Batchqcnormdata = IntVar()
        Checkbutton(window, text="Use normalized data for QC", variable=self.Batchqcnormdata).grid(row=15, column=4)
        self.Batchqcnormdata.set(0)

        self.BatchScoring = IntVar()
        Checkbutton(window, text="Scoring", variable=self.BatchScoring).grid(row=16, column=1)
        self.BatchScoring.set(0)

        tkinter.Button(window, text="GO Batch Analysis", command=self._DoBatchAnalyse).grid(row=17, column=1)

    def AnalyseFrame(self):
        window = Toplevel(self)

        menubar = tkinter.Menu(window)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Create New Source Plate", command=self.__init_plate)
        filemenu.add_command(label="Add data file/replica", command=self.__add_replica)
        filemenu.add_command(label="Add platemap file", command=self.__add_platemap)
        filemenu.add_separator()
        filemenu.add_command(label="Print Plate Status", command=self.showPlate)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=window.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tkinter.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Remove replica", command=self.__remove_replica)
        editmenu.add_command(label="Remove PlateMap", command=self.__remove_platemap)
        editmenu.add_command(label="Edit PlateName", command=self.__edit_plate)
        menubar.add_cascade(label="Edit", menu=editmenu)

        normmenu = tkinter.Menu(menubar, tearoff=0)
        normmenu.add_command(label="Single Cell data Normalization", command=self.__dataNorm)
        normmenu.add_command(label="Size effect Normalization", command=self.__SizeEffectNorm)
        menubar.add_cascade(label="Normalization", menu=normmenu)

        graphmenu = tkinter.Menu(menubar, tearoff=0)
        graphmenu.add_command(label="Plate Heatmap", command=self.__HeatMap)
        graphmenu.add_command(label="Value density KDE", command=self.__DensityKDE)
        graphmenu.add_command(label="Value distribution", command=self.__WellsDistribution)
        graphmenu.add_command(label="Value histogramme", command=self.__Histogramme)
        menubar.add_cascade(label="Graph", menu=graphmenu)

        qcmenu = tkinter.Menu(menubar, tearoff=0)
        qcmenu.add_command(label="Neg/Pos", command=self.__qc)
        qcmenu.add_command(label="Wells", command=lambda: print("Do nothing"))
        menubar.add_cascade(label="QC", menu=qcmenu)

        analysemenu = tkinter.Menu(menubar, tearoff=0)
        analysemenu.add_command(label="Do Analyse", command=self.__Analyse)
        analysemenu.add_command(label="Do CellsCount", command=self.__cellsCount)
        analysemenu.add_command(label="Do Scoring", command=self.__Scoring)
        menubar.add_cascade(label="Analyse", menu=analysemenu)

        window.config(menu=menubar)

        tkinter.Label(window, text="Neg Ctrl").grid(row=1, column=0)
        tkinter.Label(window, text="Format in A1 H12 for ex.").grid(row=1, column=3)
        tkinter.Label(window, text="Channel").grid(row=2, column=0)
        tkinter.Label(window, text="Can be multiple but the first is prior").grid(row=2, column=3)
        tkinter.Label(window, text="Threshold type").grid(row=3, column=0)
        tkinter.Label(window, text="Threshold Value").grid(row=4, column=0)

        self.NegCtrl = StringVar()
        self.ChnVal = StringVar()
        self.ThrsVal = StringVar()
        tkinter.Entry(window, textvariable=self.NegCtrl).grid(row=1, column=1)
        tkinter.Entry(window, textvariable=self.ChnVal).grid(row=2, column=1)
        tkinter.Entry(window, textvariable=self.ThrsVal).grid(row=4, column=1)

        self.threshold_type = StringVar()
        Combobox(window, textvariable=self.threshold_type, values=('Percent', 'value'), state='readonly').grid(row=3,
                                                                                                               column=1)
        self.threshold_type.set('Percent')

    # function to open dir and file

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
        logging.debug('Save file location choosen : {}'.format(self.SaveFilePath))

    # FUNCTION THAT PERFORM ACTUALLY SOMETHING

    def __DoFormatPlaque(self):
        """
        Function that perform ''format plaque'' on selected directory
        """
        if self.DirPath is None:
            tkinter.messagebox.showerror(message="Empty directory, choose one")
            self.load_dir()

        logging.info("Start processing")
        for root, dirs, filenames in os.walk(self.DirPath):
            if "Plate.csv" in filenames:
                plateId = pd.read_csv(os.path.join(root, InputPlate))

                # # read data
                inputdata = pd.read_csv(os.path.join(root, InputWell))

                for i in range(len(plateId)):
                    if self.FP_OutputName.get() == 'PlateID/Barcode':
                        OutputName = plateId[Col_PlateIDBarcode][i]
                    elif self.FP_OutputName.get() == 'Plate Name':
                        OutputName = plateId[Col_PlateName][i]
                    else:
                        OutputName = "{0}-{1}".format(plateId[Col_PlateIDBarcode][i], plateId[Col_PlateName][i])
                    platenumber = plateId[Col_PlateNumber][i]

                    nbrow = plateId[Col_nrows][i]
                    nbcol = plateId[Col_ncol][i]

                    logging.info('Work on {}'.format(OutputName))

                    data = TCA.CSV()
                    data.dataframe = inputdata[inputdata[Col_PlateNumber] == platenumber].reset_index(drop=True)
                    data.is1Datawell = True

                    skip = Skip_FormatPlaque

                    # # get all channel (columns)
                    all_col = data.get_col()

                    # # create new excel file and worksheet
                    filename = os.path.join(self.DirPath, OutputName + ".xlsx")
                    workbook = pd.ExcelWriter(filename)

                    for chan in all_col:
                        if chan in skip:
                            continue

                        logging.debug('Work on {} channel'.format(chan))

                        if data.dataframe[chan].dtypes == 'object':
                            data.dataframe[chan] = data.dataframe[chan].str.replace(",", ".")

                        array = data.df_to_array(chan, size=nbrow*nbcol)

                        # # if chan is to long, cut it
                        if len(str(chan)) >= 30:
                            if str(chan) in KnowProblematicChanName:
                                Chan = KnowProblematicChanName[str(chan)]
                                logging.warning('Channel {0} is writed as {1}'.format(chan, Chan))
                            else:
                                Chan = ''.join(x for x in str(chan) if not x.islower())
                                logging.warning('Channel {0} is writed as {1}'.format(chan, Chan))
                        else:
                            Chan = str(chan)

                        pd.DataFrame(array).to_excel(workbook, Chan)

                    workbook.save()
                    logging.info('Finish {}'.format(OutputName))

    def __DoCSVFile(self):
        """
        Function that perform conversion to good csv format from output of HCS studio
        """
        if self.DirPath is None:
            tkinter.messagebox.showerror(message="Empty directory, choose one")
            self.load_dir()

        if self.Cellprofilerinput.get():
            lstfile = [each for each in os.listdir(self.DirPath) if each.endswith(InputCell)]

            for inFile in lstfile:
                file = TCA.CSV()
                file.load(os.path.join(self.DirPath, inFile))

                file.rename_col(colname=Col_CP_PlateName, newcolname=Col_PlateName)
                file.rename_col(colname=Col_CP_Well, newcolname=Col_Well)
                file.format_well_format()

                uniquePlate = file.dataframe[Col_PlateName].unique()

                for plate in uniquePlate:
                    df = file.dataframe[file.dataframe[Col_PlateName] == plate].reset_index()
                    df.to_csv(os.path.join(self.DirPath, plate+'.csv'))


        else:
            for root, dirs, filenames in os.walk(self.DirPath):
                if InputPlate in filenames:
                    plateId = pd.read_csv(os.path.join(root, InputPlate))

                    # # read data
                    inputdata = pd.read_csv(os.path.join(root, self.CSV_Target.get()))

                    for i in range(len(plateId)):
                        if self.CSV_OutputName.get() == 'PlateID/Barcode':
                            OutputName = plateId[Col_PlateIDBarcode][i]
                        elif self.CSV_OutputName.get() == 'Plate Name':
                            OutputName = plateId[Col_PlateName][i]
                        else:
                            OutputName = "{0}-{1}".format(plateId[Col_PlateIDBarcode][i], plateId[Col_PlateName][i])
                        platenumber = plateId[Col_PlateNumber][0]

                        #  # create well in good format
                        file = TCA.CSV()
                        file.dataframe = inputdata[inputdata[Col_PlateNumber] == platenumber]
                        file.format_well_format()
                        try:
                            if self.RemoveCol.get():
                                file.remove_col()
                            if self.RemoveNan.get():
                                file.remove_nan()
                            if self.ReplaceNan.get():
                                file.replace_nan()
                        except:
                            pass
                        file.write_raw_data(path=self.DirPath, name=OutputName)

    def __init_plate(self):
        """
        Init plate
        """
        window = Toplevel(self)

        tkinter.Label(window, text="Plate name").grid(row=1, column=0)
        self.PlateName = StringVar()
        tkinter.Entry(window, textvariable=self.PlateName).grid(row=1, column=1)

        tkinter.Label(window, text="Plate size").grid(row=2, column=0)
        self.plate_size = StringVar()
        Combobox(window, textvariable=self.plate_size, values=('96', '384'), state='readonly').grid(row=2, column=1)
        self.plate_size.set('96')

        tkinter.Button(window, text='Create Plate', command=self.__create_plate).grid(row=3, column=0)
        # tkinter.Button(window, text='add file', command=self.selectFiles).grid(row=3, column=0)

    def __create_plate(self):
        """
        create a plate object
        """
        self.PlateToAnalyse = TCA.Plate(name=self.PlateName.get(),
                                        platemap=TCA.Core.PlateMap(size=self.plate_size.get()))

    def __remove_platemap(self):
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)
        tkinter.Label(window, text="New platemap size").grid(row=0, column=0)
        newplatemapsize = StringVar()
        Combobox(window, textvariable=newplatemapsize, values=('96', '384'), state='readonly').grid(row=0, column=1)
        newplatemapsize.set('96')

        tkinter.Button(window, text='New platemap',
                       command=lambda: self.PlateToAnalyse.add_platemap(
                           TCA.PlateMap(size=int(newplatemapsize.get())))).grid(row=2, column=0)

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
        tkinter.Button(window, text='New platename',
                       command=lambda: self.PlateToAnalyse.set_name(self.PlateName.get())).grid(row=2, column=0)

    def __add_platemap(self):
        """
        Function for adding a platemap to plate
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)
        tkinter.Button(window, text='Browse file', command=self.load_file).grid(row=1, column=0)
        tkinter.Button(window, text='Add file/replica to plate',
                       command=lambda: self.PlateToAnalyse.add_platemap(TCA.PlateMap(fpath=self.FilePathToOpen))).grid(
            row=2, column=0)

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
        tkinter.Button(window, text='Add file/replica to plate', command=lambda: self.PlateToAnalyse.add_replica(
            TCA.Replica(name=repname.get(), fpath=self.FilePathToOpen))).grid(row=3, column=0)

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
        tkinter.Button(window, text='Remove replica',
                       command=lambda: self.PlateToAnalyse.remove_replica(repname.get())).grid(row=2, column=0)

    def __Analyse(self):
        """
        Do analyse on current plate
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)

        NegRef = self.NegCtrl.get()
        logging.debug("Negative reference : {}".format(NegRef))
        if NegRef == '':
            NegRef = None

        if NegRef is not None:
            NegRef = NegRef.split()
            for i in NegRef:
                self.PlateToAnalyse.platemap[i] = "Neg"
            NegRef = "Neg"

        ChanRef = self.ChnVal.get()
        logging.debug("Channel analysed : {}".format(ChanRef))
        if ChanRef == '':
            ChanRef = None
        else:
            ChanRef = [ChanRef]

        noposcell = False
        thresRef = self.ThrsVal.get()
        logging.debug("Threshold used : {}".format(thresRef))
        if thresRef == '':
            thresRef = None
            noposcell = True
        else:
            thresRef = int(thresRef)

        if self.threshold_type.get() == 'Percent':
            thresTypePercent = True
            thresTypeFixedVal = False
        else:
            thresTypePercent = False
            thresTypeFixedVal = True

        if noposcell is False:
            self.CurrentResToSave, thres = TCA.PlateChannelsAnalysis(self.PlateToAnalyse,
                                                                     channels=ChanRef,
                                                                     neg=NegRef,
                                                                     threshold=thresRef,
                                                                     percent=thresTypePercent,
                                                                     fixed_threshold=thresTypeFixedVal,
                                                                     clean=False,
                                                                     noposcell=noposcell,
                                                                     multiIndexDF=True)
            logging.info("Threshold value : {}".format(thres))

        else:
            self.CurrentResToSave = TCA.PlateChannelsAnalysis(self.PlateToAnalyse,
                                                              channels=ChanRef,
                                                              neg=NegRef,
                                                              threshold=thresRef,
                                                              percent=thresTypePercent,
                                                              fixed_threshold=thresTypeFixedVal,
                                                              clean=False,
                                                              noposcell=noposcell,
                                                              multiIndexDF=True)

        self.__AnalyseData = self.CurrentResToSave

        tkinter.Button(window, text="Select where to save", fg="red", command=self.selectFileToSave).pack(padx=10,
                                                                                                          pady=10)
        tkinter.Button(window, text="Save analyse results", fg="red", command=self.__saveFile).pack(padx=10, pady=10)

    def __Scoring(self):
        """
        Do analyse on current plate
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)

        NegRef = self.NegCtrl.get()
        if NegRef is not None:
            NegRef = NegRef.split()
            for i in NegRef:
                self.PlateToAnalyse.platemap[i] = "Neg"
            NegRef = "Neg"

        ChanRef = self.ChnVal.get()
        logging.debug("Channel analysed : {}".format(ChanRef))
        if ChanRef == '':
            logging.error("Must have a channel")
        else:
            ChanRef = ChanRef

        self.CurrentResToSave = TCA.ScoringPlate(self.PlateToAnalyse, neg=NegRef, channel=ChanRef)
        tkinter.Button(window, text="Save scoring results", fg="red", command=self.__saveFile).pack(padx=10, pady=10)

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
        self.__CellsCountData = self.CurrentResToSave

        tkinter.Button(window, text="Select where to save", fg="red", command=self.selectFileToSave).pack(padx=10,
                                                                                                          pady=10)
        tkinter.Button(window, text="Save cellscount", fg="red", command=self.__saveFile).pack(padx=10, pady=10)

    def __saveFile(self):
        """
        Write csv file
        """
        self.selectFileToSave()
        # tkinter.messagebox.showerror(message="No selected file name")
        # return
        self.CurrentResToSave.to_csv(self.SaveFilePath, header=True, index=False)

    def __dataNorm(self):
        """
        single cell data norm
        """
        if not DEBUG:
            if self.PlateToAnalyse is None:
                tkinter.messagebox.showerror(message="No existing Plate, create one")
                return
        window = Toplevel(self)

        tkinter.Label(window, text="Data normalization").grid(row=1, column=0)

        self.dataNorm = StringVar()
        Combobox(window, textvariable=self.dataNorm, values=("Zscore", "RobustZscore", "PercentOfSample",
                                                             "RobustPercentOfSample", "PercentOfControl",
                                                             "RobustPercentOfControl"), state='readonly').grid(
            row=1, column=1)
        self.dataNorm.set('Zscore')

        self.log2Norm = IntVar()
        Checkbutton(window, text="Apply log2 transformation", variable=self.log2Norm).grid(row=2, column=0)
        self.log2Norm.set(0)

        tkinter.Label(window, text="Neg Ctrl").grid(row=3, column=0)
        tkinter.Label(window, text="Channel").grid(row=4, column=0)

        self.NormNeg = StringVar()
        self.NormPos = StringVar()
        self.NormChan = StringVar()
        tkinter.Entry(window, textvariable=self.NormNeg).grid(row=3, column=1)
        tkinter.Entry(window, textvariable=self.NormChan).grid(row=4, column=1)

        tkinter.Button(window, text='Apply data norm',
                       command=lambda: self.PlateToAnalyse.normalization_channels(channels=[self.NormChan.get()],
                                                                                  method=self.dataNorm.get(),
                                                                                  log_t=self.log2Norm.get(),
                                                                                  neg=self.NormNeg.get()),
                       fg="red").grid(row=1, column=2)

    def __SizeEffectNorm(self):
        """
        single cell data norm
        """
        if not DEBUG:
            if self.PlateToAnalyse is None:
                tkinter.messagebox.showerror(message="No existing Plate, create one")
                return
        window = Toplevel(self)

        tkinter.Label(window, text="Channel").grid(row=0, column=0)
        self.SideNormChan = StringVar()
        tkinter.Entry(window, textvariable=self.SideNormChan).grid(row=0, column=1)

        tkinter.Label(window, text="Side Effect normalization").grid(row=1, column=0)
        self.SideNorm = StringVar()
        Combobox(window, textvariable=self.SideNorm, values=('Bscore', 'BZscore', 'PMP', 'MEA', 'Lowess', 'Polynomial'),
                 state='readonly').grid(row=1, column=1)
        self.SideNorm.set('Lowess')

        tkinter.Button(window, text='Apply data norm',
                       command=lambda: self.PlateToAnalyse.systematic_error_correction(algorithm=self.SideNorm.get()),
                       fg="red").grid(row=1, column=2)

    def __qc(self):
        if not DEBUG:
            if self.PlateToAnalyse is None:
                tkinter.messagebox.showerror(message="No existing Plate, create one")
                return
        window = Toplevel(self)

        tkinter.Label(window, text="Channel").grid(row=0, column=0)
        self.QCchan = StringVar()
        tkinter.Entry(window, textvariable=self.QCchan).grid(row=0, column=1)

        tkinter.Label(window, text="Neg ctrl").grid(row=1, column=0)
        self.QCneg = StringVar()
        tkinter.Entry(window, textvariable=self.QCneg).grid(row=1, column=1)

        tkinter.Label(window, text="Pos ctrl").grid(row=2, column=0)
        self.QCpos = StringVar()
        tkinter.Entry(window, textvariable=self.QCpos).grid(row=2, column=1)

        self.QCnormdata = IntVar()
        Checkbutton(window, text="Use normalized data", variable=self.QCnormdata).grid(row=3, column=0)
        self.QCnormdata.set(0)

        tkinter.Button(window, text='Launch QC',
                       command=self.__do_QC,
                       fg="red").grid(row=4, column=0)

    def __do_QC(self):
        if not DEBUG:
            if self.PlateToAnalyse is None:
                tkinter.messagebox.showerror(message="No existing Plate, create one")
                return

        qc = TCA.plate_quality_control(self.PlateToAnalyse,
                                       channel=self.QCchan.get(),
                                       cneg=self.QCneg.get(),
                                       cpos=self.QCpos.get(),
                                       sec_data=bool(self.QCnormdata.get()))
        self.selectFileToSave()

        qc.to_csv(self.SaveFilePath)

    def _DoBatchAnalyse(self):
        DF_BeforeNorm = []
        DF_AfterNorm = []
        thresfile = open(os.path.join(self.DirPath, "ThresholdValue_{}.csv".format(time.asctime())), 'a')
        QCdata = []
        ScoringDataWithoutNorm = []
        ScoringDataWithNorm = []

        for i in range(1, int(self.BatchNPlate.get()) + 1, 1):
            plaque = TCA.Plate(name="Plate nb{}".format(i),
                               platemap=os.path.join(self.DirPath, self.BatchPlateMapName.get().format(i)))

            for j in range(1, int(self.BatchNRep.get()) + 1, 1):
                file = os.path.join(self.DirPath, self.BatchInPlateName.get().format(i, j))
                if os.path.isfile(file):
                    plaque + TCA.Core.Replica(name='Rep' + str(j), fpath=file)
                else:
                    logging.warning("File doesn't exist : {}".format(file))

            if bool(self.BatchUseCellCount.get()):
                plaque.use_count_as_data()

            # channel analysis without norm
            if self.BatchThrsType.get() == 'Percent':
                df, thres = TCA.PlateChannelsAnalysis(plaque,
                                                      channels=self.BatchChnVal.get().split(),
                                                      neg=self.BatchNegCtrl.get(),
                                                      threshold=100 - int(self.BatchThrsVal.get()),
                                                      percent=True)
            else:
                df, thres = TCA.PlateChannelsAnalysis(plaque,
                                                      channels=self.BatchChnVal.get().split(),
                                                      neg=self.BatchNegCtrl.get(),
                                                      threshold=int(self.BatchThrsVal.get()),
                                                      percent=False,
                                                      fixed_threshold=True)

            thresfile.write("{0} @ {1}%: {2}\n".format(plaque.name, int(self.BatchThrsVal.get()), thres))
            DF_BeforeNorm.append(df)

            # scoring results on non-normalized data
            ScoringDataWithoutNorm.append(TCA.ScoringPlate(plaque,
                                                           neg=self.BatchNegCtrl.get().split()[0],
                                                           channel=self.BatchChnVal.get().split()[0],
                                                           data_c=False))

            # Raw data normalization
            if self.BatchdataNorm.get() != "":
                plaque.normalization_channels(channels=self.BatchChnVal.get().split(),
                                              method=self.BatchdataNorm.get(),
                                              neg=self.BatchNegCtrl.get(),
                                              log_t=bool(self.Batchlog2Norm.get()))

            # side effect normalization
            if self.BatchSideEffectNorm.get() != "":
                plaque.apply_systematic_error_correction(algorithm=self.BatchSideEffectNorm.get(),
                                                         apply_down=True,
                                                         max_iterations=10)
            # channel analysis wih norm
            if self.BatchdataNorm.get() or self.BatchSideEffectNorm.get() != "":
                if self.BatchThrsType.get() == 'Percent':
                    df, thres = TCA.PlateChannelsAnalysis(plaque,
                                                          channels=self.BatchChnVal.get().split(),
                                                          neg=self.BatchNegCtrl.get(),
                                                          threshold=100 - int(self.BatchThrsVal.get()),
                                                          percent=True)
                else:
                    df, thres = TCA.PlateChannelsAnalysis(plaque,
                                                          channels=self.BatchChnVal.get().split(),
                                                          neg=self.BatchNegCtrl.get(),
                                                          threshold=int(self.BatchThrsVal.get()),
                                                          percent=False,
                                                          fixed_threshold=True)

                # scoring results on normalized data
                if self.BatchSideEffectNorm.get() == "":
                    plaque.agg_data_from_replica_channel(channel=self.BatchChnVal.get().split()[0], forced_update=True)
                else:
                    ScoringDataWithNorm.append(TCA.ScoringPlate(plaque,
                                                                neg=self.BatchNegCtrl.get().split()[0],
                                                                channel=self.BatchChnVal.get().split()[0],
                                                                data_c=True))

            thresfile.write("{0} Normalized @ {1}%: {2}\n".format(plaque.name, int(self.BatchThrsVal.get()), thres))
            DF_AfterNorm.append(df)

            if self.BatchPosqc.get() != "":
                qc = TCA.plate_quality_control(plate=plaque,
                                               channel=self.BatchChnVal.get().split()[0],
                                               cneg=self.BatchNegCtrl.get(),
                                               cpos=self.BatchPosqc.get(),
                                               sec_data=bool(self.Batchqcnormdata.get()))
                QCdata.append(qc)

        beforenorm = pd.concat(DF_BeforeNorm)
        beforenorm.to_csv(
            os.path.join(self.DirPath, "Resultat_@{0}.csv".format(int(self.BatchThrsVal.get()))),
            index=False, header=True)

        if self.BatchPosqc.get() != "":
            pd.concat(QCdata).to_csv(os.path.join(self.DirPath, "QC.csv"), index=False, header=True)

        if self.BatchMeanSD.get() != "":
            x = beforenorm[beforenorm.PlateMap.isin(self.BatchMeanSD.get().split())]
            x.groupby(by=['PlateName', 'PlateMap']).mean().to_csv(
                os.path.join(self.DirPath, "Resultat_@{0}_Mean.csv".format(int(self.BatchThrsVal.get()))),
                index=False, header=True)
            x.groupby(by=['PlateName', 'PlateMap']).std().to_csv(
                os.path.join(self.DirPath, "Resultat_@{0}_Std.csv".format(int(self.BatchThrsVal.get()))),
                index=False, header=True)

        if self.BatchdataNorm.get() or self.BatchSideEffectNorm.get() != "":
            afternorm = pd.concat(DF_AfterNorm)
            afternorm.to_csv(
                os.path.join(self.DirPath, "Resultat_Normalized_@{0}.csv".format(int(self.BatchThrsVal.get()))),
                index=False, header=True)

            if self.BatchMeanSD.get() != "":
                x = afternorm[afternorm.PlateMap.isin(self.BatchMeanSD.get().split())]
                x.groupby(by=['PlateName', 'PlateMap']).mean().to_csv(
                    os.path.join(self.DirPath,
                                 "Resultat_Normalized_@{0}_Mean.csv".format(int(self.BatchThrsVal.get()))),
                    index=False, header=True)
                x.groupby(by=['PlateName', 'PlateMap']).std().to_csv(
                    os.path.join(self.DirPath, "Resultat_Normalized_@{0}_Std.csv".format(int(self.BatchThrsVal.get()))),
                    index=False, header=True)
        pd.concat(ScoringDataWithoutNorm).to_csv(os.path.join(self.DirPath, "ScoringWithoutNorm.csv"),
                                                 index=False, header=True)
        if self.BatchdataNorm.get() or self.BatchSideEffectNorm.get() != "":
            pd.concat(ScoringDataWithNorm).to_csv(os.path.join(self.DirPath, "ScoringWithNorm.csv"),
                                                  index=False, header=True)
        thresfile.close()

    # FUNCTION FOR GRAPHIC OUTPUT

    def __HeatMap(self):
        """
        Perform heatmap
        """
        if not DEBUG:
            if self.PlateToAnalyse is None:
                tkinter.messagebox.showerror(message="No existing Plate, create one")
                return
        window = Toplevel(self)

        tkinter.Label(window, text="Feature to plot").grid(row=1, column=0)

        self.heatmapToplot = StringVar()
        Combobox(window, textvariable=self.heatmapToplot, values=("CellsCount", "Given Channel"),
                 state='readonly').grid(row=1, column=1)
        self.heatmapToplot.set('CellsCount')

        tkinter.Label(window, text="Channel to plot").grid(row=2, column=0)
        self.heatmapChanneltoplot = StringVar()
        tkinter.Entry(window, textvariable=self.heatmapChanneltoplot).grid(row=2, column=1)

        logging.debug("Heatmap plot")

        tkinter.Button(window, text='Do Heatmap', command=self.__DoHeatmap, fg="red").grid(row=3, column=0)

    def __DoHeatmap(self):
        """
        Do heatmap
        """
        if self.heatmapToplot.get() == 'CellsCount':
            self.PlateToAnalyse.use_count_as_data()
        else:
            self.PlateToAnalyse.agg_data_from_replica_channel(channel=self.heatmapChanneltoplot.get(),
                                                              forced_update=True)

        TCA.HeatMapPlate(self.PlateToAnalyse)

    def __DensityKDE(self):
        """
        Density or KDE plot
        """
        if not DEBUG:
            if self.PlateToAnalyse is None:
                tkinter.messagebox.showerror(message="No existing Plate, create one")
                return
        window = Toplevel(self)

        tkinter.Label(window, text="Channel").grid(row=0, column=0)
        self.KdeChan = StringVar()
        tkinter.Entry(window, textvariable=self.KdeChan).grid(row=0, column=1)

        tkinter.Label(window, text="Wells").grid(row=1, column=0)
        self.KdeWells = StringVar()
        tkinter.Entry(window, textvariable=self.KdeWells).grid(row=1, column=1)

        logging.debug("Density plot")

        tkinter.Button(window, text='Do Density',
                       command=lambda: TCA.PlateWellsDistribution(self.PlateToAnalyse,
                                                                  wells=self.KdeWells.get().split(),
                                                                  channel=self.KdeChan.get()),
                       fg="red").grid(row=3, column=0)

    def __WellsDistribution(self):
        """
        Wells distribution plot
        """
        if not DEBUG:
            if self.PlateToAnalyse is None:
                tkinter.messagebox.showerror(message="No existing Plate, create one")
                return
        window = Toplevel(self)

        tkinter.Label(window, text="Channel").grid(row=0, column=0)
        self.WellsDisChan = StringVar()
        tkinter.Entry(window, textvariable=self.WellsDisChan).grid(row=0, column=1)

        tkinter.Label(window, text="Wells").grid(row=1, column=0)
        self.WellsDisWells = StringVar()
        tkinter.Entry(window, textvariable=self.WellsDisWells).grid(row=1, column=1)

        self.WellsDisPool = IntVar()
        Checkbutton(window, text="Pool replica", variable=self.WellsDisPool).grid(row=2, column=0)
        self.WellsDisPool.set(0)

        logging.debug("Wells distribution plot ")

        tkinter.Button(window, text='Do Wells distribution',
                       command=lambda: TCA.PlateWellsSorted(self.PlateToAnalyse,
                                                            wells=self.WellsDisWells.get().split(),
                                                            channel=self.WellsDisChan.get(),
                                                            pool=bool(self.WellsDisPool.get())),
                       fg="red").grid(row=3, column=0)

    def __Histogramme(self):
        if not DEBUG:
            if self.PlateToAnalyse is None:
                tkinter.messagebox.showerror(message="No existing Plate, create one")
                return
        window = Toplevel(self)
        tkinter.Label(window, text="Channel").grid(row=0, column=0)
        self.WellsHistChan = StringVar()
        tkinter.Entry(window, textvariable=self.WellsHistChan).grid(row=0, column=1)

        tkinter.Label(window, text="Wells").grid(row=1, column=0)
        self.WellsHistWells = StringVar()
        tkinter.Entry(window, textvariable=self.WellsHistWells).grid(row=1, column=1)

        tkinter.Label(window, text="bins").grid(row=2, column=0)
        self.WellsHistbins = StringVar()
        self.WellsHistbins.set("100")
        tkinter.Entry(window, textvariable=self.WellsHistbins).grid(row=2, column=1)

        tkinter.Button(window, text='Do Wells distribution',
                       command=lambda: TCA.PlateWellsDistribution(self.PlateToAnalyse,
                                                                  kind='hist',
                                                                  wells=self.WellsHistWells.get().split(),
                                                                  channel=self.WellsHistChan.get(),
                                                                  bins=int(self.WellsHistbins.get())),
                       fg="red").grid(row=3, column=0)

    def showPlate(self):
        print(self.PlateToAnalyse)

if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("300x200")
    view = MainAppFrame(root)
    root.mainloop()

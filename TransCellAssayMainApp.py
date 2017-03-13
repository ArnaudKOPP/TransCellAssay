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
import string

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2017 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

DEBUG = True

#################
##  input file col name
Col_PlateIDBarcode = 'PlateId/Barcode'
Col_PlateName = 'Plate Name'
Col_PlateNumber = 'PlateNumber'
Col_Well = 'Well'
Col_nrows = 'NumberOfRows'
Col_ncol = 'NumberOfColumns'
# special for cellprofiler
Col_CP_PlateName = 'Metadata_Plate'
Col_CP_Well = 'Metadata_Well'
# #  Input file name of hcstudio export
InputCell = 'Cell.csv'
InputWell = 'Well.csv'
InputField = 'Field.csv'
InputPlate = 'Plate.csv'
# # col to skip
Skip_FormatPlaque = ['PlateNumber', 'Status', 'Zposition', 'WellId']
# # format plaque
KnowProblematicChanName = {"MEAN_NeuriteMaxLengthWithoutBranchesCh2": "MEAN_NMLWHBC2"}


#################


def chk_empty(input):
    assert isinstance(input, str)
    if len(input) == 0:
        return None
    else:
        return input


class LogFile(object):
    def __init__(self, path, name="LOG"):
        self.file = open(os.path.join(path, '{}.txt'.format(name)), 'w')

    def add(self, to_write):
        self.file.write("{0} \n".format(to_write))

    def close(self):
        self.file.close()


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
        self.PlateToAnalyseAddedPM = False

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
        Checkbutton(window, text="CellProfiler input data", variable=self.Cellprofilerinput).pack(padx=5, pady=5,
                                                                                                  fill=BOTH)
        self.Cellprofilerinput.set(0)

        Label(window, text="Which csv file use").pack()

        self.CSV_Target = StringVar()
        Combobox(window, textvariable=self.CSV_Target, values=(InputWell, InputCell, InputField),
                 state='readonly').pack(padx=10,
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

        tkinter.Button(window, text="Set Input Directory", command=self.load_dir).grid(row=1, column=3)

        tkinter.Label(window, text="Input Plate Name").grid(row=1, column=0)
        tkinter.Label(window, text="XXX{0}.{1}.csv").grid(row=1, column=2)

        tkinter.Label(window, text="PlateMap Name").grid(row=2, column=0)
        tkinter.Label(window, text="PP_{0}.csv or PP.csv").grid(row=2, column=2)

        tkinter.Label(window, text="N of plate").grid(row=3, column=0)
        tkinter.Label(window, text="Number of source plate").grid(row=3, column=2)

        tkinter.Label(window, text="N of replica").grid(row=4, column=0)
        tkinter.Label(window, text="Number of replica for each source plate").grid(row=4, column=2)

        tkinter.Label(window, text="Neg Ctrl").grid(row=5, column=0)
        tkinter.Label(window, text="Name of neg reference in platemap").grid(row=5, column=2)

        tkinter.Label(window, text="Pos Ctrl").grid(row=6, column=0)
        tkinter.Label(window, text="Name of pos reference in platemap").grid(row=6, column=2)

        tkinter.Label(window, text="Channels").grid(row=7, column=0)
        tkinter.Label(window, text="Which channels to analyse (multiple is possible)").grid(row=7, column=2)

        tkinter.Label(window, text="Threshold Value").grid(row=8, column=0)
        tkinter.Label(window, text="Threshold Value for positive cells").grid(row=8, column=2)

        self.BatchInPlateName = StringVar()
        self.BatchPlateMapName = StringVar()
        self.BatchNPlate = StringVar()
        self.BatchNRep = StringVar()
        self.BatchNegCtrl = StringVar()
        self.BatchPosCtrl = StringVar()
        self.BatchChan = StringVar()
        self.BatchThrsVal = StringVar()
        tkinter.Entry(window, textvariable=self.BatchInPlateName).grid(row=1, column=1)
        tkinter.Entry(window, textvariable=self.BatchPlateMapName).grid(row=2, column=1)
        tkinter.Entry(window, textvariable=self.BatchNPlate).grid(row=3, column=1)
        tkinter.Entry(window, textvariable=self.BatchNRep).grid(row=4, column=1)
        tkinter.Entry(window, textvariable=self.BatchNegCtrl).grid(row=5, column=1)
        tkinter.Entry(window, textvariable=self.BatchPosCtrl).grid(row=6, column=1)
        tkinter.Entry(window, textvariable=self.BatchChan).grid(row=7, column=1)
        tkinter.Entry(window, textvariable=self.BatchThrsVal).grid(row=8, column=1)
        tkinter.Label(window, text=" X for single value on all chan or {'chan' : 10} for specified").grid(row=8, column=2)

        tkinter.Label(window, text="Threshold type").grid(row=9, column=0)
        self.BatchThrsType = StringVar()
        Combobox(window, textvariable=self.BatchThrsType, values=('Percent', 'value'), state='readonly').grid(row=9,
                                                                                                              column=1)
        self.BatchThrsType.set('Percent')

        tkinter.Label(window, text="Data normalization").grid(row=10, column=0)
        self.BatchDataNorm = StringVar()
        Combobox(window, textvariable=self.BatchDataNorm, values=("", "Zscore", "RobustZscore", "PercentOfSample",
                                                                  "RobustPercentOfSample", "PercentOfControl",
                                                                  "RobustPercentOfControl",
                                                                  "NormalizedPercentInhibition"),
                 state='readonly').grid(row=10, column=1)
        self.BatchDataNorm.set("")

        tkinter.Label(window, text="Side Effect normalization").grid(row=11, column=0)
        self.BatchSideEffectNorm = StringVar()
        Combobox(window, textvariable=self.BatchSideEffectNorm,
                 values=("", "Bscore", "BZscore", "PMP", "MEA", "Lowess", "Polynomial"),
                 state='readonly').grid(row=11, column=1)
        self.BatchSideEffectNorm.set("")

        tkinter.Label(window, text="Ref for Mean/SD").grid(row=12, column=0)
        self.BatchMeanSD = StringVar()
        tkinter.Entry(window, textvariable=self.BatchMeanSD).grid(row=12, column=1)
        tkinter.Label(window, text="Ref for having mean and SD (separate by space)").grid(row=12, column=2)

        self.BatchQC = IntVar()
        Checkbutton(window, text="QC", variable=self.BatchQC).grid(row=13, column=0)
        self.BatchQC.set(0)
        tkinter.Label(window, text="DO or not QC with Neg and Pos reference").grid(row=13, column=2)

        self.BatchScoring = IntVar()
        Checkbutton(window, text="Scoring", variable=self.BatchScoring).grid(row=14, column=0)
        self.BatchScoring.set(0)
        tkinter.Label(window, text="Do or not scoring").grid(row=14, column=2)

        self.BatchHeatMap = IntVar()
        Checkbutton(window, text="Plate heatmap", variable=self.BatchHeatMap).grid(row=15, column=0)
        self.BatchHeatMap.set(0)
        tkinter.Label(window, text="Plot or not heatmap").grid(row=15, column=2)

        tkinter.Button(window, text="GO Batch Analysis", command=self._DoBatchAnalyse).grid(row=16, column=1)

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
        menubar.add_cascade(label="QC", menu=qcmenu)

        analysemenu = tkinter.Menu(menubar, tearoff=0)
        analysemenu.add_command(label="Do Analyse", command=self.__Analyse)
        analysemenu.add_command(label="Do CellsCount", command=self.__cellsCount)
        analysemenu.add_command(label="Do Scoring", command=self.__Scoring)
        analysemenu.add_command(label="Do Binning", command=self.__Binning)
        menubar.add_cascade(label="Analyse", menu=analysemenu)

        window.config(menu=menubar)

        tkinter.Label(window, text="Neg Ctrl").grid(row=1, column=0)
        tkinter.Label(window, text="Pos Ctrl").grid(row=2, column=0)
        tkinter.Label(window, text="Format in A1 H12 for ex.").grid(row=1, column=2)
        tkinter.Label(window, text="Channel").grid(row=3, column=0)
        tkinter.Label(window, text="Can be multiple but the first is prior").grid(row=3, column=2)
        tkinter.Label(window, text="Threshold type").grid(row=4, column=0)
        tkinter.Label(window, text="Threshold Value").grid(row=5, column=0)
        tkinter.Label(window, text=" X for single value on all chan or {'chan' : 10} for specified").grid(row=5,
                                                                                                          column=2)

        self.NegCtrl = StringVar()
        self.PosCtrl = StringVar()
        self.ChnVal = StringVar()
        self.ThrsVal = StringVar()
        tkinter.Entry(window, textvariable=self.NegCtrl).grid(row=1, column=1)
        tkinter.Entry(window, textvariable=self.PosCtrl).grid(row=2, column=1)
        tkinter.Entry(window, textvariable=self.ChnVal).grid(row=3, column=1)
        tkinter.Entry(window, textvariable=self.ThrsVal).grid(row=5, column=1)

        self.threshold_type = StringVar()
        Combobox(window, textvariable=self.threshold_type, values=('Percent', 'value'), state='readonly').grid(row=4,
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

                        array = data.df_to_array(chan, size=nbrow * nbcol)

                        # # if chan is to long, cut it
                        if len(str(chan)) >= 30:
                            try:
                                if str(chan) in KnowProblematicChanName:
                                    Chan = KnowProblematicChanName[str(chan)]
                                    logging.warning('Channel {0} is writed as {1}'.format(chan, Chan))
                                else:
                                    Chan = ''.join(x for x in str(chan) if not x.islower())
                                    logging.warning('Channel {0} is writed as {1}'.format(chan, Chan))
                            except Exception as e:
                                logging.error('Channel {0} cannot be processed, name to long : {1}'.format(chan, e))
                        else:
                            Chan = str(chan)
                        if (nbrow * nbcol) == 96:
                            df = pd.DataFrame(data=array, index=list(string.ascii_uppercase)[0:8],
                                              columns=[str(x) for x in range(1, 13, 1)])
                        elif (nbrow * nbcol) == 384:
                            df = pd.DataFrame(data=array, index=list(string.ascii_uppercase)[0:16],
                                              columns=[str(x) for x in range(1, 25, 1)])
                        elif (nbrow * nbcol) == 1536:
                            df = pd.DataFrame(data=array,
                                              index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                                                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                                     'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF'],
                                              columns=[str(x) for x in range(1, 49, 1)])
                        df.to_excel(workbook, Chan)

                    workbook.save()
                    logging.info('Finish {}'.format(OutputName))

    def __DoCSVFile(self):
        """
        Function that perform conversion to good csv format from output of HCS studio
        """
        if self.DirPath is None:
            tkinter.messagebox.showerror(message="Empty directory, choose one")
            self.load_dir()

        # ## if cellprofiler output file
        if bool(self.Cellprofilerinput.get()):
            # search all csv file into dir
            lstfile = [each for each in os.listdir(self.DirPath) if each.endswith(InputCell)]

            for inFile in lstfile:
                file = TCA.CSV()
                file.load(os.path.join(self.DirPath, inFile))

                file.rename_col(colname=Col_CP_PlateName, newcolname=Col_PlateName)
                file.rename_col(colname=Col_CP_Well, newcolname=Col_Well)
                file.format_well_format()

                uniquePlate = file.dataframe[Col_PlateName].unique()

                # save each plate in separate file
                for plate in uniquePlate:
                    df = file.dataframe[file.dataframe[Col_PlateName] == plate].reset_index()
                    df.to_csv(os.path.join(self.DirPath, plate + '.csv'))


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
                        platenumber = plateId[Col_PlateNumber][i]

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

        def __create_plate():
            """
            create a plate object
            """
            self.PlateToAnalyse = TCA.Plate(name=self.PlateName.get(),
                                            platemap=TCA.Core.PlateMap(size=self.plate_size.get()))
            window.destroy()

        tkinter.Button(window, text='Create Plate', command=__create_plate).grid(row=3, column=0)

    def __remove_platemap(self):
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)
        tkinter.Label(window, text="New platemap size").grid(row=0, column=0)
        newplatemapsize = StringVar()
        Combobox(window, textvariable=newplatemapsize, values=('96', '384'), state='readonly').grid(row=0, column=1)
        newplatemapsize.set('96')

        def make_destroy():
            """
            destroy platemap
            :return:
            """
            self.PlateToAnalyse.add_platemap(TCA.PlateMap(size=int(newplatemapsize.get())))
            window.destroy()

        tkinter.Button(window, text='New platemap', command=make_destroy).grid(row=2, column=0)

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

        def editplate():
            """
            Edit plate
            :return:
            """
            self.PlateToAnalyse.set_name(self.PlateName.get())
            window.destroy()

        tkinter.Button(window, text='New platename', command=editplate).grid(row=2, column=0)

    def __add_platemap(self):
        """
        Function for adding a platemap to plate
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return
        window = Toplevel(self)
        tkinter.Button(window, text='Browse file', command=self.load_file).grid(row=1, column=0)

        def addplatemap():
            self.PlateToAnalyse.add_platemap(TCA.PlateMap(fpath=self.FilePathToOpen))
            self.PlateToAnalyseAddedPM = True
            window.destroy()

        tkinter.Button(window, text='Add file/replica to plate', command=addplatemap).grid(row=2, column=0)

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

        def addreplica():
            self.PlateToAnalyse.add_replica(TCA.Replica(name=repname.get(), fpath=self.FilePathToOpen))
            window.destroy()

        tkinter.Button(window, text='Add file/replica to plate', command=addreplica).grid(row=3, column=0)

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

        def removereplica():
            self.PlateToAnalyse.remove_replica(repname.get())
            window.destroy()

        tkinter.Button(window, text='Remove replica', command=removereplica).grid(row=2, column=0)

    def __Analyse(self):
        """
        Do analyse on current plate
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return

        NegRef = chk_empty(self.NegCtrl.get())
        logging.debug("Negative reference : {}".format(NegRef))

        if NegRef is not None:
            if not self.PlateToAnalyseAddedPM:
                NegRef = NegRef.split()
                # add this for having a virgin platemap
                self.PlateToAnalyse.platemap = TCA.PlateMap(size=self.PlateToAnalyse.platemap.shape(alt_frmt=True))
                for i in NegRef:
                    self.PlateToAnalyse.platemap[i] = "Neg"
                NegRef = "Neg"
            else:
                NegRef = NegRef

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
            thresRef = eval(thresRef)

        if self.threshold_type.get() == 'Percent':
            thresTypePercent, thresTypeFixedVal = True, False
            if isinstance(thresRef, int):
                thresRef = 100 - thresRef
            elif isinstance(thresRef, dict):
                thresRef = dict((k, 100 - v) for k, v in thresRef.items())

        else:
            thresTypePercent, thresTypeFixedVal = False, True

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

        self.selectFileToSave()
        self.CurrentResToSave.to_csv(self.SaveFilePath, header=True, index=False)

    def __Scoring(self):
        """
        Do analyse on current plate
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return

        NegRef = chk_empty(self.NegCtrl.get())
        logging.debug("Negative reference : {}".format(NegRef))

        if NegRef is not None:
            if not self.PlateToAnalyseAddedPM:
                NegRef = NegRef.split()
                # add this for having a virgin platemap
                self.PlateToAnalyse.platemap = TCA.PlateMap(size=self.PlateToAnalyse.platemap.shape(alt_frmt=True))
                for i in NegRef:
                    self.PlateToAnalyse.platemap[i] = "Neg"
                NegRef = "Neg"
            else:
                NegRef = NegRef

        ChanRef = self.ChnVal.get()
        logging.debug("Channel analysed : {}".format(ChanRef))
        if ChanRef == '':
            logging.error("Must have a channel")
        else:
            ChanRef = ChanRef

        self.CurrentResToSave = TCA.ScoringPlate(self.PlateToAnalyse, neg=NegRef, channel=ChanRef)
        self.selectFileToSave()
        self.CurrentResToSave.to_csv(self.SaveFilePath, header=True, index=False)

    def __cellsCount(self):
        """
        Function that perform cellscount
        """
        if self.PlateToAnalyse is None:
            tkinter.messagebox.showerror(message="No existing Plate, create one")
            return

        self.CurrentResToSave = TCA.PlateChannelsAnalysis(self.PlateToAnalyse, channels=None,
                                                          neg=None,
                                                          noposcell=True,
                                                          multiIndexDF=True)

        self.selectFileToSave()
        self.CurrentResToSave.to_csv(self.SaveFilePath, header=True, index=False)

    def __Binning(self):
        """
        Function that perform binning
        """
        if not DEBUG:
            if self.PlateToAnalyse is None:
                tkinter.messagebox.showerror(message="No existing Plate, create one")
                return
        window = Toplevel(self)

        tkinter.Label(window, text="Which channels").grid(row=0, column=1)
        tkinter.Label(window, text="Custom bin (interval)").grid(row=1, column=1)
        self.BinChan = StringVar()
        self.Bin = StringVar()
        tkinter.Entry(window, textvariable=self.BinChan).grid(row=0, column=0)
        tkinter.Entry(window, textvariable=self.Bin).grid(row=1, column=0)

        self.BinPercent = IntVar()
        Checkbutton(window, text="Percent", variable=self.BinPercent).grid(row=2, column=0)
        self.BinPercent.set(0)
        tkinter.Label(window, text="Percent value or not").grid(row=2, column=1)

        def dobinning():
            if self.Bin.get() != "":
                Bin = self.Bin.get().split()
            else:
                Bin = None
            for chan in self.BinChan.get().split():
                if Bin is None:
                    self.CurrentResToSave = TCA.Binning(self.PlateToAnalyse, chan=chan, nbins=20,
                                                        percent=bool(self.BinPercent.get()))
                else:
                    self.CurrentResToSave = TCA.Binning(self.PlateToAnalyse, chan=chan, bins=Bin,
                                                        percent=bool(self.BinPercent.get()))
            self.selectFileToSave()
            workbook = pd.ExcelWriter(self.SaveFilePath)
            for id, df in self.CurrentResToSave.items():
                pd.DataFrame(df).to_excel(workbook, id)
            workbook.close()

        tkinter.Button(window, text="Do Binning", fg="red", command=dobinning).grid(row=3, column=0)

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
                                                             "RobustPercentOfControl", "NormalizedPercentInhibition"),
                 state='readonly').grid(
            row=1, column=1)
        self.dataNorm.set('Zscore')

        tkinter.Label(window, text="Neg Ctrl").grid(row=2, column=0)
        tkinter.Label(window, text="Pos Ctrl").grid(row=3, column=0)
        tkinter.Label(window, text="Channel").grid(row=4, column=0)

        self.NormNeg = StringVar()
        self.NormPos = StringVar()
        self.NormChan = StringVar()
        tkinter.Entry(window, textvariable=self.NormNeg).grid(row=2, column=1)
        tkinter.Entry(window, textvariable=self.NormPos).grid(row=3, column=1)
        tkinter.Entry(window, textvariable=self.NormChan).grid(row=4, column=1)

        tkinter.Button(window, text='Apply data norm',
                       command=lambda: self.PlateToAnalyse.normalization_channels(channels=[self.NormChan.get()],
                                                                                  method=self.dataNorm.get(),
                                                                                  log_t=False,
                                                                                  neg=chk_empty(self.NormNeg.get()),
                                                                                  pos=chk_empty(self.NormPos.get())),
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
        self.SideNorm.set('Bscore')

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

        def __do_QC():
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
            qc.to_csv(self.SaveFilePath, header=True, index=True)

        tkinter.Button(window, text='Launch QC', command=__do_QC, fg="red").grid(row=4, column=0)

    def _DoBatchAnalyse(self):

        # ## Get all value of arg
        __BatchDirPath = self.DirPath
        __BatchInputPlateName = self.BatchInPlateName.get()
        __BatchInputPlamap = self.BatchPlateMapName.get()
        __BatchNPlate = int(self.BatchNPlate.get())
        __BatchNRep = int(self.BatchNRep.get())
        __BatchNeg = self.BatchNegCtrl.get()
        __BatchPos = self.BatchPosCtrl.get()
        __BatchChan = self.BatchChan.get()
        __BatchThresVal = eval(self.BatchThrsVal.get())
        __BatchThresType = self.BatchThrsType.get()
        __BatchDataNorm = self.BatchDataNorm.get()
        __BatchSideEffect = self.BatchSideEffectNorm.get()
        __BatchMeanSD_Ref = self.BatchMeanSD.get()
        __BatchQC = bool(self.BatchQC.get())
        __BatchScoring = bool(self.BatchScoring.get())
        __BatchHeatmap = bool(self.BatchHeatMap.get())

        # create a directory where data is located with timestamp as dir name
        __outputDirPath = os.path.join(__BatchDirPath, time.asctime())
        if not os.path.isdir(__outputDirPath):
            os.makedirs(__outputDirPath)

        # ## File for saving log and threshold value
        THRVALUEFILE = LogFile(path=__outputDirPath, name="THRESHOLD_VALUE")
        LOGFILE = LogFile(path=__outputDirPath, name="PROCESS_LOGFILE")

        # ## lst for saving data
        DF_result = []
        DF_resultWithNorm = []
        QC_BeforeNorm = []
        QC_AfterNorm = []
        Scoring_BeforeNorm = []
        Scoring_AfterNorm = []

        for i in range(1, __BatchNPlate + 1, 1):
            # ## create first a plate object with a platemap object
            pm_filepath = os.path.join(__BatchDirPath, __BatchInputPlamap.format(i))
            if os.path.isfile(pm_filepath):
                plaque = TCA.Plate(name="Plate nb{}".format(i), platemap=pm_filepath)
                LOGFILE.add("Create plate : {}".format(plaque.name))
            else:
                logging.warning("File doesn't exist : {}".format(file))
                continue

            # create and add replica to main plate object
            for j in range(1, __BatchNRep + 1, 1):
                file = os.path.join(__BatchDirPath, __BatchInputPlateName.format(i, j))
                if os.path.isfile(file):
                    plaque + TCA.Core.Replica(name='Rep ' + str(j), fpath=file)
                    LOGFILE.add("Add data : {}".format(file))
                else:
                    logging.warning("File doesn't exist : {}".format(file))

            # ## if plate object has no replica (because no file found) then continue to next plaque id
            if len(plaque) == 0:
                logging.error("Empty plate")
                continue

            # #### CHANNEL ANALYSIS WITHOUT NORM
            if __BatchThresType == 'Percent':
                if isinstance(__BatchThresVal, int):
                    threshold_value = 100 - __BatchThresVal
                elif isinstance(__BatchThresVal, dict):
                    threshold_value = dict((k, 100 - v) for k, v in __BatchThresVal.items())
                percent_type = True
                threshold_fixed = False
                LOGFILE.add("Threshold Type : {0} with {1} value".format(__BatchThresType, __BatchThresVal))
            else:
                threshold_value = __BatchThresVal
                percent_type = False
                threshold_fixed = True
                LOGFILE.add("Threshold Type : {0} with {1} value".format(__BatchThresType, __BatchThresVal))

            df, thres = TCA.PlateChannelsAnalysis(plaque,
                                                  channels=__BatchChan.split(),
                                                  neg=__BatchNeg,
                                                  threshold=threshold_value,
                                                  percent=percent_type,
                                                  fixed_threshold=threshold_fixed)

            if percent_type:
                THRVALUEFILE.add("{0} @ {1}%: {2}".format(plaque.name, __BatchThresVal, thres))
            else:
                THRVALUEFILE.add("{0} @ {1}%: {2}".format(plaque.name, __BatchThresVal, thres))
            LOGFILE.add("* Do analysis on channels : {}".format(__BatchChan))
            DF_result.append(df)

            # scoring results on non-normalized data
            if __BatchScoring:
                Scoring_BeforeNorm.append(TCA.ScoringPlate(plaque,
                                                           neg=__BatchNeg,
                                                           channel=__BatchChan.split()[0],
                                                           data_c=False))
                LOGFILE.add("* Do scoring on non-normalized data")

            # # make QC if wanted
            if __BatchQC:
                qc = TCA.plate_quality_control(plate=plaque,
                                               channel=__BatchChan.split()[0],
                                               cneg=__BatchNeg,
                                               cpos=__BatchPos,
                                               sec_data=False)
                QC_BeforeNorm.append(qc)
                LOGFILE.add("* Do QC on non-normalized data")

            # # save heatmap if wanted
            if __BatchHeatmap:
                for chan in __BatchChan.split():
                    plaque.agg_data_from_replica_channel(channel=chan, forced_update=True)
                    TCA.HeatMapPlate(plaque, fpath=os.path.join(__outputDirPath,
                                                                "HEATMAP_WithoutNorm_{}.pdf".format(plaque.name)),
                                     size=20.)

            # ##### NORMALIZED PIPELINE BEGIN HERE
            # Raw data normalization
            if __BatchDataNorm != "":
                plaque.normalization_channels(channels=__BatchChan.split(),
                                              method=__BatchDataNorm,
                                              neg=chk_empty(__BatchNeg),
                                              pos=chk_empty(__BatchPos),
                                              log_t=False)
                LOGFILE.add(
                    "DO single cell data normalization : \n  -> Channels : {0}\n  -> Method : {1}\n  -> Neg : {2}\n  -> Pos : {3}".format(
                        __BatchChan, __BatchDataNorm, __BatchNeg, __BatchPos))

            # side effect normalization
            if __BatchSideEffect != "":
                plaque.apply_systematic_error_correction(algorithm=__BatchSideEffect,
                                                         apply_down=True,
                                                         max_iterations=10)
                LOGFILE.add("DO side effect normalization : {0}".format(__BatchSideEffect))

            if __BatchDataNorm:
                # #### CHANNEL ANALYSIS WITH NORM
                if __BatchThresType == 'Percent':
                    if isinstance(__BatchThresVal, int):
                        threshold_value = 100 - __BatchThresVal
                    elif isinstance(__BatchThresVal, dict):
                        threshold_value = dict((k, 100 - v) for k, v in __BatchThresVal.items())
                    percent_type = True
                    threshold_fixed = False
                    LOGFILE.add("Threshold Type : {0} with {1} value".format(__BatchThresType, __BatchThresVal))
                else:
                    threshold_value = __BatchThresVal
                    percent_type = False
                    threshold_fixed = True
                    LOGFILE.add("Threshold Type : {0} with {1} value".format(__BatchThresType, __BatchThresVal))

                df, thres = TCA.PlateChannelsAnalysis(plaque,
                                                      channels=__BatchChan.split(),
                                                      neg=__BatchNeg,
                                                      threshold=threshold_value,
                                                      percent=percent_type,
                                                      fixed_threshold=threshold_fixed)

                if percent_type:
                    THRVALUEFILE.add(
                        "Normalized {0} @ {1}%: {2}".format(plaque.name, __BatchThresVal, thres))
                else:
                    THRVALUEFILE.add("Normalized {0} @ {1}%: {2}".format(plaque.name, __BatchThresVal, thres))
                LOGFILE.add("* Do analysis on normalized channels : {}".format(__BatchChan))
                DF_resultWithNorm.append(df)

            # #### CHANNEL ANALYSIS WITH NORM
            if __BatchDataNorm or __BatchSideEffect != "":

                # scoring results on normalized data
                if __BatchScoring:
                    if __BatchSideEffect == "":
                        plaque.agg_data_from_replica_channel(channel=__BatchChan.split()[0],
                                                             forced_update=True)
                        Scoring_AfterNorm.append(TCA.ScoringPlate(plaque,
                                                                  neg=__BatchNeg,
                                                                  channel=__BatchChan.split()[0],
                                                                  data_c=False))
                    else:
                        Scoring_AfterNorm.append(TCA.ScoringPlate(plaque,
                                                                  neg=__BatchNeg,
                                                                  channel=__BatchChan.split()[0],
                                                                  data_c=True))
                    LOGFILE.add("* Do scoring on normalized data")

                # ## QC after norm data
                if __BatchQC:
                    if __BatchSideEffect != "":
                        use_sec_data = True
                    else:
                        use_sec_data = False
                    qc = TCA.plate_quality_control(plate=plaque,
                                                   channel=__BatchChan.split()[0],
                                                   cneg=__BatchNeg,
                                                   cpos=__BatchPos,
                                                   sec_data=use_sec_data)
                    QC_AfterNorm.append(qc)
                    LOGFILE.add("* Do QC on normalized data")

                # ## plot heatmap after data norm
                if __BatchHeatmap:
                    for chan in __BatchChan.split():
                        plaque.agg_data_from_replica_channel(channel=chan, forced_update=True,
                                                             use_sec_data=__BatchSideEffect)
                        TCA.HeatMapPlate(plaque, fpath=os.path.join(__outputDirPath,
                                                                    "HEATMAP_WithNorm_{}.pdf".format(plaque.name)),
                                         size=20.)

        # #### WRITING RESULT PART

        # # don't save anything if anything was compute
        if len(DF_result) != 0:

            workbook = pd.ExcelWriter(os.path.join(__outputDirPath, "RESULT.xlsx"))

            # # save basic data before norm like value for each wells
            beforenorm = pd.concat(DF_result)
            beforenorm.to_excel(workbook, "Analyse without norm",
                                index=False, header=True)

            if __BatchDataNorm:
                afternorm = pd.concat(DF_resultWithNorm)
                afternorm.to_excel(excel_writer=workbook, sheet_name="Analyse with norm",
                                   index=False, header=True)

            # # save QC data
            if __BatchQC:
                pd.concat(QC_BeforeNorm).to_excel(excel_writer=workbook, sheet_name="QC without norm",
                                                  index=False, header=True)

                if __BatchDataNorm or __BatchSideEffect != "":
                    pd.concat(QC_AfterNorm).to_excel(excel_writer=workbook, sheet_name="QC with norm",
                                                     index=False, header=True)
            # # save mean and sd for given reference
            if __BatchMeanSD_Ref != "":
                x = beforenorm[beforenorm.PlateMap.isin(__BatchMeanSD_Ref.split())]
                x.groupby(by=['PlateName', 'PlateMap']).mean().to_excel(excel_writer=workbook,
                                                                        sheet_name="Reference Mean",
                                                                        index=True, header=True)
                x.groupby(by=['PlateName', 'PlateMap']).std().to_excel(excel_writer=workbook,
                                                                       sheet_name="Reference std",
                                                                       index=True, header=True)

                if __BatchDataNorm:
                    afternorm = pd.concat(DF_resultWithNorm)
                    x = afternorm[afternorm.PlateMap.isin(__BatchMeanSD_Ref.split())]
                    x.groupby(by=['PlateName', 'PlateMap']).mean().to_excel(excel_writer=workbook,
                                                                            sheet_name="Reference Mean Norm",
                                                                            index=True, header=True)
                    x.groupby(by=['PlateName', 'PlateMap']).std().to_excel(excel_writer=workbook,
                                                                           sheet_name="Reference std Norm",
                                                                           index=True, header=True)

            # # save scoring & if norm where applied
            if __BatchScoring:
                pd.concat(Scoring_BeforeNorm).to_excel(excel_writer=workbook, sheet_name="Scoring Without Norm",
                                                       index=False, header=True)
                if __BatchDataNorm or __BatchSideEffect != "":
                    pd.concat(Scoring_AfterNorm).to_excel(excel_writer=workbook, sheet_name="Scoring With Norm.",
                                                          index=False, header=True)

            workbook.close()
        # close file
        THRVALUEFILE.close()
        LOGFILE.close()
        logging.info("BATCH FINISH \./")

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

        def __DoHeatmap():
            """
            Do heatmap
            """
            if self.heatmapToplot.get() == 'CellsCount':
                self.PlateToAnalyse.use_count_as_data()
            else:
                self.PlateToAnalyse.agg_data_from_replica_channel(channel=self.heatmapChanneltoplot.get(),
                                                                  forced_update=True)

            TCA.HeatMapPlate(self.PlateToAnalyse)

        tkinter.Button(window, text='Do Heatmap', command=__DoHeatmap, fg="red").grid(row=3, column=0)

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

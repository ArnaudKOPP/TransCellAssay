__author__ = 'Arnaud KOPP'
"""
Parse defined method for reading data from a directory (replicat data and platesetup)
PlXrep_0.csv, PlXrep_1.csv ... name for replicat
PlXPP.csv  name for platesetup
"""
import os
import re


def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    Include only csv file
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".csv"):
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.
    return file_paths  # Self-explanatory.


def parsePlateCouple(plateList):
    """
    Parse plate list and create plate object
    :param plateList:
    :return:
    """
    try:
        for items in plateList:
            print('\n')
            print(items)
            splItemps = str.split(items, sep="/")
            print(splItemps[-1])
            regexp = re.compile(r'PP')
            if regexp.search(splItemps[-1]) is not None:
                print('matched Platesetup !!')
            else:
                print('matched replicat data !!')
    except Exception as e:
        print(e)
        print('Error in parsing Plate list %s' % plateList)


def parseInputDirectory(InputDirectory):
    """
    Parse the input Directory and create plate couple, begin here the pipeline
    :param InputDirectory:
    :return:
    """
    try:
        # Run the above function and store its results in a variable.
        full_file_paths = get_filepaths(InputDirectory)
        parsePlateCouple(full_file_paths)
        # print(full_file_paths)
    except Exception as e:
        print(e)
        print('Error in parsing directory %s' % InputDirectory)

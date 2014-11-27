"""
Parse defined method for reading data from a directory (replicat data and platesetup)
PlXrep_0.csv, PlXrep_1.csv ... name for replicat
PlXPP.csv  name for platesetup
"""

import os
import re

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def input_directory_parser(input_dir, extension='.csv'):
    """
    Parse the input Directory and create plate couple, begin here the pipeline
    :param input_dir:
    :return:
    """
    try:
        # Run the above function and store its results in a variable.
        full_file_paths = _get_all_files_of_directory(input_dir, extension=extension)
        _parse_file_list(full_file_paths)
        print(full_file_paths)

        indice = [m.group(0) for m in (re.search(r'\d+', l) for l in full_file_paths) if m]
        ind = [int(i) for i in indice]  # transform list of string to int

        print(max(ind))

        return full_file_paths

    except Exception as e:
        print('\033[0;31m[ERROR]\033[0m Error in parsing directory %s' % input_dir, e)


def _get_all_files_of_directory(directory, extension):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    Include only csv file
    """
    try:
        files_path = []  # List which will store all of the full filepaths.

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                if filename.endswith(extension):
                    # Join the two strings in order to form the full filepath.
                    file_path = os.path.join(root, filename)
                    files_path.append(file_path)  # Add it to the list.
        return sorted(files_path)  # Self-explanatory.
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


def _parse_file_list(file_list):
    """
    Parse file list
    :param file_list:
    :return:
    """
    try:
        for items in file_list:
            item_split = str.split(items, sep="/")
            print(item_split[-1])
            regexp = re.compile(r'PP')

            if regexp.search(item_split[-1]) is not None:
                print('matched PlateMap !!')
                match = re.search(r'\d+', item_split[-1])
                print(match.group(0))
            else:
                print('matched replicat data !!')
                match = re.finditer(r'\d+', item_split[-1])
                for m in match:
                    print(m.group(0))
    except Exception as e:
        print('\033[0;31m[ERROR]\033[0m Error in parsing Plate list %s', e)

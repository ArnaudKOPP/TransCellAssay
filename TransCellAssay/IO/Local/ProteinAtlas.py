# coding=utf-8
"""
Protein Atlas File Parser

http://www.proteinatlas.org/about/download

All data in xml file ~ 8 gb uncompressed
http://www.proteinatlas.org/download/proteinatlas.xml.gz

RNA data in csv file
http://www.proteinatlas.org/download/rna.csv.zip
"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import os
import zipfile
import gzip
import urllib.request
import pandas as pd
from TransCellAssay.Utils.utils import reporthook


class ProteinAtlas(object):
    """
    Class for parsing data from protein atlas
    """
    RNA_DATA = "http://www.proteinatlas.org/download/rna.csv.zip"
    DATA = "http://www.proteinatlas.org/download/proteinatlas.xml.gz"

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def download_data(cls, force_update=True, location=None):
        try:
            if force_update or not os.path.isfile(cls.RNA_DATA):
                if location is not None:
                    urllib.request.urlretrieve(url=cls.RNA_DATA, filename=os.path.join(location, "rna.csv.zip"),
                                               reporthook=reporthook)
                else:
                    urllib.request.urlretrieve(url=cls.RNA_DATA, filename="rna.csv.zip", reporthook=reporthook)
                with zipfile.ZipFile("rna.csv.zip", 'r') as myzip:
                    myzip.extractall()
        except Exception as e:
            print(e)
        try:
            if force_update or not os.path.isfile(cls.DATA):
                if location is not None:
                    urllib.request.urlretrieve(url=cls.DATA, filename=os.path.join(location, "proteinatlas.xml.gz"),
                                               reporthook=reporthook)
                else:
                    urllib.request.urlretrieve(url=cls.DATA, filename="proteinatlas.xml.gz", reporthook=reporthook)
                with gzip.GzipFile("proteinatlas.xml.gz", "r") as mygzip:
                    mygzip.extractall()
        except Exception as e:
            print(e)
    @classmethod
    def init_db(cls):
        raise NotImplementedError
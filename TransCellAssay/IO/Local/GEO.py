"""
GEO File Parser

http://www.ncbi.nlm.nih.gov/geo/
ftp://ftp.ncbi.nih.gov/pub/geo/DATA/SOFT/GDS/
"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"


class GEO(object):
    """
    Class for parsing GEO data file
    """

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def download_data(cls, location=None):
        raise NotImplementedError

    @classmethod
    def init_db(cls):
        raise NotImplementedError
"""
Protein Atlas File Parser

http://www.proteinatlas.org/about/download

http://www.proteinatlas.org/download/proteinatlas.xml.gz
"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"


class ProteinAtlas(object):
    """
    Class for parsing data from protein atlas
    """

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def download_data(cls):
        raise NotImplementedError

    @classmethod
    def init_db(cls):
        raise NotImplementedError
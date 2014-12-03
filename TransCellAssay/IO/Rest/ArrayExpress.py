"""
Array Express REST

REST : https://www.ebi.ac.uk/arrayexpress/help/programmatic_access.html
"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

from TransCellAssay.IO.Rest.Service import REST


class ArrayExpress(REST):
    """
    Array Express rest class
    """

    def __init__(self, verbose=False):
        super(ArrayExpress, self).__init__(name="ArrayExpress", url="", verbose=verbose)
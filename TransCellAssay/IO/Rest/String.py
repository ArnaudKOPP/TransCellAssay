"""
String-db REST services
Website : www.http://string-db.org
REST Documentation : http://string-db.org/help/index.jsp?topic=/org.string-db.docs/api.html
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


class String(REST):
    """
    Class for doing REST requests to String-db
    """

    def __init__(self, verbose=False):
        super(String, self).__init__(name="String", url="http://string-db.org/", verbose=verbose)
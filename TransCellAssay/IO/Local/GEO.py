# coding=utf-8
"""
GEO File Parser

http://www.ncbi.nlm.nih.gov/geo/
ftp://ftp.ncbi.nih.gov/pub/geo/DATA/SOFT/GDS/
"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import pickle
import os
import re
from collections import defaultdict


def spots_mean(x):
    vs = [v for v in x if v and v != "?"]
    if len(vs) == 0: return "?"
    return sum(vs)/len(vs)


def spots_median(x):
    vs = [v for v in x if v and v != "?"]
    if len(vs) == 0: return "?"
    if len(vs) % 2:
        return sorted(vs)/(len(vs)/2)
    else:
        z = sorted(x)
        return (z[len(vs)/2-1] + z[len(vs)/2]) / 2.
    return sum(vs)/len(vs)


def spots_min(x):
    vs = [v for v in x if v and v != "?"]
    if len(vs) == 0: return "?"
    return min(vs)/len(vs)


def spots_max(x):
    vs = [v for v in x if v and v != "?"]
    if len(vs) == 0: return "?"
    return max(vs)/len(vs)

p_assign = re.compile(" = (.*$)")
p_tagvalue = re.compile("![a-z]*_([a-z_]*) = (.*)$")
tagvalue = lambda x: p_tagvalue.search(x).groups()


FTP_NCBI = "ftp.ncbi.nih.gov"
FTP_DIR = "pub/geo/DATA/SOFT/GDS/"


class GDSInfo(object):
    """
    An instance behaves like a dictionary: the keys are GEO DataSets
    IDs, and the dictionary values for is a dictionary providing various
    information about the particular data set.
    """

    def __init__(self, path, verbose=False):
        self._verbose = verbose
        f = open(path, "rb")
        self.info, self.excluded = pickle.load(f)

    def keys(self):
        return self.info.keys()

    def items(self):
        return self.info.items()

    def values(self):
        return self.info.values()

    def clear(self):
        return self.info.clear()

    def __getitem__(self, key):
        return self.info[key]

    def __setitem__(self, key, item):
        self.info[key] = item

    def __len__(self):
        return len(self.info)

    def __iter__(self):
        return iter(self.info)

    def __contains__(self, key):
        return key in self.info


class GeneData(object):
    """Store mapping between spot id and gene."""
    def __init__(self, spot_id, gene_name, d):
        self.spot_id = spot_id
        self.gene_name = gene_name
        self.data = d


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
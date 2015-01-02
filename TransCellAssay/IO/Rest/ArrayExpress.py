# coding=utf-8
"""
Array Express REST

REST : https://www.ebi.ac.uk/arrayexpress/help/programmatic_access.html
"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

from TransCellAssay.IO.Rest.Service import REST
import os
import urllib.request
import re
import shelve
import shutil
import posixpath
import json
from xml.etree.ElementTree import ElementTree
from io import StringIO
from collections import defaultdict
from functools import partial
from contextlib import closing
from contextlib import contextmanager


class ArrayExpress(REST):
    """
    Array Express rest class
    """
    DEFAULT_FORMAT = "json"
    DEFAULT_ADDRESS = "http://www.ebi.ac.uk/arrayexpress/" + str(DEFAULT_FORMAT) + "/v2/"
    # Order of arguments in the query
    _ARGS_ORDER = ["keywords", "species", "array"]
    # All searchable fields of ArrayExpress (see query_experiments docstring
    # for a description of the fields)
    ARRAYEXPRESS_FIELDS = ["keywords", "accession", "array", "ef", "efv", "expdesign", "exptype", "gxa", "pmid", "sa",
                           "species", "expandefo", "directsub", "assaycount", "efcount", "samplecount", "sacount",
                           "rawcount", "fgemcount", "miamescore", "date", "wholewords"]

    def __init__(self, verbose=False):
        super(ArrayExpress, self).__init__(name="ArrayExpress", url=self.DEFAULT_ADDRESS, verbose=verbose)

    def _format_query(self, **kwargs):
        """
        Format the query arguments in `kwargs`.

        conn.format_query(gxa=True, efcount=(1, 5))
        'efcount=[1 TO 5]&gxa=true'

        """
        # Formaters:
        def format_default(val):
            if isinstance(val, str):
                return val
            else:
                return "+".join(val)

        def format_species(val):
            return '"%s"' % val.lower()

        def format_gxa(val):
            if val:
                return "true"
            else:
                raise ValueError("gxa={0}".format(val))

        def format_expandefo(val):
            if val:
                return "on"
            else:
                raise ValueError("expandefo={0}".format(val))

        def format_true_false(val):
            return "true" if val else "false"

        def format_interval(val):
            if isinstance(val, tuple):
                return "[{0} TO {1}]".format(*val)
            else:
                raise ValueError("Must be an interval argument (min, max)!")

        def format_date(val):
            # TODO check if val contains a datetime.date object
            # assert proper format
            return format_interval(val)

        def format_wholewords(val):
            if val:
                return "on"
            else:
                raise ValueError("wholewords={0}".format(val))

        formaters = {"species": format_species,
                     "gxa": format_gxa,
                     "expandefo": format_expandefo,
                     "directsub": format_true_false,
                     "assaycount": format_interval,
                     "efcount": format_interval,
                     "samplecount": format_interval,
                     "sacount": format_interval,
                     "rawcount": format_interval,
                     "fgemcount": format_interval,
                     "miamescore": format_interval,
                     "date": format_date,
                     "wholewords": format_wholewords,
        }
        parts = []
        arg_items = kwargs.items()

        arg_items = sorted(
            arg_items,
            key=lambda arg: self._ARGS_ORDER.index(arg[0])
            if arg[0] in self._ARGS_ORDER else 100
        )

        for key, value in arg_items:
            if key == "format":
                continue  # format is handled in query_url
            if key not in self.ARRAYEXPRESS_FIELDS:
                raise ValueError("Invalid argument name: '{0}'".format(key))
            if value is not None and value != []:
                fmt = formaters.get(key, format_default)
                value = fmt(value)
                parts.append("{0}={1}".format(key, value))

        return "&".join(parts)

    def _query_url(self, what="experiments", **kwargs):
        """
        Return a formatted query URL for the query arguments.

        conn.query_url(accession="E-MEXP-31")
        'http://www.ebi.ac.uk/arrayexpress/json/v2/experiments?accession=E-MEXP-31'

        """
        query = self._format_query(**kwargs)
        url = posixpath.join(self.DEFAULT_ADDRESS, what)
        url = url.format(format=kwargs.get("format", self.DEFAULT_FORMAT))
        url += "?" + query if query else ""
        # url = url.replace(" ", "%20")
        return url

    def _query_url_experiments(self, **kwargs):
        """
        Return query URL of formatted experiments for the query arguments.
        """
        return self._query_url("experiments", **kwargs)

    def _query_url_files(self, **kwargs):
        """
        Return query URL of formatted experiments for the query arguments.
        """
        return self._query_url("files", **kwargs)

    def _query_experiment(self, **kwargs):
        """
        Return an open stream to the experiments query results.
        Takes the same arguments as the :obj:`query_experiments` function.
        """
        url = self._query_url_experiments(**kwargs)
        stream = self.http_get(url, frmt=self.DEFAULT_FORMAT)
        return stream

    def _query_files(self, **kwargs):
        """
        Return an open stream to the files query results.
        Takes the same arguments as the :obj:`query_files` function.
        """
        url = self._query_url_files(**kwargs)
        stream = self.http_get(url, frmt=self.DEFAULT_FORMAT)
        return stream

    def query_experiments(self, keywords=None, accession=None, array=None, ef=None,
                          efv=None, expdesign=None, exptype=None,
                          gxa=None, pmid=None, sa=None, species=None,
                          expandefo=None, directsub=None, assaycount=None,
                          efcount=None, samplecount=None, rawcount=None,
                          fgemcount=None, miamescore=None, date=None,
                          format="json", wholewords=None):
        """
        Query Array Express experiments.

        query_experiments(species="Homo sapiens", ef="organism_part", efv="liver")
        {u'experiments': ...

        """

        stream = self._query_experiment(
            keywords=keywords, accession=accession,
            array=array, ef=ef, efv=efv, expdesign=expdesign, exptype=exptype,
            gxa=gxa, pmid=pmid, sa=sa, species=species, expandefo=expandefo,
            directsub=directsub, assaycount=assaycount, efcount=efcount,
            samplecount=samplecount, rawcount=rawcount, fgemcount=fgemcount,
            miamescore=miamescore, date=date, format=format,
            wholewords=wholewords
        )

        return stream

    def query_files(self, keywords=None, accession=None, array=None, ef=None,
                    efv=None, expdesign=None, exptype=None,
                    gxa=None, pmid=None, sa=None, species=None,
                    expandefo=None, directsub=None, assaycount=None,
                    efcount=None, samplecount=None, rawcount=None,
                    fgemcount=None, miamescore=None, date=None,
                    format="json", wholewords=None, connection=None):
        """
        Query Array Express files. See :obj:`query_experiments` for the arguments.

        query_files(species="Mus musculus", ef="developmental_stage", efv="embryo", format="xml")
        <xml.etree.ElementTree.ElementTree object ...

        """
        stream = connection.query_files(
            keywords=keywords, accession=accession,
            array=array, ef=ef, efv=efv, expdesign=expdesign, exptype=exptype,
            gxa=gxa, pmid=pmid, sa=sa, species=species, expandefo=expandefo,
            directsub=directsub, assaycount=assaycount, efcount=efcount,
            samplecount=samplecount, rawcount=rawcount, fgemcount=fgemcount,
            miamescore=miamescore, date=date, format=format,
            wholewords=wholewords
        )

        return stream
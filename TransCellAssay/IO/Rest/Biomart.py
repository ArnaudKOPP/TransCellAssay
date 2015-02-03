# coding=utf-8
"""
This module provides a class :class:`~BioModels` that allows an easy access
to all the BioModel service.


.. topic:: What is BioMart ?

    :URL: http://www.biomart.org/
    :REST: http://www.biomart.org/martservice.html
           http://www.biomart.org/other/biomart_0.9_0_documentation.pdf

    .. highlights::

        The BioMart project provides free software and data services to the
        international scientific community in order to foster scientific collaboration
        and facilitate the scientific discovery process. The project adheres to the open
        source philosophy that promotes collaboration and code reuse.

        -- from BioMart March 2013

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

# TODO finish class


class BioMart(REST):
    """
    Interface to the `BioMart <http://www.biomart.org>`_ service

    V 0.9 implemented

    BioMart is made of different views. Each view correspond to a specific **MART**.
    For instance the UniProt service has a `BioMart view <http://www.ebi.ac.uk/uniprot/biomart/martview/>`_.

    .. note:: the biomart sevice is slow (in my experience, 2013-2014) so please be patient...

    """

    def __init__(self, verbose=False):
        """
        By default, the URL used for the biomart service is::

            http://www.biomart.org/biomart/martservice

        Sometimes, the server is down, in which case you may want to use another
        one (e.g., www.ensembl.org). To do so, use the **host** parameter.

        """
        url = "http://central.biomart.org"

        super(BioMart, self).__init__("BioMart", url=url, verbose=verbose)

    def portal(self, frmt='json'):
        """
        Return the root GUI container containing all child Containers and associated marts
        :param frmt: json or xml
        :return:
        """
        query = "martservice/portal"
        res = self.http_get(query, frmt=frmt, headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res

    def available_marts(self, frmt='json'):
        """
        Return available marts
        :param frmt: json or xml
        :return:
        """
        query = "martservice/marts"
        res = self.http_get(query, frmt=frmt, headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res

    def datasets_for_marts(self, config, frmt='json'):
        """
        Lists all Datasets for the given Mart
        :param config: name of config as returned by the mart object
        :param frmt: json or xml
        :return:
        """
        query = 'martservice/datasets'
        res = self.http_get(query, frmt=frmt, params={'config': str(config)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res

    def filter_for_datasets(self, datasets, config, frmt='json'):
        """
        Lists all filter for the given dataset(s) of a given marts
        :param datasets: Comma-separated string of datasets
        :param config: name of config as returned bu the mart object
        :param frmt: json or xml
        :return:
        """
        query = 'martservice/filters'
        res = self.http_get(query, frmt=frmt, params={'datasets': str(datasets), 'config': str(config)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res

    def attributs_for_datasets(self, datasets, config, frmt='json'):
        """
        List all attributes for the given dataset(s) of a given marts
        :param datasets: Comma-separated string of datasets
        :param config: name of config as returned bu the mart object
        :param frmt: json or xml
        :return:
        """
        query = 'martservice/attributes'
        res = self.http_get(query, frmt=frmt, params={'datasets': str(datasets), 'config': str(config)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res

    def container_for_marts(self, datasets, config,frmt='json'):
        """
        Lists all containers for the given Mart, starting from the root Container
        :param datasets: Comma-separated string of datasets
        :param config: name of config as returned bu the mart object
        :param withattributes: include container attributes
        :param withfilters:  include container filter
        :param frmt: json or xml
        :return:
        """
        query = "martservice/containers"
        res = self.http_get(query, params={'datasets': str(datasets), 'config': str(config)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res
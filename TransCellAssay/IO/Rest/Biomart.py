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

    def container_for_marts(self, datasets, config, frmt='json'):
        """
        Lists all containers for the given Mart, starting from the root Container
        :param datasets: Comma-separated string of datasets
        :param config: name of config as returned bu the mart object
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

    def linkable_datasets(self, datasets, frmt='json'):
        """
        List all the datasets that can be linked with selected datasets
        :param frmt: json or xml
        :param datasets: comma-separated string of datasets
        :return:
        """
        query = "martservice/linkables"
        res = self.http_get(query, params={'datasets': str(datasets)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res

    def querying(self, xmlq):
        """
        Post a query xml
        :param xmlq: the xml query


        Query xml must be formatted like that:

        <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE Query>
                <Query virtualSchemaName="default" formatter="CSV" header="0" uniqueRows="0" count="" datasetConfigVersion="0.6">
                <Dataset name="mmusculus_gene_ensembl" interface="default">
                <Filter name="ensembl_gene_id" value="ENSMUSG00000086981"/>
                <Attribute name="ensembl_gene_id"/>
                <Attribute name="ensembl_transcript_id"/>
                <Attribute name="transcript_start"/>
                <Attribute name="transcript_end"/>
                <Attribute name="exon_chrom_start"/>
                <Attribute name="exon_chrom_end"/>
                </Dataset>
                </Query>

        """
        query = "martservices/results"
        ret = self.http_post(query, frmt=None, data={'query': xmlq.strip()}, headers={})
        return ret


class BioMartQuery(object):
    """
    Class for creating xml query
    """
    def __init__(self, version="1.0", virtualscheme="default"):

        params = {
            "version": version,
            "virtualSchemaName": virtualscheme,
            "formatter": "TSV",
            "header": 0,
            "uniqueRows": 0,
            "configVersion": "0.6"

        }

        self.header = """<?xml version="%(version)s" encoding="UTF-8"?>
    <!DOCTYPE Query>
    <Query  virtualSchemaName = "%(virtualSchemaName)s" formatter = "%(formatter)s"
    header = "%(header)s" uniqueRows = "%(uniqueRows)s" count = ""
    datasetConfigVersion = "%(configVersion)s" >\n""" % params

        self.footer = "    </Dataset>\n</Query>"
        self.reset()

    def add_filter(self, flt):
        """
        Add filter in query xml
        :param flt:
        """
        self.filters.append(flt)

    def add_attribute(self, attribute):
        """
        Add attribut in query xml
        :param attribute:
        """
        self.attributes.append(attribute)

    def add_dataset(self, dataset):
        """
        Set dataset
        :param dataset:
        """
        self.dataset = """    <Dataset name = "%s" interface = "default" >""" % dataset

    def reset(self):
        """
        Reset all value
        """
        self.attributes = []
        self.filters = []
        self.dataset = None

    def get_xml(self):
        """
        Return the xml query
        :return: :raise ValueError:
        """
        if self.dataset is None:
            raise ValueError("data set must be set.")
        xml = self.header
        xml += self.dataset + "\n\n"
        for line in self.filters:
            xml += line + "\n"
        for line in self.attributes:
            xml += line + "\n"
        xml += self.footer
        return xml
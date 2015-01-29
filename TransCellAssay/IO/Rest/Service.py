# coding=utf-8
"""
Base Class for REST services, inspired by bioservices package
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
import platform
import webbrowser
import binascii
import json
import time
import xml.etree.ElementTree as ET
import bs4
import urllib
from urllib.request import urlopen
import requests  # replacement for urllib2 (2-3 times faster)
from requests.models import Response


__all__ = ["Service", "REST"]


class Service(object):
    """
    Base class for REST class
    """

    response_codes = {
        200: 'OK',
        201: 'Created',
        400: 'Bad Request. There is a problem with your input',
        404: 'Not found. The resource you requests does not exist',
        406: "Not Acceptable. Usually headers issue",
        410: 'Gone. The resource you requested was removed.',
        415: "Unsupported Media Type",
        500: 'Internal server error. Most likely a temporary problem',
        503: 'Service not available. The server is being updated, try again later'
    }

    def __init__(self, name, url=None, verbose=True, request_per_sec=3):
        """
        :param name: a name for this service
        :param url: its URL
        :param verbose: prints informative message
        :param request_per_sec:maximum number of requests per seconds
            are restricted to 3. You can change that value. If you reach the
            limit, an error is raise. The reason for this limitation is
            that some services (e.g.., NCBI) may black list you IP.
            If you need or can do more (e.g., ChEMBL does not seem to have
            restrictions), change the value. You can also have several instance
            but again, if you send too many requests at the same, your future
            requests may be restricted.
        """
        self._verbose = verbose
        self._request_per_sec = request_per_sec
        self.url = url
        self._timeout = 30
        self._max_retries = 3
        try:
            if self.url is not None:
                urlopen(self.url)
        except Exception:
            if self._verbose:
                print("\033[0;33m[WARNING]\033[0m The URL (%s) provided cannot be reached." % self.url)
        self.name = name

    def _get_url(self):
        return self.url

    def _set_url(self, url):
        if url is not None:
            url = url.rstrip("/")
            self.url = url

    def _get_easyXMLConversion(self):
        return self._easyXMLConversion

    def _set_easyXMLConversion(self, value):
        if isinstance(value, bool) is False:
            raise TypeError("value must be a boolean value (True/False)")
        self._easyXMLConversion = value

    easyXMLConversion = property(_get_easyXMLConversion, _set_easyXMLConversion,
                                 doc="""If True, xml output from a request are converted to easyXML object (Default behaviour).""")

    def easyXML(self, res):
        """
        Use this method to convert a XML document
        The easyXML object provides utilities to ease access to the XML
        tag/attributes.
        """
        return easyXML(res)

    def __str__(self):
        txt = "Instance of %s service" % self.name
        return txt

    def pubmed(self, id):
        """
        Open a pubmed id into a brower tab
        :param id: valie pubmed id
        """
        url = "http://www.ncbi.nlm.nih.gov/pubmed"
        webbrowser.open(url + str(id))

    def save_str_to_image(self, data, filename):
        """
        Save string object into a file converting into binary
        """
        with open(filename, 'wb') as f:
            try:
                # python3
                newres = binascii.a2b_base64(bytes(data, "utf-8"))
            except:
                newres = binascii.a2b_base64(data)
            f.write(newres)


class REST(Service):
    """
    The ideas (sync/async) and code using requests were inspired from the chembl
    python wrapper but significantly changed.

    Get one value::
    s = REST("test", "https://www.ebi.ac.uk/chemblws")
    res = s.get_one("targets/CHEMBL2476.json", "json")
    res['organism']
    u'Homo sapiens'

    Advantages of requests over urllib
    requests length is not limited to 2000 characters
    http://www.g-loaded.eu/2008/10/24/maximum-url-length/
    """
    content_types = {
        'bed': 'text/x-bed',
        'default': "application/x-www-form-urlencoded",
        'gff3': 'text/x-gff3',
        'fasta': 'text/x-fasta',
        'json': 'application/json',
        "jsonp": "text/javascript",
        "nh": "text/x-nh",
        'phylip': 'text/x-phyloxml+xml',
        'phyloxml': 'text/x-phyloxml+xml',
        'seqxml': 'text/x-seqxml+xml',
        'txt': 'text/plain',
        'text': 'text/plain',
        'xml': 'application/xml',
        'yaml': 'text/x-yaml'
    }

    def __init__(self, name, url=None, verbose=True):
        super(REST, self).__init__(name, url, verbose=verbose)
        print("Initialising %s service (REST)" % self.name)
        self._session = None
        self.last_response = None

    def _get_session(self):
        if self._session is None:
            self._session = self._create_session()
        return self._session

    session = property(_get_session)

    def _create_session(self):
        """
        Creates a normal session using HTTPAdapter
        max retries is defined in the :attr:`MAX_RETRIES`
        """
        if self._verbose:
            print("Create session")
        self._session = requests.session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self._max_retries)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)
        return self._session

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout

    TIMEOUT = property(_get_timeout, _set_timeout)

    def _interpret_returned_request(self, res, frmt):
        # must be a response
        if isinstance(res, Response) is False:
            return res
        if not res.ok:
            reason = res.reason
            print("status is not ok with {0}".format(reason))
            return res.status_code
        if frmt == 'json':
            try:
                return res.json()
            except:
                return res.content
        # finally
        return res.content

    def http_get(self, query, frmt='json', params={}, **kargs):
        """
        * query is the suffix that will be appended to the main url attribute.
        * query is either a string or a list of strings.
        """
        if isinstance(query, list):
            if self._verbose:
                print("Running sync call for a list")
            return [self.get_one(key, frmt, params=params, **kargs) for key in query]
            # return self.get_sync(query, frmt)
        if self._verbose:
            print("Running http_get (single call mode)")
        return self.get_one(query, frmt, params=params, **kargs)

    def get_sync(self, keys, frmt='json', **kargs):
        return [self.get_one(key, frmt=frmt, **kargs) for key in keys]

    def get_one(self, query, frmt='json', params={}, **kargs):
        """
        if query starts with http:// do not use self.url
        """
        if query is None:
            url = self.url
        else:
            if query.startswith("http"):
                # assume we do want to use self.url
                url = query
            else:
                url = '%s/%s' % (self.url, query)
        try:
            kargs['params'] = params
            kargs['timeout'] = self._timeout
            # res = self.session.get(url, **{'timeout':self.timeout, 'params':params})
            if self._verbose:
                print("Target URL :%s" % url)
            res = self.session.get(url, **kargs)

            if res.status_code != 200:
                print("\033[0;33m[WARNING]\033[0m Requests Status is not OK : {0} : {1}".format(res.status_code,
                                                                                                self.response_codes[
                                                                                                    res.status_code]))
            # For avoid too many requests
            time.sleep(1 / self._request_per_sec)

            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            try:
                # for python 3 compatibility
                res = res.decode()
            except:
                pass
            return res
        except Exception as err:
            print(err)
            print("Issue while Your current timeout is {0}. ".format(self._timeout))

    def http_post(self, query, params=None, data=None, frmt='xml', headers=None, files=None, **kargs):
        # query and frmt are services parameters. Others are post parameters
        # NOTE in requests.get you can use params parameter
        # BUT in post, you use data
        # only single post implemented for now unlike get that can be asynchronous
        # or list of queries
        if headers is None:
            headers = {'User-Agent': self.getUserAgent(), 'Accept': self.content_types[frmt]}

        print("Running http_post (single call mode)")
        kargs.update({'query': query})
        kargs.update({'headers': headers})
        kargs.update({'files': files})
        kargs.update({'params': params})
        kargs.update({'data': data})
        kargs.update({'frmt': frmt})
        return self.post_one(**kargs)

    def post_one(self, query, frmt='json', **kargs):
        if query is None:
            url = self.url
        else:
            url = '%s/%s' % (self.url, query)

        try:
            if self._verbose:
                print(url)
            res = self.session.post(url, **kargs)
            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            try:
                return res.decode()
            except:
                return res
        except Exception as err:
            print(err)
            return None

    def getUserAgent(self):
        try:
            urllib_agent = 'Python-urllib/%s' % urllib.request.__version__
        except Exception:
            raise Exception
        clientversion = __version__
        user_agent = 'EBI-Sample-CLient/%s (%s; Python %s; %s) %s' % (clientversion, os.path.basename(__file__, ),
                                                                      platform.python_version(), platform.system(),
                                                                      urllib_agent)
        return user_agent

    def get_headers(self, content='default'):
        """
        :param str content: ste to default that is application/x-www-form-urlencoded
        so that it has the same behaviour as urllib2 (Sept 2014)
        """
        headers = {}
        headers['User-Agent'] = self.getUserAgent()
        headers['Accept'] = self.content_types[content]
        headers['Content-Type'] = self.content_types[content]
        # "application/json;odata=verbose" required in reactome
        # headers['Content-Type'] = "application/json;odata=verbose" required in reactome
        return headers

    def debug_last_response(self):
        print(self.last_response.content)
        print(self.last_response.reason)
        print(self.last_response.status_code)

    def http_put(self):
        raise NotImplementedError

    def http_delete(self):
        raise NotImplementedError


def tolist(data, verbose=True):
    """
    Transform an object into a list if possible

    :param data: a list, tuple, or simple type (e.g. int)
    :return: a list
    """
    if isinstance(data, list) or isinstance(data, tuple):
        return data  # nothing to do
    elif isinstance(data, float):
        return [data]
    elif isinstance(data, int):
        return [data]
    elif isinstance(data, str):
        return [data]
    else:
        try:
            data = data.tolist()
            return data
        except:
            if verbose:
                print("not known type. cast to list")
            return list(data)


def list2string(data, sep=",", space=True):
    """
    Transform a list into a string

    :param list data: list of items that have a string representation.
        the input data could also be a simple object, in which case
        it is simply returned with a cast into a string
    :param str sep: the separator to be use
    """
    data = tolist(data)
    if space is True:
        sep += " "
    res = sep.join([str(x) for x in data])
    return res


def check_param_in_list(param, valid_values, name=None):
    """
    Checks that the value of param is amongst valid

    :param param: a parameter to be checked
    :param list valid_values: a list of values

    ::

        check_param_in_list(1, [1,2,3])
        check_param_in_list(mode, ["on", "off"])
    """
    if isinstance(valid_values, list) is False:
        raise TypeError(
            "the valid_values second argument must be a list of valid values. {0} was provided.".format(valid_values))

    if param not in valid_values:
        if name:
            msg = "Incorrect value provided for {} ({})".format(name, param)
        else:
            msg = "Incorrect value provided (%s)" % param
        msg += "    Correct values are %s" % valid_values
        raise ValueError(msg)


def to_json(dictionary):
    return json.dumps(dictionary)


def check_range(value, a, b, strict=False):
    """
    Check that a value lies in a given range
    :param value: value to test
    :param a: lower bound
    :param b: upper bound
    :return: nothing
    """

    if strict is True:
        if value <= a:
            raise ValueError(" {} must be greater (or equal) than {}".format(value, a))
        if value >= b:
            raise ValueError(" {} must be less (or less) than {}".format(value, b))
    elif strict is False:
        if value < a:
            raise ValueError(" {} must be greater than {}".format(value, a))
        if value > b:
            raise ValueError(" {} must be less than {}".format(value, b))


class easyXML(object):
    """
    class to ease the introspection of XML documents.
    This class uses the standard xml module as well as the package BeautifulSoup
    to help introspecting the XML documents.
    """

    def __init__(self, data):
        """
        :param data: an XML document format

        The data parameter must be a string containing the XML document. If you
        have an URL instead, use :class:`readXML`

        """
        self.data = data[:]

        try:
            self.root = ET.fromstring(self.data)
        except:
            self.root = self.data[:]
        self._soup = None
        self.prettify = self.soup.prettify
        self.findAll = self.soup.findAll

    def getchildren(self):
        """
        returns all children of the root XML document
        This is just an alias to self.soup.getchildren()
        """
        return self.root.getchildren()

    def _get_soup(self):
        if self._soup is None:
            self._soup = bs4.BeautifulSoup(self.data)
        return self._soup

    soup = property(_get_soup, doc="Returns the beautiful soup instance")

    def __str__(self):
        txt = self.soup.prettify()
        return txt

    def __getitem__(self, i):
        return self.findAll(i)


class readXML(easyXML):
    """
    Read XML and converts to beautifulsoup data structure
    easyXML accepts as input a string. This class accepts a filename instead
    inherits from easyXML
    """

    def __init__(self, filename):
        url = urlopen(filename, "r")
        self.data = url.read()
        super(readXML, self).__init__(self.data)
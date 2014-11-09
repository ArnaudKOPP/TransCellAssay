"""
Base Class for REST services, inspired by bioservices
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import os
import socket
import platform
import time
import webbrowser
import binascii
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError
import requests  # replacement for urllib2 (2-3 times faster)
from requests.models import Response
import aiohttp

__all__ = ["Service"]
DEBUG = True

class ServiceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Service():
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
            requests may be retricted. Currently implemented for REST only
        """
        self.request_per_sec = request_per_sec
        self.url = url
        self.timeout = 30
        self.max_retries = 3
        self.async_concurrent = 50
        self.async_threshold = 10
        try:
            if self.url is not None:
                urlopen(self.url)
        except Exception:
            if verbose:
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
        from TransCellAssay.IO.Rest import xml

        return xml.easyXML(res)

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
        """Save string object into a file converting into binary"""
        with open(filename, 'wb') as f:
            try:
                # python3
                newres = binascii.a2b_base64(bytes(data, "utf-8"))
            except:
                newres = binascii.a2b_base64(data)
            f.write(newres)


class RESTBase(Service):
    _service = "REST"

    def __init__(self, name, url=None, verbose=True):
        super(RESTBase, self).__init__(name, url, verbose=verbose)
        print("Initialising %s service (REST)" % self.name)
        self.last_response = None

    def http_get(self):
        raise NotImplementedError

    def http_post(self):
        raise NotImplementedError

    def http_put(self):
        raise NotImplementedError

    def http_delete(self):
        raise NotImplementedError


class RESTService(RESTBase):
    """
    Class to manipulate REST Service
    """

    def __init__(self, name, url=None, verbose=True):
        """
        :param name: a name like Kegg Reactome
        :param url: url of rest service
        :param verbose: verbose
        """
        super(RESTService, self).__init__(name, url, verbose=verbose)
        self.verbose = verbose
        if self.verbose:
            print("\033[0;33m[WARNING]\033[0m Use REST class instead of RESTService")
        self.trials = 5
        self.timesleep = 1

    def getUserAgent(self):
        try:
            import urllib

            urllib_agent = 'Python-urllib/%s' % urllib.request.__version__
        except Exception:
            raise Exception
        ClientVersion = ''
        user_agent = 'EBI-Sample-CLient/%s (%s; Python %s; %s) %s' % (ClientVersion, os.path.basename(__file__, ),
                                                                      platform.python_version(), platform.system(),
                                                                      urllib_agent)
        return user_agent

    def request(self, path, format='xml', baseUrl=True):
        """
        Send a request via an url to the web service
        :param path: the request will be formed as self.url+/+path
        :param format:
        :param baseUrl:
        :return: res
        """
        for i in range(self.trials):
            res = self._get_requests(path, format=format, baseUrl=baseUrl)
            if res is not None:
                break
            print("\033[0;33m[WARNING]\033[0m Request seemed to have failed.")
            if i != self.trials - 1:
                print("Trying again {}/{}".format(i + 1, self.trials))
            time.sleep(self.timesleep)
        return res

    def http_get(self, path, format='xml', baseUrl=True):
        return self.request(path, format=format, baseUrl=baseUrl)

    def _get_requests(self, path, format='xml', baseUrl=True):
        if path.startswith(self.url):
            url = path
        elif baseUrl is False:
            url = path
        else:
            url = self.url + "/" + path

        if self.verbose:
            print("REST: %s request begins" % self.name)
            print("--Fetching url=%s" % url)

        if len(url) > 2000:
            raise ValueError("URL length (%s) exceeds 2000. Please use a different URL" % len(url))

        try:
            res = urlopen(url).read()
            if format == 'xml':
                if self.easyXMLConversion:
                    try:
                        res = self.easyXML(res)
                    except Exception as e:
                        print(e)
            self.last_response = res
            return res
        except socket.timeout:
            raise socket.timeout(
                "Time out. consider increasing the timeout attribute (currently set to {})".format(self.timeout))

    def requestPost(self, requestUrl, params, extra=None):
        """
        request with a post method
        :param requestUrl: the entire URL to request
        :param params: the dictionary of param/value pairs
        :param extra:an additional string to add after the params if
            needed. Could be usefule if a parameter/value can not be added to the
            dictionary. For instance is a parameter has several values
            Solved in requests module.
        note:: this is a HTTP POST request
        note:: use only by ::`ncbiblast` service so far.
        """
        requestData = urlencode(params)
        print(requestData)
        if extra is not None:
            requestData += extra
        # concatenate the two parts
        # Errors are indicated by HTTP status code.
        try:
            # set HTTP User-agent
            user_agent = self.getUserAgent()
            http_headers = {'User-Agent': user_agent}
            print(requestUrl)
            req = Request(requestUrl, None, http_headers)
            # Make submission (HTTP, POST)
            print(req)
            reqH = urlopen(req, requestData)
            jobId = reqH.read()
            reqH.close()
        except HTTPError as e:
            print(e)
            raise
        return jobId

    def urlencode(self, params):
        """
        Returns a string compatible with a url request
        The pair of key/value are converted into a single string by concatenated
        the "&key=value" string for each key/value in the dictionary.
        :param params: keys are parameters
        :return:
        """
        if isinstance(params, dict) is False:
            raise TypeError("Params must be a dictionary.")
        postData = urlencode(params)
        return postData


class REST(RESTBase):
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
        self._session = None
        self.FAST_SAVE = True

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
        if DEBUG:
            print("Create session")
        self._session = requests.session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)
        return self._session

    def _get_timeout(self):
        return self.timeout

    def _set_timeout(self, timeout):
        self.timeout = timeout

    TIMEOUT = property(_get_timeout, _set_timeout)

    def _process_get_request(self, url, session, frmt, data=None, **kwargs):
        try:
            res = session.get(url, **kwargs)
            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            return res
        except Exception:
            return None

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
                return res
        # finally
        return res.content

    def _apply(self, iterable, fn, *args, **kwargs):
        return [fn(x, *args, **kwargs) for x in iterable if x is not None]

    def _get_async2(self, keys, frmt="json", params={}):
        import asyncio
        # # DEVELOPMENT SANDBOX for TRYING
        session = self.session
        try:
            urls = self._get_all_urls(keys, frmt)

            @asyncio.coroutine
            def loop(url):
                loop = asyncio.get_event_loop()
                future = loop.run_until_complete(None, requests.get, url)
                response = yield from future
                return response

            loop = asyncio.get_event_loop()
            loop.run_until_complete(loop())

        except Exception as e:
            print("Error caught in async. ", e)
            return []

    def _get_async(self, keys, frmt='json', params={}):
        # does not work under python3 so local import
        import grequests

        session = self._session
        try:
            urls = self._get_all_urls(keys, frmt)
            rs = (grequests.get(url, session=session, params=params) for key, url in zip(keys, urls))
            # execute them
            ret = grequests.map(rs, size=min(self.async_concurrent, len(keys)))
            self.last_response = ret
            return ret
        except Exception as e:
            print("Error caught in async. ", e)
            return []

    def _get_all_urls(self, keys, frmt=None):
        return ('%s/%s' % (self.url, query) for query in keys)

    def get_async(self, keys, frmt='json', params={}, **kargs):
        ret = self._get_async(keys, frmt, params=params, **kargs)
        return self._apply(ret, self._interpret_returned_request, frmt)

    def get_sync(self, keys, frmt='json', **kargs):
        return [self.get_one(key, frmt=frmt, **kargs) for key in keys]

    def http_get(self, query, frmt='json', params={}, **kargs):
        """
        * query is the suffix that will be appended to the main url attribute.
        * query is either a string or a list of strings.
        * if list is larger than ASYNC_THRESHOLD, use asynchronous call.
        """
        if isinstance(query, list) and len(query) > self.async_threshold:
            if DEBUG:
                print("Running async call for a list")
            # Not implemented yet a sync funtions with Requests package, will be available in REST2 with aiohttp
            # return self.get_async(query, frmt, params=params, **kargs)
            return [self.get_one(key, frmt, params=params, **kargs) for key in query]
        if isinstance(query, list) and len(query) <= self.async_threshold:
            if DEBUG:
                print("Running sync call for a list")
            return [self.get_one(key, frmt, params=params, **kargs) for key in query]
            # return self.get_sync(query, frmt)
        # OTHERWISE
        if DEBUG:
            print("Running http_get (single call mode)")
        # return self.get_one(**{'frmt': frmt, 'query': query, 'params':params})
        return self.get_one(query, frmt, params=params, **kargs)

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
            kargs['timeout'] = self.timeout
            # res = self.session.get(url, **{'timeout':self.timeout, 'params':params})
            res = self.session.get(url, **kargs)

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
            print("Issue while Your current timeout is {0}. ".format(self.timeout))

    def http_post(self, query, params=None, data=None, frmt='xml', headers=None, files=None, **kargs):
        # query and frmt are bioservices parameters. Others are post parameters
        # NOTE in requests.get you can use params parameter
        # BUT in post, you use data
        # only single post implemented for now unlike get that can be asynchronous
        # or list of queries
        if headers is None:
            headers = {}
            headers['User-Agent'] = self.getUserAgent()
            headers['Accept'] = self.content_types[frmt]

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
            import urllib

            urllib_agent = 'Python-urllib/%s' % urllib.request.__version__
        except Exception:
            raise Exception
        ClientVersion = ''
        user_agent = 'EBI-Sample-CLient/%s (%s; Python %s; %s) %s' % (ClientVersion, os.path.basename(__file__, ),
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

    def debug_message(self):
        print(self.last_response.content)
        print(self.last_response.reason)
        print(self.last_response.status_code)


class REST2(RESTBase):
    """
    The ideas (sync/async) and code using requests were inspired from the chembl
    python wrapper but significantly changed.

    This class is variant of REST by use of aiohttp for async http request

    IN DEV !!!!

    Get one value::
    s = REST("test", "https://www.ebi.ac.uk/chemblws")
    res = s.get_one("targets/CHEMBL2476.json", "json")
    res['organism']
    u'Homo sapiens'

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
        self._session = None
        self.FAST_SAVE = True
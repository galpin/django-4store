# Created by Martin Galpin (m@66laps.com)
#
# Copyright (C) 2010 66laps Limited.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

import httplib
import urllib
import os
import json
from urlparse import urlparse

from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from rdflib import URIRef
from HTTP4Store import HTTP4Store

from fourstore.test import Base4StoreTest
from fourstore.utils import get_rdf_files
from fourstore.fixtures import find_first_fixture

from fourstore.utils import reverse_django_meta_keys

# This app label
APP_LABEL = "fourstore"

# Basic SPARQL query based on the test fixtures
TEST_SPARQL = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?who WHERE { ?who a foaf:Person . }
"""

# Expected rdflib response for the above query
TEST_RDFLIB_RESPONSE = [{u'who': URIRef('http://www.example.org/people/Melissa_Robinson')},
                        {u'who': URIRef('http://www.example.org/people/Ace_Ventura')}]

# Epected SPARQL JSON response for the above query
TEST_JSON_RESPONSE = {
    "head":{"vars":["who"]},
    "results": {
        "bindings":[
            {"who":{"type":"uri","value":"http://www.example.org/people/Melissa_Robinson"}},
            {"who":{"type":"uri","value":"http://www.example.org/people/Ace_Ventura"}}
            ]
        }
    }

class FourstoreTests(Base4StoreTest):
    kbfixtures = ["ace.n3", "melissa.rdf"]

    def setUp(self):
        Base4StoreTest.setUp(self)
        # test the HTTP server is running
        self.host = "localhost:%d" % self.port
        url = urlparse(settings.SPARQL_ENDPOINT)
        self.store = HTTP4Store("%s://%s" % (url.scheme, url.netloc))

    def tearDown(self):
        Base4StoreTest.tearDown(self)

        # test the HTTP server is no longer running
        self.assertRaises(Exception, crude_http_request, self.host, "/test/")

    def test_sparql_query(self):
        self.assertEqual(200, crude_http_request(self.host, "/test/"))

        # test a SPARQL query based against our test fixtures
        self.assertEqual(TEST_RDFLIB_RESPONSE, self.store.sparql(TEST_SPARQL))

class ManagementCommandTests(TestCase):
    def test_get_files(self):
        expected = [find_first_fixture("ace.n3", APP_LABEL)]
        self.assertEquals(expected, get_rdf_files(expected))

        expected = [find_first_fixture("melissa.rdf", APP_LABEL)]
        self.assertEquals(expected, get_rdf_files(expected))

        fixtures_dir = os.path.dirname(expected[0])
        all_files = get_rdf_files([fixtures_dir])
        self.assertTrue(find_first_fixture("ace.n3", APP_LABEL) in all_files)
        self.assertTrue(find_first_fixture("melissa.rdf", APP_LABEL) in all_files)

    def test_get_files_recusrive(self):
        app_dir = os.path.dirname(os.path.abspath(__file__))
        all_files = get_rdf_files([app_dir], recursive=True)
        fixtures_dir = os.path.join(app_dir, "fixtures")
        self.assertTrue(os.path.join(fixtures_dir, "ace.n3") in all_files)
        self.assertTrue(os.path.join(fixtures_dir, "melissa.rdf") in all_files)

class FixtureTests(TestCase):
    def test_find_first_fixture(self):
        self.assertNotEqual(None, find_first_fixture("ace.n3", APP_LABEL))
        self.assertEqual(None, find_first_fixture("truman.n3", APP_LABEL))
        self.assertNotEqual(None, find_first_fixture("melissa.rdf"))

class ViewTests(Base4StoreTest):
    kbfixtures = ["ace.n3", "melissa.rdf"]
    urls = "fourstore.test_urls"

    def setUp(self):
        Base4StoreTest.setUp(self)
        self.client = Client()

    def test_sparql_proxy(self):
        response = self.client.post("/sparql/",
                                    urllib.urlencode({"query":TEST_SPARQL}),
                                    content_type="application/x-www-form-urlencoded",
                                    HTTP_ACCEPT="application/json")
        self.assertEquals(TEST_JSON_RESPONSE, json.loads(response.content))

    def test_sparql_proxy_http_verbs(self):
        response = self.client.put("/sparql/",
                                   urllib.urlencode({"query":TEST_SPARQL}),
                                   content_type="application/x-www-form-urlencoded")
        self.assertEquals(400, response.status_code)

        response = self.client.delete("/sparql/")
        self.assertEquals(400, response.status_code)

    def test_sparql_proxy_bad_content_type(self):
        response = self.client.put("/sparql/", {"query":TEST_SPARQL})
        self.assertEquals(400, response.status_code)

class Utiltests(TestCase):
    def test_reverse_django_meta_keys(self):
        django_http_meta = {
            "CONTENT_LENGTH": "",
            "CONTENT_TYPE": "",
            "HTTP_ACCEPT_ENCODING": "",
            "HTTP_ACCEPT_LANGUAGE": "",
            "HTTP_ACCEPT": "",
            "HTTP_HOST": "",
            "HTTP_REFERER": "",
            "HTTP_USER_AGENT": "",
            "QUERY_STRING": "", # should be ignored
            "REMOTE_ADDR": "",  # should be ignored
            }
        http_meta = {
            "Content-Length": "",
            "Content-Type": "",
            "Accept-Encoding": "",
            "Accept-Language": "",
            "Accept": "",
            "Host": "",
            "Referer": "",
            "User-Agent": "",
            }
        self.assertEquals(http_meta, reverse_django_meta_keys(django_http_meta))

def crude_http_request(host, path, method="GET"):
    connection = httplib.HTTPConnection(host)
    connection.request(method, path)
    response = connection.getresponse()
    return response.status

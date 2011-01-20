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
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

import httplib
import os

from django.test import TestCase
from django.conf import settings

from rdflib import URIRef
from HTTP4Store import HTTP4Store

from fourstore.test import Base4StoreTest
from fourstore.utils import get_rdf_files
from fourstore.fixtures import find_first_fixture

# This app label
APP_LABEL = "fourstore"

# Basic SPARQL query based on the test fixtures
TEST_SPARQL = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?who WHERE { ?who a foaf:Person . }
"""

# Expected response for the above query
TEST_RESPONSE = [{u'who': URIRef('http://www.example.org/people/Melissa_Robinson')},
                 {u'who': URIRef('http://www.example.org/people/Ace_Ventura')}]


class FourstoreTests(Base4StoreTest):
    kbfixtures = ["ace.n3", "melissa.rdf"]

    def setUp(self):
        Base4StoreTest.setUp(self)

        # test the HTTP server is running
        self.host = "localhost:%d" % self.port
        self.assertEqual(200, crude_http_request(self.host, "/test/"))

        self.store = HTTP4Store(settings.SPARQL_ENDPOINT)

    def tearDown(self):
        Base4StoreTest.tearDown(self)

        # test the HTTP server is no longer running
        self.assertRaises(Exception, crude_http_request, self.host, "/test/")

    def test_sparql_query(self):
        # test a SPARQL query based against our test fixtures
        self.assertEqual(TEST_RESPONSE, self.store.sparql(TEST_SPARQL))

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

class FixtureTests(TestCase):
    def test_find_first_fixture(self):
        self.assertNotEqual(None, find_first_fixture("ace.n3", APP_LABEL))
        self.assertEqual(None, find_first_fixture("truman.n3", APP_LABEL))
        self.assertNotEqual(None, find_first_fixture("melissa.rdf"))

def crude_http_request(host, path, method="GET"):
    connection = httplib.HTTPConnection(host)
    connection.request(method, path)
    response = connection.getresponse()
    return response.status

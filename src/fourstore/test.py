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

from subprocess import CalledProcessError

from django.test import TestCase
from django.conf import settings

from fourstore.server import start_4store_server, stop_4store_server
from fourstore.fixtures import find_first_fixture

class Base4StoreTest(TestCase):
    '''
    A base test case that automatically creates a 4store
    backend, imports the specified test fixtures and starts
    a SPARQL HTTP server. Essentially, it creates an isolated
    4store environment for each test case and the Django
    setting.SPARQL_ENDPOINT will automatically be set.
    '''
    kbname = "django_4store_test"
    port = 6666
    kbfixtures = []

    def setUp(self):
	try:
            files = [find_first_fixture(f) for f in self.kbfixtures]
            start_4store_server(self.kbname, self.port, files)
            settings.SPARQL_ENDPOINT = "http://localhost:%d/" % self.port
        except CalledProcessError:
	    self.fail('Unable to create temporary 4store')

    def tearDown(self):
        stop_4store_server(self.kbname, self.port)

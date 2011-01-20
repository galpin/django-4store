# This file is part of django-4store.
#
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

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from fourstore.server import start_4store_server, stop_4store_server
from fourstore.utils import get_rdf_files

import time
import signal
import sys

HELP_MESSAGE = \
"""Creates and starts a 4store backend and HTTP server.

Importing data will overwrite existing models."""


def signal_handler(signal, frame):
    print 'Shutting down 4store servers!'
    stop_4store_server(settings.FOURSTORE_KBNAME, settings.FOURSTORE_PORT)
    sys.exit(0)

class Command(BaseCommand):
    args = "<file.n3 file.rdf dir dir file.n3...>"
    help = HELP_MESSAGE

    def handle(self, *args, **options):
        try:
            files = get_rdf_files(args)
            if files:
                print "Importing the following files: %s." % files
            start_4store_server(settings.FOURSTORE_KBNAME, settings.FOURSTORE_PORT, files)
            print "4store server is running at http://localhost:%d/" % settings.FOURSTORE_PORT
            print "Quit the server with CONTROL-C."
            signal.signal(signal.SIGINT, signal_handler)
            while 1:
                time.sleep(5000)
                continue
        except AttributeError:
            raise CommandError("You must set FOURSTORE_KBNAME and FOURSTORE_PORT in your settings.py.")

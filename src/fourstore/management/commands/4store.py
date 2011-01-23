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
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.


import time
import signal
import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from fourstore.server import \
     fourstore_backend, fourstore_httpd, \
     fourstore_kill

def signal_handler(signal, frame):
    print 'Shutting down 4store servers!'
    fourstore_kill(settings.FOURSTORE_KBNAME, settings.FOURSTORE_PORT)
    sys.exit(0)

class Command(BaseCommand):
    help = """Starts the 4store HTTP server."""

    def handle(self, *args, **options):
        try:
            fourstore_backend(settings.FOURSTORE_KBNAME)
            fourstore_httpd(settings.FOURSTORE_KBNAME, settings.FOURSTORE_PORT)
            print "4store server is running at http://localhost:%d/" % settings.FOURSTORE_PORT
            print "Quit the server with CONTROL-C."
            signal.signal(signal.SIGINT, signal_handler)
            while 1:
                time.sleep(5000)
                continue
        except AttributeError:
            raise CommandError("You must set FOURSTORE_KBNAME and FOURSTORE_PORT in your settings.py.")
        except OSError:
            raise CommandError("Please ensure 4store is installed and accessible in $PATH.")


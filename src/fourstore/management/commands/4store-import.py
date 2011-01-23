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

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from fourstore.server import fourstore_create, fourstore_import
from fourstore.utils import get_rdf_files

HELP_MESSAGE = """Creates and imports data into a 4store knowledge base."""

class Command(BaseCommand):
    args = "<file.n3 file.rdf dir dir file.n3...>"
    help = HELP_MESSAGE
    option_list = BaseCommand.option_list  + (
        make_option("--recursive", "-r",
                    action="store_true",
                    dest="recursive",
                    default=False,
                    help="Recursively import directories."),
        )

    def handle(self, *args, **options):
        try:
            files = get_rdf_files(args, recursive=options["recursive"])
            if files:
                print "Importing the following files: %s." % files
            fourstore_create(settings.FOURSTORE_KBNAME)
            fourstore_import(settings.FOURSTORE_KBNAME, files)
        except AttributeError:
            raise CommandError("You must set FOURSTORE_KBNAME and FOURSTORE_PORT in your settings.py.")

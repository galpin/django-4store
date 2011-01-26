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

from os import listdir
from os.path import join, splitext, isdir

# Valid RDF file extensions (supported by 4s-import)
RDF_EXTENSIONS = (".rdf", ".n3")

def get_rdf_files(paths, recursive=False):
    """
    Get all the path of all valid RDF files in the specified list. If a
    paths is a directory, all RDF files within this directory will be
    returned. Additionally, if recurive is True, the directory will be
    searched recursively.
    """
    all_files = set()
    for path in paths:
        if isdir(path):
            for f in listdir(path):
                f = join(path, f)
                if recursive and isdir(f):
                    all_files.update(get_rdf_files([f]))
                if splitext(f)[1] in RDF_EXTENSIONS:
                    all_files.add(f)
        else:
            all_files.add(path)
    return list(all_files)

def reverse_django_meta_keys(meta):
    """
    Convert the a dict of Django ``HttpRequest.META`` headers to a dict
    suitable for use with ``httplib``.

    With the exception of ``CONTENT_TYPE`` and ``CONTENT_LENGTH``, this
    method will convert all keys starting with ``HTTP_`` to upper-camel-case
    and replace all underscores with hyphens. For example,
    ``HTTP_ACCEPT_ENCODING`` becomes ``Accept-Encoding``.

    A new dict is returned containing only the keys and values from the
    original dict that match these rules.

    This reverses the process internally applied by Django to a request.
    """
    def transform(str):
        return "-".join([s.lower().capitalize() for s in str.split("_")])
    http_headers = {}
    for key in meta.keys():
        if key.startswith("HTTP_"):
            http_headers.update({transform(key[5:]): meta[key]})
        elif key in ("CONTENT_TYPE", "CONTENT_LENGTH"):
            http_headers.update({transform(key): meta[key]})
    return http_headers

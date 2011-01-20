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

def get_rdf_files(paths):
    """
    Get all the path of all valid RDF files in the specified list. If a
    paths is a directory, all RDF files within this directory will be
    returned.
    """
    all_files = set()
    for path in paths:
        if isdir(path):
            files = [join(path, f) for f in listdir(path)
                     if splitext(join(path, f))[1] in RDF_EXTENSIONS]
            all_files.update(set(files))
        else:
            all_files.add(path)
    return list(all_files)

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

from subprocess import call, check_call

def fourstore_httpd(name, port):
    """
    Start the 4store HTTP server on a specified port.
    """
    check_call(["4s-httpd", "-p", str(port), name])

def fourstore_kill(name, port):
    """
    Stops any running instances of 4s-backend and 4s-httpd.
    """
    call(["pkill", "-f", "4s-backend %s" % name])
    call(["pkill", "-f", "4s-httpd -p %d" % port])

def fourstore_create(name):
    """
    Create a new 4store backend with the specified name.
    """
    check_call(["4s-backend-setup", name])
    check_call(["4s-backend", name])

def fourstore_import(name, files):
    """
    Import the files into a specified 4store knowledge base.
    """
    check_call(["4s-import", name] + list(files))

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

def start_4store_server(name, port, files=[]):
    """
    Start a new instance of 4store, imports any specified files
    and runs the 4s-httpd server.
    """
    check_call(["4s-backend-setup", name])
    check_call(["4s-backend", name])
    if files:
        check_call(["4s-import", name] + list(files))
    check_call(["4s-httpd", "-p", str(port), name])

def stop_4store_server(name, port):
    """
    Stops any running instances of 4s-backend and 4s-httpd.
    """
    call(["pkill", "-f", "4s-backend %s" % name])
    call(["pkill", "-f", "4s-httpd -p %d" % port])


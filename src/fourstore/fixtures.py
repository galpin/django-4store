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

import os

from django.db.models import get_apps, get_app

def find_first_fixture(filename, app_label=None):
    """
    Find the first fixture that matches a specified filename
    and within an optional installed app.
    """
    if not app_label:
        app_module_paths = get_fixture_paths()
    else:
        app_module_paths = get_app_fixture_paths(get_app(app_label))

    for path in app_module_paths:
        filepath = os.path.join(path, filename)
        if os.path.exists(filepath):
            return filepath

def get_fixture_paths():
    """Get the fixture path for all installed apps."""
    app_fixture_paths = []
    for app in get_apps():
        app_fixture_paths.extend(get_app_fixture_paths(app))
    return app_fixture_paths

def get_app_fixture_paths(app):
    """Get the fixture path for a specified app."""
    # originates in django/core/models/loading.py
    app_module_paths = []
    if hasattr(app, '__path__'):
        #It's a 'models/' subpackage
        for path in app.__path__:
            app_module_paths.append(path)
    else:
        # It's a models.py module
        app_module_paths.append(os.path.dirname(app.__file__))
    return [os.path.join(path, "fixtures") for path in app_module_paths]


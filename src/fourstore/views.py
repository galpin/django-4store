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

import httplib
import urlparse

from django.http import HttpResponse, HttpResponseBadRequest

from fourstore.utils import reverse_django_meta_keys

def sparql_proxy(request, sparql_endpoint):
    """
    Tunnel an HTTP request to SPARQL endpoint and wait for a respnose..

    The given HTTP request is relayed to the specified SPARQL endpoint
    via this view. This allows us to make requests to arbitary endpoints
    regardless of domain (and cross-domain restrictions).

    Note: There is no attempt to "sanitise" the given request.
    """
    if request.method not in ("GET", "POST"):
        return HttpResponseBadRequest("Only POST and GET verbs are supported.")

    if request.META["CONTENT_TYPE"] != "application/x-www-form-urlencoded":
        return HttpResponseBadRequest("Content-type must be application/x-www-form-urlencoded.")

    headers = reverse_django_meta_keys(request.META)

    # use httplib to set the correct content-length
    if "Content-Length" in headers:
        del headers["Content-Length"]

    params = request.GET if request.method == "GET" else request.POST

    url = urlparse.urlparse(sparql_endpoint)
    connection = httplib.HTTPConnection(url.netloc)

    connection.request(request.method, "/sparql/", params.urlencode(), headers)
    response = connection.getresponse()

    our_response = HttpResponse(response.read(),
                                content_type=response.getheader("Content-Type"))
    our_response.status_code = response.status

    connection.close()

    return our_response

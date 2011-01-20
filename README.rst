django-4store
=============

:Author:
    Martin Galpin
:Contact:
    m@66laps.com

django-4store is a small Django application that makes developing
apps with the `4Store RDF database`_ easier.

Installation
------------

django-4store is on `PyPi`_ for ``easy_install`` or `buildout`_::

    $ easy_install django-4store

Alternatively, clone the repository and place it either in your Django
project or within your ``$PYTHONPATH``::

    $ git clone git://github.com/66laps/django-4store.git

Configuration
-------------

Edit your ``settings.py`` and add ``fourstore`` to the end of
``INSTALLED_APPS``.

You must also add two additional settings to ``settings.py``::

    FOURSTORE_KBNAME = "demo"  # Name of 4store knowledge base
    FOURSTORE_PORT = 6667      # Port for 4store HTTP server

It is recommended (but not required) that you also set a constant to
the SPARQL endpoint at the same time::

    SPARQL_ENDPOINT = "http://localhost:6667"

Code that depends on this endpoint URL will continue to work during
testing (see `Test Cases`_.)

Management Command
------------------

A simple management command is provided that quickly creates a 4store
knowledge base, imports any specified files and starts the 4store
HTTP server.

For example, to start a 4store server and import two files::

    $ python manage.py 4store rdf/card.rdf rdf/myself.n3
    ...
    Importing the following files: ['rdf/card.rdf', 'rdf/myself.n3'].
    4store[53904]: backend-setup.c:185 erased files for KB demo
    4store[53904]: backend-setup.c:310 created RDF metadata for KB demo
    4store server is running at http://localhost:6667/
    Quit the server with CONTROL-C.

You can also specify directories together with files. In this case,
all valid RDF files within the directory will be imported. This means
that the previous example is equivalent to::

    $ python manage.py 4store rdf/
    ...

Importing data will overwrite any existing content in the knowledge
base. If you wish to start 4store without importing any data, simply
omit the files::

   $ python manage.py 4store
   ...

.. _`Test Cases`:

Test Cases
----------

A subclass of ``django.test.Testcase`` is included. This provides a
mechanism for starting an isolated 4store server and automatically
importing test fixtures.

For example, the following test case can be used to test any 4store
dependant code::

    from django.conf import settings
    from HTTP4Store import HTTP4Store

    from fourstore.test import Base4StoreTest

    class MySemanticTestCase(Base4StoreTest):
        kbfixtures = ["card.rdf", "someone.n3"]

	def test_something(self):
	    store = HTTP4Store(settings.SPARQL_ENDPOINT)
	    response = store.sparql("SELECT * WHERE { ?s ?p ?o . } ")
	    self.assertEquals(..., response)

Test fixtures should be placed within the ``fixtures`` directory of
the app under testing (note the class variable is ``kbfixtures``).

The Django setting attribute ``settings.SPARQL_ENDPOINT`` is
automatically updated to the current endpoint URL.

The server is reinitialised between tests and its operation is dependant
on ``setUp`` and ``tearDown``. If you need to override these methods,
make sure that you still call the parent implementations::

    class MySemanticTestCase(Base4StoreTest):
        ...
        def setUp(self):
             Base4StoreTest.setUp(self)
	     // do something

        def tearDown(self):
            Base4StoreTest.tearDown(self)
            // do something

License
-------

This library is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301 USA

.. _`4Store RDF database`: http://www.4store.org
.. _`PyPI`: http://pypi.python.org/pypi?name=django-4store
.. _`buildout`: http://www.buildout.org/

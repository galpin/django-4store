import os

DEBUG = TEMPLATE_DEBUG = True
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/shorturls.db'
INSTALLED_APPS = ['fourstore']
ROOT_URLCONF = ['fourstore.urls']
TEMPLATE_DIRS = os.path.join(os.path.dirname(__file__), 'tests', 'templates')

FOURSTORE_KBNAME = "django_4store"
FOURSTORE_PORT = 6667
SPARQL_ENDPOINT = "http://localhost:6667"

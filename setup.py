import os

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-4store",
    version = "0.2.1",
    url = "http://github.com/66laps/django-fourstore",
    license = "LGPL v3",
    description = "A small Django application that makes developing with the 4Store RDF database easier.",
    long_description = read('README.rst'),
    author = "Martin Galpin",
    author_email = "m@66laps.com",
    packages = find_packages("src"),
    package_dir = { "": "src" },
    install_requires = ["setuptools"],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        ]
    )

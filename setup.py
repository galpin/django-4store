from setuptools import setup, find_packages

setup(
    name = "django-4store",
    version = "0.1",
    url = "http://github.com/66laps/django-fourstore",
    license = "LGPL v3",
    description = "A collection of tools for using 4store with Django.",
    author = "Martin Galpin",
    packages = find_packages("src"),
    package_dir = { "": "src" },
    install_requires = ["setuptools"],
    )

# Microngo

[![Documentation Status](https://readthedocs.org/projects/microngo/badge/?version=latest)](https://microngo.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/emsuryadi/Microngo/blob/master/LICENSE)
[![Python Version Support](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

Microngo is small, fast, and lightweight MongoDB toolkit for python.

### Install

Install using PIP:

	pip install Microngo

or install from source:

	python setup.py install

### Documentation

The documentation can be found here [https://microngo.readthedocs.io/en/latest/](https://microngo.readthedocs.io/en/latest/ "Microngo Documentation")

### Testing

Install requirements and package:

	pip install -r requirements-test.txt
	python setup.py install

Test:

	nosetests -v --with-coverage --cover-package=microngo test.py
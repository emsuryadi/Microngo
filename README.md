# Microngo

[![Build Status](https://travis-ci.org/emsuryadi/Microngo.svg?branch=master)](https://travis-ci.org/emsuryadi/Microngo)
[![Coverage Status](https://coveralls.io/repos/github/emsuryadi/Microngo/badge.svg?branch=master)](https://coveralls.io/github/emsuryadi/Microngo?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/Microngo.svg)](https://pypi.org/project/Microngo/)
[![Documentation Status](https://readthedocs.org/projects/microngo/badge/?version=latest)](https://microngo.emsuryadi.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/emsuryadi/Microngo/blob/master/LICENSE)
[![Python Version Support](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

Microngo is small, fast, and lightweight MongoDB toolkit for python.

### Install

Install using PIP:

	pip install Microngo

or install from source:

	python setup.py install

### Documentation

The documentation can be found here [https://microngo.emsuryadi.com/](https://microngo.emsuryadi.com/ "Microngo Documentation")

### Testing

Install requirements and package:

	pip install -r requirements-test.txt
	python setup.py install

Test:

	nosetests -v --with-coverage --cover-erase --cover-package=microngo test.py
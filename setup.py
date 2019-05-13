#!/usr/bin/env python

import setuptools
from distutils.core import setup

VERSION				= '0.1.1'
DESCRIPTION			= 'Microngo is small, fast, and lightweight MongoDB toolkit for python'
LONG_DESCRIPTION	= open('README.md', 'r').read()

setup(
	name							= 'Microngo',
	version							= VERSION,
	description						= DESCRIPTION,
	long_description				= LONG_DESCRIPTION,
	long_description_content_type	= 'text/markdown',
	author							= 'Em Suryadi',
	author_email					= 'me@emsuryadi.com',
	license							= 'MIT',
	url								= 'https://microngo.emsuryadi.com/',
	packages						= ['microngo'],
	install_requires				= ['pymongo>=3.7.0'],
	classifiers						= [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Database',
		'Topic :: Software Development :: Libraries :: Python Modules',
	]
)
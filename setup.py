#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='sportsref',
    version='1.0.0',
    description='Sports reference scraper',
    long_description=long_description,
    author='J. Scott Moreland',
    author_email='morelandjs@gmail.com',
    url='https://github.com/sports_reference.git',
    license='MIT',
    packages=['sportsref'],
)

#!/usr/bin/env python

# distutils/setuptools install script for Scout2
import os
from setuptools import setup, find_packages

# Package info
NAME = 'AWSScout2'
ROOT = os.path.dirname(__file__)
VERSION = __import__(NAME).__version__

# Requirements
requirements = []
with open('requirements.txt') as f:
    for r in f.readlines():
        requirements.append(r.strip())

# Setup
setup(
    name=NAME,
    version=VERSION,
    description='Scout2, TODO',
    long_description=open('README.md').read(),
    author='l01cd3v',
    author_email='l01cd3v@gmail.com',
    url='https://github.com/iSECPartners/Scout2',
    entry_points={
        'console_scripts': [
            'Scout2 = AWSScout2.__main__:main',
        ]
    },
    packages=find_packages(exclude=['tests*']),
    package_data={
        NAME: [
            'data/*.json',
            'data/rulesets/*.json',
            'data/html/*.html'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='GNU General Public License v2 (GPLv2)',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
)

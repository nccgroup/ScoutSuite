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
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AWSScout2', 'data', 'requirements.txt')) as f:
    for r in f.readlines():
        requirements.append(r.strip())

# Setup
setup(
    name=NAME,
    version=VERSION,
    description='Scout2, TODO',
    long_description=open('README.rst').read(),
    author='l01cd3v',
    author_email='l01cd3v@gmail.com',
    url='https://github.com/nccgroup/Scout2',
    entry_points={
        'console_scripts': [
            'Scout2 = AWSScout2.__main__:main',
            'Scout2RulesGenerator = AWSScout2.__rules_generator__:main',
            'Scout2Listall = AWSScout2.__listall__:main'
        ]
    },
    packages=[
        'AWSScout2', 'AWSScout2.configs', 'AWSScout2.output', 'AWSScout2.rules', 'AWSScout2.services'
    ],
    package_data={
        'AWSScout2': [
            'data/requirements.txt'
        ],
        'AWSScout2.configs': [
            'data/*.json'
        ],
        'AWSScout2.output': [
            'data/html/*.html',
            'data/html/partials/*.html',
            'data/html/summaries/*.html',
            'data/includes.zip',
            'data/inc-scout2/*.js',
            'data/inc-scout2/*.css'
        ],
        'AWSScout2.rules': [
            'data/*.html',
            'data/filters/*.json',
            'data/findings/*.json',
            'data/rulesets/*.json'
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

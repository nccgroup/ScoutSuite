#!/usr/bin/env python

# distutils/setuptools install script for Scout Suite
import os
from setuptools import setup, find_packages

# Package info
NAME = 'ScoutSuite'
ROOT = os.path.dirname(__file__)
VERSION = __import__(NAME).__version__

# Requirements
requirements = []
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')) as f:
    for r in f.readlines():
        requirements.append(r.strip())

# Setup
setup(
    name=NAME,
    version=VERSION,
    description='Scout Suite, a multi-cloud security auditing tool',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author='NCC Group',
    url='https://github.com/nccgroup/ScoutSuite',
    entry_points={
        'console_scripts': [
            'scout = ScoutSuite.__main__:run_from_cli',
        ]
    },
    packages=find_packages(),
    package_data={
        'ScoutSuite.data': [
            '*.json'
        ],
        'ScoutSuite.output': [
            'data/html/*.html',
            'data/html/conditionals/*.html',
            'data/html/partials/*.html',
            'data/html/partials/aws/*.html',
            'data/html/partials/azure/*.html',
            'data/html/partials/gcp/*.html',
            'data/html/summaries/*.html',
            'data/includes.zip',
            'data/inc-scoutsuite/*.js',
            'data/inc-scoutsuite/*.css'
        ],
        'ScoutSuite.providers': [
            'aws/rules/conditions/*.json',
            'aws/rules/filters/*.json',
            'aws/rules/findings/*.json',
            'aws/rules/rulesets/*.json'
            'azure/rules/conditions/*.json',
            'azure/rules/filters/*.json',
            'azure/rules/findings/*.json',
            'azure/rules/rulesets/*.json'
            'gcp/rules/conditions/*.json',
            'gcp/rules/filters/*.json',
            'gcp/rules/findings/*.json',
            'gcp/rules/rulesets/*.json'
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)

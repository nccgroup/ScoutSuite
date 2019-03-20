# -*- coding: utf-8 -*-

from enum import Enum


class ReportFile(Enum):
    AWSCONFIG = 'scoutsuite-results/scoutsuite_results.js'
    EXCEPTIONS = 'scoutsuite-results/scoutsuite_exceptions.js'
    HTMLREPORT = 'report.html'
    AWSRULESET = 'scoutsuite-results/scoutsuite_ruleset.js'

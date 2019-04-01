# -*- coding: utf-8 -*-

from enum import Enum


class ReportFile(Enum):
    results = 'scoutsuite-results/scoutsuite_results.js'
    exceptions = 'scoutsuite-results/scoutsuite_exceptions.js'
    report = 'report.html'
    ruleset = 'scoutsuite-results/scoutsuite_ruleset.js'
    errors = 'scoutsuite-results/scoutsuite_errors_log.json'

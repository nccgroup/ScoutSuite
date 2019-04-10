from enum import Enum


class ReportFile(Enum):
    directory = 'scoutsuite-report'
    results = 'scoutsuite-results/scoutsuite_results.js'
    exceptions = 'scoutsuite-results/scoutsuite_exceptions.js'
    report = 'report.html'
    ruleset = 'scoutsuite-results/scoutsuite_ruleset.js'
    errors = 'scoutsuite-results/scoutsuite_errors_log.json'

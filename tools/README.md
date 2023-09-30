# Tools

This folder holds a number of useful tools for development and advanced usage of Scout Suite.

## [aws_security_hub_export.py](https://github.com/nccgroup/ScoutSuite/blob/master/tools/aws_security_hub_export.py)

Allows exporting results from at report to AWS Security Hub.

CLI Usage:

```shell
$ python tools/aws_security_hub_export.py -h
usage: aws_security_hub_export.py [-h] [-p PROFILE] -f FILE

Tool to upload a JSON report to AWS Security Hub

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        The named profile to use to authenticate to AWS.
                        Defaults to "default".
  -f FILE, --file FILE  The path of the JSON results file to process, e.g.
                        "scoutsuite-report/scoutsuite-
                        results/scoutsuite_results_aws-<profile>.js".

$ python tools/aws_security_hub_export.py --profile <profile> --file scoutsuite-report/scoutsuite-results/scoutsuite_results_aws-<profile>.js
2020-04-19 10:09:06 wrkbx2 scout[7121] INFO Authenticated with profile <profile>
2020-04-19 10:09:06 wrkbx2 scout[7121] INFO Batch uploading 14 findings
2020-04-19 10:09:07 wrkbx2 scout[7121] INFO Upload completed, 14 succeeded, 0 failed
```

Programmatic Usage:

```python
Python 3.7.3 (default, Dec 20 2019, 18:57:59) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> from tools.aws_security_hub_export import run
>>> run('<profile>', 'scoutsuite-report/scoutsuite-results/scoutsuite_results_aws-<profile>.js')
```

## [format_findings.py](https://github.com/nccgroup/ScoutSuite/blob/master/tools/format_findings.py)

Formats all findings to ensure they follow standard format.

Usage:

```shell
$ python tools/format_findings.py -h                                                                                 
usage: format_findings.py [-h] [-f FOLDER]

Tool to help properly format findings.

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        The path of the folder containing the findings. If not
                        provided will format all folders

$ python tools/format_findings.py   
Formatting findings in /home/xxxxx/Git/ScoutSuite/ScoutSuite/providers/aliyun/rules/findings
Found 8/10 findings with no rationale
Formatting findings in /home/xxxxx/Git/ScoutSuite/ScoutSuite/providers/aws/rules/findings
Found 66/100 findings with no rationale
Formatting findings in /home/xxxxx/Git/ScoutSuite/ScoutSuite/providers/azure/rules/findings
Found 2/40 findings with no rationale
Formatting findings in /home/xxxxx/Git/ScoutSuite/ScoutSuite/providers/gcp/rules/findings
Found 10/30 findings with no rationale
Formatting findings in /home/xxxxx/Git/ScoutSuite/ScoutSuite/providers/oci/rules/findings
Found 5/10 findings with no rationale
```

Refer to https://github.com/nccgroup/ScoutSuite/wiki/HowTo:-Create-a-new-rule for related information.

## [gen-tests.py](https://github.com/nccgroup/ScoutSuite/blob/master/tools/gen-tests.py)

TBD 

## [process_raw_response.py](https://github.com/nccgroup/ScoutSuite/blob/master/tools/process_raw_response.py)

Helps parse an object returned by the cloud provider's APIs and generate a boilerplate partial.

Refer to https://github.com/nccgroup/ScoutSuite/wiki/Tools & https://github.com/nccgroup/ScoutSuite/wiki/HowTo:-Create-a-custom-partial-for-new-resources for usage information.

## [sort-ruleset.py](https://github.com/nccgroup/ScoutSuite/blob/master/tools/sort-ruleset.py)

Sorts and prettyfies a ruleset by file name.

## [update-aws-ips.sh](https://github.com/nccgroup/ScoutSuite/blob/master/tools/update-aws-ips.sh)

Updates the AWS CIDRs file.


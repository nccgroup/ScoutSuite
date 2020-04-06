# Tools

This folder holds a number of useful tools for development and advanced usage of Scout Suite.

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

Refer to https://github.com/nccgroup/ScoutSuite/wiki/HowTo:-Create-a-custom-partial-for-new-resources for usage information.

## [sort-ruleset.py](https://github.com/nccgroup/ScoutSuite/blob/master/tools/sort-ruleset.py)

Sorts and prettyfies a ruleset by file name.

## [update-aws-ips.sh](https://github.com/nccgroup/ScoutSuite/blob/master/tools/update-aws-ips.sh)

Updates the AWS CIDRs file.


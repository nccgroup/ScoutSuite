<p align="center">
  <img src="https://user-images.githubusercontent.com/4206926/49877604-10457580-fe26-11e8-92d7-cd876c4f6454.png" width=350/>
</p>

#

[![Travis](https://travis-ci.org/nccgroup/ScoutSuite.svg?branch=master)](https://travis-ci.org/nccgroup/ScoutSuite)
[![Coverage Status](https://coveralls.io/repos/github/nccgroup/ScoutSuite/badge.svg?branch=master)](https://coveralls.io/github/nccgroup/ScoutSuite?branch=master)
[![CodeCov](https://codecov.io/gh/nccgroup/ScoutSuite/branch/master/graph/badge.svg)](https://codecov.io/gh/nccgroup/ScoutSuite)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/nccgroup/ScoutSuite.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/nccgroup/ScoutSuite/alerts/)
[![PyPI version](https://badge.fury.io/py/ScoutSuite.svg)](https://badge.fury.io/py/ScoutSuite)

## Description

Scout Suite is an open source multi-cloud security-auditing tool, which enables security posture assessment of cloud 
environments. Using the APIs exposed by cloud providers, Scout Suite gathers configuration data for manual inspection 
and highlights risk areas. Rather than going through dozens of pages on the web consoles, Scout Suite presents a clear 
view of the attack surface automatically.

Scout Suite is stable and actively maintained, but a number of features and internals may change. As such, please bear
with us as we find time to work on, and improve, the tool. Feel free to report a bug with details (please provide
console output using the `--debug` argument), request a new feature, or send a pull request.

The project team can be contacted at <scoutsuite@nccgroup.com>.

**Note:**

The latest (and final) version of Scout2 can be found in <https://github.com/nccgroup/Scout2/releases> and
<https://pypi.org/project/AWSScout2>. Further work is not planned for Scout2. Fixes will be implemented in Scout Suite.

### Support

The following cloud providers are currently supported/planned:

- Amazon Web Services
- Microsoft Azure
- Google Cloud Platform
- Alibaba Cloud (alpha)
- Oracle Cloud Infrastructure (alpha)

### Installation

Refer to the [wiki](https://github.com/nccgroup/ScoutSuite/wiki/Setup).

## Compliance

### AWS

Use of Scout Suite does not require AWS users to complete and submit the AWS Vulnerability / Penetration Testing
Request Form. Scout Suite only performs API calls to fetch configuration data and identify security gaps, which is not
considered security scanning as it does not impact AWS' network and applications.

### Azure

Use of Scout Suite does not require Azure users to contact Microsoft to begin testing. The only requirement is that
users abide by the Microsoft Cloud Unified Penetration Testing Rules of Engagement.

References:
- https://docs.microsoft.com/en-us/azure/security/azure-security-pen-testing
- https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement

### Google Cloud Platform

Use of Scout Suite does not require GCP users to contact Google to begin testing. The only requirement is that users
abide by the Cloud Platform Acceptable Use Policy and the Terms of Service and ensure that tests only affect projects
you own (and not other customers' applications).

References:
- https://cloud.google.com/terms/aup
- https://cloud.google.com/terms/

## Usage

The following command will provide the list of available command line options:

    $ python scout.py --help

You can also use this to get help on a specific provider:

    $ python scout.py PROVIDER --help

For further details, checkout our Wiki pages at <https://github.com/nccgroup/ScoutSuite/wiki>.

After performing a number of API calls, Scout will create a local HTML report and open it in the default browser.

Also note that the command line will try to infer the argument name if possible when receiving partial switch. For
example, this will work and use the selected profile:

    $ python scout.py aws --profile PROFILE

### Credentials

Assuming you already have your provider's CLI up and running you should have your credentials already set up and be able to run Scout Suite by using one of the following commands. If that is not the case, please consult the wiki page for the provider desired.

#### [Amazon Web Services](https://github.com/nccgroup/ScoutSuite/wiki/Amazon-Web-Services)

    $ python scout.py aws

#### [Azure](https://github.com/nccgroup/ScoutSuite/wiki/Azure)

    $ python scout.py azure --cli

#### [Google Cloud Platform](https://github.com/nccgroup/ScoutSuite/wiki/Google-Cloud-Platform)

    $ python scout.py gcp --user-account

Additional information can be found in the [wiki](https://github.com/nccgroup/ScoutSuite/wiki).
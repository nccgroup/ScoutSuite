<p align="center">
  <img src="https://user-images.githubusercontent.com/4206926/49877604-10457580-fe26-11e8-92d7-cd876c4f6454.png" width=350/>
</p>

#

[![Travis](https://travis-ci.org/nccgroup/ScoutSuite.svg?branch=master)](https://travis-ci.org/nccgroup/ScoutSuite)
[![Coverage Status](https://coveralls.io/repos/github/nccgroup/ScoutSuite/badge.svg?branch=master)](https://coveralls.io/github/nccgroup/ScoutSuite?branch=master)
[![CodeCov](https://codecov.io/gh/nccgroup/ScoutSuite/branch/master/graph/badge.svg)](https://codecov.io/gh/nccgroup/ScoutSuite)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/nccgroup/ScoutSuite.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/nccgroup/ScoutSuite/alerts/)
[![PyPI version](https://badge.fury.io/py/ScoutSuite.svg)](https://badge.fury.io/py/ScoutSuite)
[![PyPI downloads](https://img.shields.io/pypi/dm/scoutsuite)](https://img.shields.io/pypi/dm/scoutsuite)

## Description

Scout Suite is an open source multi-cloud security-auditing tool, which enables security posture assessment of cloud 
environments. Using the APIs exposed by cloud providers, Scout Suite gathers configuration data for manual inspection 
and highlights risk areas. Rather than going through dozens of pages on the web consoles, Scout Suite presents a clear 
view of the attack surface automatically.

Scout Suite is stable and actively maintained, but a number of features and internals may change. As such, please bear
with us as we find time to work on, and improve, the tool. Feel free to report a bug with details (please provide
console output using the `--debug` argument), request a new feature, or send a pull request.

The project team can be contacted at <scoutsuite@nccgroup.com>.

### Cloud Provider Support

The following cloud providers are currently supported:

- Amazon Web Services
- Microsoft Azure
- Google Cloud Platform
- Alibaba Cloud (alpha)
- Oracle Cloud Infrastructure (alpha)

### Installation

Refer to the [wiki](https://github.com/nccgroup/ScoutSuite/wiki/Setup).

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
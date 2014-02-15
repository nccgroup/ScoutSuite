AWS Scout2
==========

## Description

Scout2 is a security tool that lets AWS administrators asses their environment's
security posture. Using the AWS API, Scout2 gathers configuration data for
manual inspection and highlights high-risk areas automatically. Rather than
pouring through dozens of pages on the web, Scout2 supplies a clear view of the
attack surface automatically.

**Note:** Scout2 is still under development. It is currently usable, but a
number of features may change. As such, please bear with us as we find time to
work on the tool. Feel free to report a bug with details, request a new feature,
or send a pull request.

## Installation

To install Scout2, simply clone this repository.

The following is a list of required python modules that may not be installed on
your system:

* Boto, Amazon's AWS SDK for Python (https://aws.amazon.com/sdkforpython)
* Dateutil (https://pypi.python.org/pypi/python-dateutil)

## Requirements

To run Scout2, you will need valid AWS credentials (Access Key). The role, or
user account, associated with this Access Key needs to have read access on all
resources within:

* Identity and Access Management (IAM)
* Elastic Compute Cloud (EC2)
* Simple Storage Service (S3)

## Usage

To run Scout2 using an access key downloaded from AWS, run the following command:

    $ python Scout2.py --credentials <CREDENTIALS.CSV>

To run Scout2 from an EC2 instance within an appropriate IAM Role, run the following command:

    $ python Scout2.py --role-credentials

To run Scout2 when MFA-Protected API Access is configured, run the following command:

    $ python Scout2.py --credentials <CREDENTIALS.CSV> --mfa_serial <ARN_MFA_SERIAL_NUMBER> --mfa_code <MFA CODE>

Scout2 will generate a number of JavaScript files that contain AWS configuration
data stored as JSON payloads. Scout2 will also generate additional JavaScript
files that contain potential security flaws and best practices violations will.
To review the configuration, simply open the report.html file in your browser.

## Advanced documentation

The following command will provide the list of available command line options:

    $ python Scout2.py --help

## License

GPLv2: See LICENSE.txt.

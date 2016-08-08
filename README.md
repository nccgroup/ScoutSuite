AWS Scout2
==========

[![Build Status](https://travis-ci.org/nccgroup/Scout2.svg?branch=master)](https://travis-ci.org/nccgroup/Scout2)

## Description

Scout2 is a security tool that lets AWS administrators assess their environment's
security posture. Using the AWS API, Scout2 gathers configuration data for
manual inspection and highlights high-risk areas automatically. Rather than
pouring through dozens of pages on the web, Scout2 supplies a clear view of the
attack surface automatically.

**Note:** Scout2 is still under development. It is currently usable, but a
number of features may change. As such, please bear with us as we find time to
work on the tool. Feel free to report a bug with details, request a new feature,
or send a pull request.

## Installation

To install Scout2:

	# Clone this repository.
	$ git clone https://github.com/nccgroup/Scout2

	# install required packages:
	$ pip install -r requirements.txt

## Requirements

To run Scout2, you will need valid AWS credentials (Access Key). The role, or
user account, associated with this Access Key requires read-only access for all
resources in the following services:

* Cloudtrail
* Elastic Compute Cloud (EC2)
* Identity and Access Management (IAM)
* Relational Database Service (RDS)
* Redshift
* Simple Storage Service (S3)

If you are not sure what permissions to grant, the
[Scout2-Default](https://github.com/nccgroup/AWS-recipes/blob/master/IAM-Policies/Scout2-Default.json)
IAM policy lists the permissions necessary for a default run of Scout2.

## Usage

To run Scout2 from  an EC2 instance with an appropriate role or from a computer
already configured to use the AWS CLI, boto, or another AWS SDK (via
environment variables or configuration files), run the following command:

    $ python Scout2.py

If you configured multiple profiles, run the following command if you do not
wish to use the default profile:

    $ python Scout2.py --profile <PROFILE_NAME>

To run Scout2 using an access key downloaded from AWS, run the following command:

    $ python Scout2.py --csv-credentials <CREDENTIALS.CSV>

To run Scout2 when MFA-Protected API Access is configured, add the following
parameters to your command:

    --mfa-serial <ARN_MFA_SERIAL_NUMBER> --mfa-code <MFA CODE>

To view the report, simply open report.html in your browser.

## Format of the CSV file that contains credentials

AWS allows users to download access keys in a CSV file. If you downloaded the
file from the AWS web console, this should just work. If you were handed
credentials outside of a CSV file, the expected format is as follow:

    User Name,Access Key Id,Secret Access Key (,MFA Serial)
    f00b4r,YOUR_ACCESS_KEY_ID,YOUR_ACCESS_KEY_SECRET (,arn:aws:iam::YOUR_AWS_ACCOUNT:mfa/f00b4r)

**Note:** The fourth value is not standard, but supported for convenience if you
have enabled MFA-protected API access and want to avoid entering your MFA serial
everytime you run Scout2.

## Advanced documentation

The following command will provide the list of available command line options:

    $ python Scout2.py --help

For further details, checkout our GitHub pages at
[https://isecpartners.github.io/Scout2/](https://isecpartners.github.io/Scout2/).

## License

GPLv2: See LICENSE.

AWS Scout2
==========

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
	$ git clone git@github.com:iSECPartners/Scout2.git

	# install required packages:
	$ pip install -r requirements.txt

## Requirements

To run Scout2, you will need valid AWS credentials (Access Key). The role, or
user account, associated with this Access Key needs to have read access on all
resources within:

* Cloudtrail
* Elastic Compute Cloud (EC2)
* Identity and Access Management (IAM)
* Relational Database Service (RDS)
* Simple Storage Service (S3)

## Usage

To run Scout2 from  a computer already configured to use the AWS CLI or Boto, or
from an EC2 instance within an appropriate role, run the following command:

    $ python Scout2.py

To run Scout2 using an access key downloaded from AWS, run the following command:

    $ python Scout2.py --csv_credentials <CREDENTIALS.CSV>

To run Scout2 when MFA-Protected API Access is configured, add the following
parameters to your command:

    --mfa_serial <ARN_MFA_SERIAL_NUMBER> --mfa_code <MFA CODE>

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

## License

GPLv2: See LICENSE.

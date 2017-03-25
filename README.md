AWS Scout2
==========

[![Build Status](https://travis-ci.org/nccgroup/Scout2.svg?branch=master)](https://travis-ci.org/nccgroup/Scout2)

## Description

Scout2 is a security tool that lets AWS administrators assess their environment's
security posture. Using the AWS API, Scout2 gathers configuration data for
manual inspection and highlights high-risk areas automatically. Rather than
pouring through dozens of pages on the web, Scout2 supplies a clear view of the
attack surface automatically.

**Note:** Scout2 is stable and actively maintained, but a number of features and internals may change. As such, please bear with us as we find time to work on, and improve, the tool. Feel free to report a bug with details, request a new feature, or send a pull request.

## Installation

TODO: pip

To install Scout2:

	# Clone this repository.
	$ git clone https://github.com/nccgroup/Scout2

	# install required packages:
	$ pip install -r requirements.txt

## Requirements

### Python                                                                                           

Scout2 is written in Python and supports the following versions:
 * 2.7
 * 3.3
 * 3.4
 * 3.5

### AWS Credentials                                                                                  
To run Scout2, you will need valid AWS credentials (Access Key). The role, or
user account, associated with this Access Key requires read-only access for all
resources in a number of services, including but not limited to CloudTrail, EC2,
IAM, RDS, Redshift, and S3.

If you are not sure what permissions to grant, the [Scout2-Default](https://github.com/nccgroup/AWS-recipes/blob/master/IAM-Policies/Scout2-Default.json)
IAM policy lists the permissions necessary for a default run of Scout2.

**Note:** If you are running the tool using new credentials, **DO NOT ATTEMPT
TO CREATE YOUR OWN CSV FILE**. Instead, configure your computer using the
[aws_recipes_configure_iam tool](https://github.com/nccgroup/AWS-recipes/blob/master/Python/aws_recipes_configure_iam.py)
or refer to
[the AWS documentation](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration)
for information about configuring credentials for the AWS CLI.

### Compliant with AWS' Acceptable Use Policy
Use of Scout2 does not require AWS users to complete and submit the AWS Vulnerability / Penetration Testing Request Form. Scout2 only performs AWS API calls to fetch configuration data and identify security gaps, which is not considered security scanning as it does not impact AWS' network and applications.

## Usage

### From an EC2 instance with an appropriate IAM role

    $ python Scout2.py

### From a computer configured to use the AWS CLI, boto, or another AWS SDK (default profile)

    $ python Scout2.py

### From a computer configured to use the AWS CLI, boto, or another AWS SDK (other profile)

    $ python Scout2.py --profile <PROFILE_NAME>

### From a computer not configured to use the AWS CLI, using a CSV file downloaded from AWS

To run Scout2 using an access key downloaded from AWS, run the following command:

    $ python Scout2.py --csv-credentials <CREDENTIALS.CSV>

### When MFA-Protected API Access is Enforced

Initiate an STS session using the [aws_recipes_init_sts_session tool](https://github.com/nccgroup/AWS-recipes/blob/master/Python/aws_recipes_init_sts_session.py)
**OR**
Add the following parameters to your command:

    --mfa-serial <ARN_MFA_SERIAL_NUMBER> --mfa-code <MFA CODE>

To view the report, simply open report.html in your browser.

## Format of the CSV file that contains credentials

AWS allows users to download access keys in a CSV file. If you downloaded the
file from the AWS web console, this should just work. If you were handed
credentials outside of a CSV file, the expected format is as follow (credentials **must** be on line 2):

    User Name,Access Key Id,Secret Access Key (,MFA Serial)
    f00b4r,YOUR_ACCESS_KEY_ID,YOUR_ACCESS_KEY_SECRET (,arn:aws:iam::YOUR_AWS_ACCOUNT:mfa/f00b4r)

**Note:** The fourth value is not standard, but supported for convenience if you
have enabled MFA-protected API access and want to avoid entering your MFA serial
everytime you run Scout2.

## Advanced documentation

The following command will provide the list of available command line options:

    $ python Scout2.py --help

For further details, checkout our GitHub pages at
[https://nccgroup.github.io/Scout2/](https://nccgroup.github.io/Scout2/).

## License

GPLv2: See LICENSE.

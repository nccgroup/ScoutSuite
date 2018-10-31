# Scout Suite

![image](https://travis-ci.org/nccgroup/Scout2.svg?branch=master)
![image](https://coveralls.io/repos/github/nccgroup/Scout2/badge.svg?branch=master)
![image](https://badge.fury.io/py/AWSScout2.svg)

## Description

Scout Suite is a multi-cloud configuration review tool, which enables assessing the security posture of cloud
environments. Using the APIs exposed by cloud providers, Scout gathers configuration data for manual inspection and 
highlights risk areas . Rather than pouring through dozens of pages on the web, Scout supplies a clear view of the 
attack surface automatically.

Scout Suite is stable and actively maintained, but a number of features and internals may change. As such, please bear 
with us as we find time to work on, and improve, the tool. Feel free to report a bug with details (please provide 
console output using the "--debug" argument), request a new feature, or send a pull request.

**Note:**

The latest (and final) version of Scout2 can be found in <https://github.com/nccgroup/Scout2/releases> and
<https://pypi.org/project/ScoutSuite/>.

Further work is not planned for Scout2. Fixes for the issues currently opened will be implemented in Scout Suite.

### Support

The following cloud providers are currently supported:

-   Amazon Web Services
-   Google Cloud Platform (beta)
-   Azure (early alpha)

## Installation

Install via `pip`:

    $ pip install scoutsuite

Install from source:

    $ git clone https://github.com/nccgroup/ScoutSuite
    $ cd ScoutSuite
    $ virtualenv -p python venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python setup.py install

## Requirements

### Computing resources

Scout Suite is a multi-threaded tool that fetches and stores your cloud account's configuration settings in memory 
during runtime. It is expected that the tool will run with no issues on any modern laptop or equivalent VM.

**Note** that running Scout Suite in a VM with limited computing resources such as an AWS t2.micro instance is not 
intended and will likely result in the process being killed.

### Python

Scout Suite is written in Python and supports the following versions:

-   2.7
-   3.4
-   3.5
-   3.6
-   3.7

The required libraries can be found in the requirements.txt file.

### Credentials

#### Amazon Web Services

To run Scout against an AWS account, you will need valid AWS credentials (*e.g* Access Key ID and Secret Access Key).
The role, or user account,associated with these credentials requires read-only access for all resources in a number of 
services, including but not limited to CloudTrail, EC2, IAM, RDS, Redshift, and S3.

The following AWS Managed Policies can be attached to the principal in order to grant necessary permissions:

-   ReadOnlyAccess
-   SecurityAudit

#### Google Cloud Platform

There are two ways to run Scout against a GCP project.

1.  User Account
    :   1.  Configure the cloud shell to use the appropriate User
            Account credentials (`gcloud init` command to use a new
            accound and `gcloud config set account <account>` to use an
            existing account)
        2.  Obtain access credentials to run Scout with:
            gcloud auth application-default login
        3.  Run Scout with the `--user-account` flag

2.  Service Account
    :   1.  Generate service account keys
        2.  Download the keys in JSON format (refer to
            <https://cloud.google.com/iam/docs/creating-managing-service-account-keys>)
        3.  Run Scout with the --service-account flag and providing the
            key file path with `--key-file <path/to/key_file.json`

The following roles can be attached to the member in order to grant
necessary permissions:

-   Viewer
-   Security Reviewer
-   Stackdriver Account Viewer

#### Azure

TODO

### Compliance

#### AWS Acceptable Use Policy

Use of Scout Suite does not require AWS users to complete and submit the AWS Vulnerability / Penetration Testing 
Request Form. Scout Suite only performs API calls to fetch configuration data and identify security gaps, which is not 
considered security scanning as it does not impact AWS' network and applications.

#### Google Cloud Platform

Use of Scout Suite does not require GCP users to contact Google to begin testing.The only requirement is that users 
abide by the Cloud Platform Acceptable Use Policy and the Terms of Service and ensure that tests only affect projects 
you onw (and not other customers’ applications).

References:
- https://cloud.google.com/terms/aup
- https://cloud.google.com/terms/

#### Azure

TODO

### Usage

The following command will provide the list of available command line options:

    $ Scout --help

For further details, checkout our Wiki pages at <https://github.com/nccgroup/ScoutSuite/wiki>.

After performing a number of AWS API calls, Scout will create a local HTML report and open it in the default browser.

#### Amazon Web Services

Using a computer already configured to use the AWS CLI, boto3, or another AWS SDK, you may use Scout using the 
following command:

    $ Scout

**Note:** EC2 instances with an IAM role fit in this category.

If multiple profiles are configured in your .aws/credentials and .aws/config files, you may specify which credentials 
to use with the following command:

    $ Scout --profile <PROFILE_NAME>

If you have a CSV file containing the API access key ID and secret, you may run Scout with the following command:

    $ Scout --csv-credentials <CREDENTIALS.CSV>

#### Google Cloud Platform

TODO

#### Azure

TODO

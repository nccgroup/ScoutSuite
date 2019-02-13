<p align="center">
  <img src="https://user-images.githubusercontent.com/4206926/49877604-10457580-fe26-11e8-92d7-cd876c4f6454.png" width=350/>
</p>

#

[![Travis](https://travis-ci.org/nccgroup/ScoutSuite.svg?branch=master)](https://travis-ci.org/nccgroup/ScoutSuite)
[![Coverage Status](https://coveralls.io/repos/github/nccgroup/ScoutSuite/badge.svg?branch=master)](https://coveralls.io/github/nccgroup/ScoutSuite?branch=master)
[![CodeCov](https://codecov.io/gh/nccgroup/ScoutSuite/branch/master/graph/badge.svg)](https://codecov.io/gh/nccgroup/ScoutSuite)
[![PyPI version](https://badge.fury.io/py/ScoutSuite.svg)](https://badge.fury.io/py/ScoutSuite)

## Description

Scout Suite is a multi-cloud security auditing tool, which enables assessing the security posture of cloud
environments. Using the APIs exposed by cloud providers, Scout gathers configuration data for manual inspection and
highlights risk areas. Rather than pouring through dozens of pages on the web consoles, Scout provides a clear view of
the attack surface automatically.

Scout Suite is stable and actively maintained, but a number of features and internals may change. As such, please bare
with us as we find time to work on, and improve, the tool. Feel free to report a bug with details (please provide
console output using the `--debug` argument), request a new feature, or send a pull request.

**Note:**

The latest (and final) version of Scout2 can be found in <https://github.com/nccgroup/Scout2/releases> and
<https://pypi.org/project/AWSScout2>. Further work is not planned for Scout2. Fixes will be implemented in Scout Suite.

### Support

The following cloud providers are currently supported/planned:

-   Amazon Web Services
-   Google Cloud Platform (beta)
-   Azure (alpha)

## Installation

Install via `pip`:

    $ pip install scoutsuite

Install from source:

    $ git clone https://github.com/nccgroup/ScoutSuite
    $ cd ScoutSuite
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python Scout.py --help

## Requirements

### Computing resources

Scout Suite is a multi-threaded tool that fetches and stores your cloud account's configuration settings in memory
during runtime. It is expected that the tool will run with no issues on any modern laptop or equivalent VM. **Note**
that running Scout Suite in a VM with limited computing resources such as an AWS t2.micro instance is not intended and
may result in the process being killed.

### Python

Scout Suite is written in Python and supports the following versions:

-   2.7
-   3.4
-   3.5
-   3.6
-   3.7

The required libraries can be found in the
[requirements.txt](https://github.com/nccgroup/ScoutSuite/blob/master/requirements.txt) file.

### Credentials

#### Amazon Web Services

To run Scout against an AWS account, you will need valid AWS credentials (i.e. Access Key ID and Secret Access Key).

The following AWS Managed Policies can be attached to the principal used to run Scout in order to grant the necessary
permissions:

-   `ReadOnlyAccess`
-   `SecurityAudit`

#### Google Cloud Platform

There are two ways to run Scout against a GCP Organization or Project.

1.  User Account
    1.  Configure the cloud shell to use the appropriate User Account credentials (`gcloud init` command to use a new
    account or `gcloud config set account <account>` to use an existing account)
    2.  Obtain access credentials to run Scout with: `gcloud auth application-default login`
    3.  Run Scout with the `--user-account` flag
2.  Service Account
    1.  Generate and download service account keys in JSON format
    (refer to <https://cloud.google.com/iam/docs/creating-managing-service-account-keys>)
    2.  Run Scout with the `--service-account` flag while providing the key file path

The following roles can be attached to the member used to run Scout in order to grant necessary permissions:

- `Viewer`
- `Security Reviewer`
- `Stackdriver Account Viewer`

#### Azure

There are five ways to run scout against an Azure organization.

1.  azure-cli
    1. On most system, you can install azure-cli using `pip install azure-cli`.
    2. Log into an account. The easiest way to do it it with `az login`(for more authentication method,
    you can refer to https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli?view=azure-cli-latest).
    3. Run Scout with the `--cli` flag.
2.  Managed Service Identity
    1. Configure your identity on the Azure portal(you can refer to
    https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/)
    2. Run Scout with the `--msi` flag.
3.  Service Principal
    1. Set up a service principal on the Azure portal(you can refer to
    https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)
    2. Run Scout with the `--service-principal` flag. Scout will prompt you for the required information.
4.  File-based Authentication
    1. Create a Service Principal for azure SDK. You can do this with azure-cli using
    `az ad sp create-for-rbac --sdk-auth > mycredentials.json`.
    2. Run Scout while providing it with the credentials file using
    `--azure-file-auth path/to/credentials/file`.
5.  User Credentials
    1. Run Scout using `--user-account`. The application will prompt you for your credentials.

Scout will require the `Reader` role over all the resources to assess. The easiest way is to authenticate with a principal that has this role over the target Subscription, as it will be inherited on all the resources.

### Compliance

#### AWS Acceptable Use Policy

Use of Scout Suite does not require AWS users to complete and submit the AWS Vulnerability / Penetration Testing
Request Form. Scout Suite only performs API calls to fetch configuration data and identify security gaps, which is not
considered security scanning as it does not impact AWS' network and applications.

#### Google Cloud Platform

Use of Scout Suite does not require GCP users to contact Google to begin testing. The only requirement is that users
abide by the Cloud Platform Acceptable Use Policy and the Terms of Service and ensure that tests only affect projects
you own (and not other customers' applications).

References:
- https://cloud.google.com/terms/aup
- https://cloud.google.com/terms/

#### Azure

Use of Scout Suite does not require Azure users to contact Microsoft to begin testing. The only requirement is that
users abide by the Microsoft Cloud Unified Penetration Testing Rules of Engagement.

References:
- https://docs.microsoft.com/en-us/azure/security/azure-security-pen-testing
- https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement

### Usage

The following command will provide the list of available command line options:

    $ python Scout.py --help

You can also use this to get help on a specific provider:

    $ python Scout.py aws --help

For further details, checkout our Wiki pages at <https://github.com/nccgroup/ScoutSuite/wiki>.

After performing a number of API calls, Scout will create a local HTML report and open it in the default browser.

Also note that the command line will try to infer the argument name if possible when receiving partial switch. For
example, this will work and use the selected profile:

    $python Scout.py aws --pro PROFILE

#### Amazon Web Services

Using a computer already configured to use the AWS CLI, you may use Scout using the following command:

    $ python Scout.py aws

**Note:** EC2 instances with an IAM role fit in this category.

If multiple profiles are configured in your .aws/credentials and .aws/config files, you may specify which credentials
to use with the following command:

    $ python Scout.py aws --profile <PROFILE_NAME>

If you have a CSV file containing the API access key ID and secret, you may run Scout with the following command:

    $ python Scout.py aws --csv-credentials <CREDENTIALS.CSV>

#### Google Cloud Platform

Using a computer already configured to use gcloud command-line tool, you may use Scout using the following command:

    $ python Scout.py gcp --user-account

To run Scout using Service Account keys, using the following command:

    $ python Scout.py gcp --service-account </PATH/TO/KEY_FILE.JSON>
    
By default, only the inferred default Project will be scanned.

To scan a GCP ...
- Organization, use the `organization-id <ORGANIZATION ID>` argument
- Folder, use the `folder-id <FOLDER ID>` argument.
- Project, use the `project-id <PROJECT ID>` argument
- All projects that a user/service account has access to, use the `--all-projects` flags.

#### Azure

Using a computer already configured to use azure-cli, you may use Scout using the following command:

    $ python Scout.py azure --cli

When using Scout in an Azure virtual machine with the Reader role, you may use
Scout using the following command:

    $ python Scout.py azure --msi

When using Scout with a Service Principal, you may run Scout using the following command:

    $ python Scout.py azure --service-principal

You can also pass the credentials you want directly with command line arguments. The remaining ones will be asked
interactively:

    $ python Scout.py azure --service-principal --tenant <TENANT_ID> --subscription <SUBSCRIPTION_ID> --client-id <CLIENT_ID>
    --client-secret <CLIENT_SECRET>

When using Scout with an authentication file, you may run Scout using the following command:

    $ python Scout.py azure --file-auth </PATH/TO/KEY_FILE.JSON>

When using Scout against your user account, you may run Scout using the following command:

    $ python Scout.py azure --user-account

You can also pass the credentials you want directly with command line arguments. The remaining ones will be asked
interactively:

    $ python Scout.py azure --username <USERNAME> --password <PASSWORD>

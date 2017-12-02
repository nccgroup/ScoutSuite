##########
AWS Scout2
##########

.. image:: https://travis-ci.org/nccgroup/Scout2.svg?branch=master
        :target: https://travis-ci.org/nccgroup/Scout2

.. image:: https://coveralls.io/repos/github/nccgroup/Scout2/badge.svg?branch=master
        :target: https://coveralls.io/github/nccgroup/Scout2

.. image:: https://badge.fury.io/py/AWSScout2.svg
        :target: https://badge.fury.io/py/AWSScout2
        :align: right

***********
Description
***********

Scout2 is a security tool that lets AWS administrators assess their
environment's security posture. Using the AWS API, Scout2 gathers configuration
data for manual inspection and highlights high-risk areas automatically. Rather
than pouring through dozens of pages on the web, Scout2 supplies a clear view of
the attack surface automatically.

**Note:** Scout2 is stable and actively maintained, but a number of features and
internals may change. As such, please bear with us as we find time to work on,
and improve, the tool. Feel free to report a bug with details (*e.g.* console
output using the "--debug" argument), request a new feature, or send a pull
request.

************
Installation
************

Install via `pip`_:

::

    $ pip install awsscout2

Install from source:

::

    $ git clone https://github.com/nccgroup/Scout2
    $ cd Scout2
    $ pip install -r requirements.txt
    $ python setup.py install

************
Requirements
************

Computing resources
-------------------

Scout2 is a multi-threaded tool that fetches and stores your AWS account's configuration settings in memory during runtime. It is expected that the tool will run with no issues on any modern laptop or equivalent VM. **Running Scout2 in a VM with limited computing resources such as a t2.micro instance is not intended and will likely result in the process being killed.**

Python
------

Scout2 is written in Python and supports the following versions:

* 2.7
* 3.3
* 3.4
* 3.5
* 3.6

AWS Credentials
---------------

To run Scout2, you will need valid AWS credentials (*e.g* Access Key ID and
Secret Access Key). The role, or user account, associated with these credentials
requires read-only access for all resources in a number of services, including
but not limited to CloudTrail, EC2, IAM, RDS, Redshift, and S3.

If you are not sure what permissions to grant, the `Scout2-Default`_
IAM policy lists the permissions necessary for a default run of Scout2.

Compliance with AWS' Acceptable Use Policy
------------------------------------------

Use of Scout2 does not require AWS users to complete and submit the AWS
Vulnerability / Penetration Testing Request Form. Scout2 only performs AWS API
calls to fetch configuration data and identify security gaps, which is not
considered security scanning as it does not impact AWS' network and
applications.

Usage
-----

After performing a number of AWS API calls, Scout2 will create a local HTML report and open it in the default browser.

Using a computer already configured to use the AWS CLI, boto3, or another AWS SDK, you may use Scout2 using the following command:

::

    $ Scout2

**Note:** EC2 instances with an IAM role fit in this category.

If multiple profiles are configured in your .aws/credentials and .aws/config files, you may specify which credentials to use with the following command:

::

    $ Scout2 --profile <PROFILE_NAME>

If you have a CSV file containing the API access key ID and secret, you may run Scout2 with the following command:

::

    $ Scout2 --csv-credentials <CREDENTIALS.CSV>

**********************
Advanced documentation
**********************

The following command will provide the list of available command line options:

::

    $ Scout2 --help

For further details, checkout our Wiki pages at https://github.com/nccgroup/Scout2/wiki.

*******
License
*******

GPLv2: See LICENSE.

.. _pip: https://pip.pypa.io/en/stable/index.html
.. _Scout2-Default: https://github.com/nccgroup/AWS-recipes/blob/master/IAM-Policies/Scout2-Default.json

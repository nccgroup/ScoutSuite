Scout Suite
#######################

.. image:: https://travis-ci.org/nccgroup/Scout2.svg?branch=master
        :target: https://travis-ci.org/nccgroup/Scout2

.. image:: https://coveralls.io/repos/github/nccgroup/Scout2/badge.svg?branch=master
        :target: https://coveralls.io/github/nccgroup/Scout2

.. image:: https://badge.fury.io/py/AWSScout2.svg
        :target: https://badge.fury.io/py/AWSScout2
        :align: right

Description
***********

Scout Suite is a multi-cloud configuratiobn review tool, which enables assessing the security posture of cloud
environments. Using the APIs provided by cloud providers, Scout gathers configuration data for manual inspection and
highlights risk areas automatically. Rather than pouring through dozens of pages on the web, Scout supplies a clear
view of the attack surface automatically.

**Note:**

Scout Suite is stable and actively maintained, but a number of features and internals may change. As such, please
bear with us as we find time to work on, and improve, the tool. Feel free to report a bug with details (please provide
console output using the "--debug" argument), request a new feature, or send a pull request.

.. IMPORTANT::
   The latest (and final) version of Scout2 can be found in https://github.com/nccgroup/Scout2/releases and
   https://pypi.org/project/AWSScout2/.

   Further work is not planned for this branch. Fixes for the issues currently opened will be implemented in Scout Suite.

Support
-------

The following cloud providers are currently supported:

- Amazon Web Services
- Google Cloud Platform (alpha)

Support is in the roadmap for the following cloud provider(s):

- Azure

Installation
************

.. NOTE::
   TODO

Install via `pip`_:

::

    $ pip install scoutsuite

Install from source:

::

    $ git clone https://github.com/nccgroup/ScoutSuite
    $ cd ScoutSuite
    $ pip install -r requirements.txt
    $ python setup.py install

Requirements
************

Computing resources
-------------------

Scout Suite is a multi-threaded tool that fetches and stores your AWS account's configuration settings in memory during
runtime. It is expected that the tool will run with no issues on any modern laptop or equivalent VM.
**Running Scout Suite in a VM with limited computing resources such as a t2.micro instance is not intended and will likely
result in the process being killed.**

Python
------

Scout Suite is written in Python and supports the following versions:

* 2.7
* 3.3
* 3.4
* 3.5
* 3.6

AWS Credentials
---------------

Amazon Web Services
^^^^^^^^^^^^^^^^^^^

To run Scout, you will need valid AWS credentials (*e.g* Access Key ID and Secret Access Key).
The role, or user account, associated with these credentials requires read-only access for all resources in a number of
services, including but not limited to CloudTrail, EC2, IAM, RDS, Redshift, and S3.

The following AWS Managed Policies can be attached to the principal in order to grant necessary permissions:

* ReadOnlyAccess
* SecurityAudit

Google Cloud Platform
^^^^^^^^^^^^^^^^^^^^^

.. NOTE::
   TODO

Compliance
----------

AWS Acceptable Use Policy
^^^^^^^^^^^^^^^^^^^^^^^^^

Use of Scout Suite does not require AWS users to complete and submit the AWS
Vulnerability / Penetration Testing Request Form. Scout Suite only performs AWS API
calls to fetch configuration data and identify security gaps, which is not
considered security scanning as it does not impact AWS' network and
applications.

Google Cloud Platform
^^^^^^^^^^^^^^^^^^^^^

.. NOTE::
   TODO

Usage
-----

.. NOTE::
   TODO - provide examples for each provider

After performing a number of AWS API calls, Scout will create a local HTML report and open it in the default browser.

Using a computer already configured to use the AWS CLI, boto3, or another AWS SDK, you may use Scout using the
following command:

::

    $ Scout

**Note:** EC2 instances with an IAM role fit in this category.

If multiple profiles are configured in your .aws/credentials and .aws/config files, you may specify which credentials
to use with the following command:

::

    $ Scout --profile <PROFILE_NAME>

If you have a CSV file containing the API access key ID and secret, you may run Scout with the following command:

::

    $ Scout --csv-credentials <CREDENTIALS.CSV>

Advanced documentation
**********************

The following command will provide the list of available command line options:

::

    $ Scout --help

For further details, checkout our Wiki pages at https://github.com/nccgroup/ScoutSuite/wiki.

License
*******

GPLv2: See LICENSE.

.. _pip: https://pip.pypa.io/en/stable/index.html

# NCC-ScoutSuite

[![Docker build status](https://img.shields.io/docker/cloud/build/rossja/ncc-scoutsuite)]( https://img.shields.io/docker/cloud/build/rossja/ncc-scoutsuite)
[![](https://images.microbadger.com/badges/image/rossja/ncc-scoutsuite.svg)](https://microbadger.com/images/rossja/ncc-scoutsuite) 
[![](https://images.microbadger.com/badges/version/rossja/ncc-scoutsuite.svg)](https://microbadger.com/images/rossja/ncc-scoutsuite) 
[![Docker Pulls](https://img.shields.io/docker/pulls/rossja/ncc-scoutsuite.svg?style=flat-square)](https://hub.docker.com/r/rossja/ncc-scoutsuite/)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-rossja%2Fncc--scoutsuite-blue)](https://hub.docker.com/r/rossja/ncc-scoutsuite/)


## Quick Links

1. [Running the Container](#running-thecontainer)
1. [Running Scoutsuite](#running-scoutsuite)
    1. [Example Test](#example-test)
1. [Accessing the Report](#report-access)
1. [Cloud Provider Setup](#setup-providers)
    1. [AWS](#setup-aws)
    1. [Azure](#setup-azure)
    1. [GCP](#setup-gcp)

## Overview

[ScoutSuite](https://github.com/nccgroup/ScoutSuite) is a Python based tool published and maintained by NCC Group, for use in cloud security assessments.
This repository is an Ubuntu based container that comes with all pre-requisite software required to run ScoutSuite. It's based on the Ubuntu 20.04 docker base.

The current version of scoutsuite installed in the container is: `Scout Suite 5.8.1`

The following CLI tools are also installed:

* **AWS (version 2)**:

~~~bash
aws-cli/2.0.12 Python/3.7.3 Linux/4.19.76-linuxkit botocore/2.0.0dev16
~~~

* **Azure**:  

~~~bash
azure-cli                          2.5.1

command-modules-nspkg              2.0.3
core                               2.5.1
nspkg                              3.0.4
telemetry                          1.0.4

Python location '/opt/az/bin/python3'
Extensions directory '/root/.azure/cliextensions'

Python (Linux) 3.6.5 (default, Apr 30 2020, 06:22:36)
[GCC 9.2.1 20191008]
~~~

* **GCP**:

~~~bash
Google Cloud SDK 291.0.0
alpha 2020.05.01
app-engine-python 1.9.90
app-engine-python-extras 1.9.90
beta 2020.05.01
bq 2.0.57
core 2020.05.01
gsutil 4.50
kubectl 2020.05.01
~~~


----

<a name="running-thecontainer" href="#"></a>

## Running The Container

* Grab the image and run it: 

~~~bash
docker run -it rossja/ncc-scoutsuite bash
~~~

* Alternatively, clone the [GitHub Repo](https://github.com/rossja/ncc-scoutsuite) and then run `docker-compose up --build` from within the source tree, then run it.

----

<a name="running-scoutsuite" href="#"></a>

## Running ScoutSuite

Once the CLI for the environment you are testing has been configured and the appropriate credentials set up (see below for more info on how to do this), we can run ScoutSuite in the container. As of version 0.1.0, when you run the container you're automatically set up in the scoutsuite environment.

You should see that the command prompt reflects this virtual environment, by pre-pending the name of the virtual environment (scoutsuite) to the prompt: 

~~~bash
root@1350ede02c47:~# source scoutsuite/bin/activate
(scoutsuite) root@1350ede02c47:~#
~~~

You can verify that the installation worked using the command `scout --help`, which should provide help for the tool.

~~~bash
(scoutsuite) root@1350ede02c47:~# scout --help
usage: scout [-h] [-v] {aws,gcp,azure,aliyun,oci} ...

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

The provider you want to run scout against:
  {aws,gcp,azure,aliyun,oci}
    aws                 Run Scout against an Amazon Web Services account
    gcp                 Run Scout against a Google Cloud Platform account
    azure               Run Scout against a Microsoft Azure account
    aliyun              Run Scout against an Alibaba Cloud account
    oci                 Run Scout against an Oracle Cloud Infrastructure
~~~

### Recommended Parameters

* Since this is a container, there's no GUI, and no browser, so passing the `--no-browser` probably makes sense. 
* Likewise, setting a specific report directory using something like `--report-dir /root/scout-report` is a good idea. *(The default location is `$HOME/scoutsuite-report`)*


----

<a name="example-test" href="#"></a>

## Example Test

The example below demonstrates running scout against AWS, using the profile `scout-user01`, saving the report to the directory `/root/scout-report`: 

~~~bash
scout aws --profile scout-user01 --no-browser --report-dir /root/scout-report
2020-01-03 17:45:16 460837197ae9 scout[7087] INFO Launching Scout
2020-01-03 17:45:16 460837197ae9 scout[7087] INFO Authenticating to cloud provider
2020-01-03 17:45:17 460837197ae9 scout[7087] INFO Gathering data from APIs
2020-01-03 17:45:17 460837197ae9 scout[7087] INFO Fetching resources for the Lambda service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the CloudFormation service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the CloudTrail service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the CloudWatch service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the Config service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the Direct Connect service
2020-01-03 17:45:19 460837197ae9 scout[7087] INFO Fetching resources for the EC2 service
2020-01-03 17:45:19 460837197ae9 scout[7087] INFO Fetching resources for the EFS service
2020-01-03 17:45:19 460837197ae9 scout[7087] INFO Fetching resources for the ElastiCache service
2020-01-03 17:45:20 460837197ae9 scout[7087] INFO Fetching resources for the ELB service
2020-01-03 17:45:21 460837197ae9 scout[7087] INFO Fetching resources for the ELBv2 service
2020-01-03 17:45:21 460837197ae9 scout[7087] INFO Fetching resources for the EMR service
2020-01-03 17:45:22 460837197ae9 scout[7087] INFO Fetching resources for the IAM service
2020-01-03 17:45:22 460837197ae9 scout[7087] INFO Fetching resources for the RDS service
2020-01-03 17:45:23 460837197ae9 scout[7087] INFO Fetching resources for the RedShift service
2020-01-03 17:45:23 460837197ae9 scout[7087] INFO Fetching resources for the Route53 service
2020-01-03 17:45:23 460837197ae9 scout[7087] INFO Fetching resources for the S3 service
2020-01-03 17:45:24 460837197ae9 scout[7087] INFO Fetching resources for the SES service
2020-01-03 17:45:24 460837197ae9 scout[7087] INFO Fetching resources for the SNS service
2020-01-03 17:45:24 460837197ae9 scout[7087] INFO Fetching resources for the SQS service
2020-01-03 17:45:24 460837197ae9 scout[7087] INFO Fetching resources for the VPC service
2020-01-03 17:46:13 460837197ae9 scout[7087] INFO Running rule engine
2020-01-03 17:46:15 460837197ae9 scout[7087] INFO Applying display filters
2020-01-03 17:46:16 460837197ae9 scout[7087] INFO Saving data to /root/scout-report/scoutsuite-results/scoutsuite_results_aws-scout-user01.js
2020-01-03 17:46:16 460837197ae9 scout[7087] INFO Saving data to /root/scout-report/scoutsuite-results/scoutsuite_exceptions_aws-scout-user01.js
2020-01-03 17:46:16 460837197ae9 scout[7087] INFO Creating /root/scout-report/aws-scout-user01.html
~~~


----

<a name="report-access" href="#"></a>

## Accessing Report Data

The report is stored in the directory specified with the `--report-dir` flag
*Note: if this flag is omitted, the default is to create a `scoutsuite-report` directory in the directory the user is in at the time scout is run*.

### TL;DR

You can shortcut the process below by simply combining the `docker ps` command with the `docker cp` command like so: 

~~~bash
docker cp $(docker ps -f ancestor=rossja/ncc-scoutsuite --format "{{.ID}}"):/root/scout-report ./
~~~

### Details

To copy the report data out of the running container, you can use the following process:

* On the docker host (not the container): run `docker ps` using a filter to find the container ID for the running instance of the container. An example of how to do this is shown below:

~~~bash
docker ps -f ancestor=rossja/ncc-scoutsuite --format "Container ID: {{.ID}}"
Container ID: a8d70ee4ced8
~~~

* Once you have the container ID, you can use the `docker cp` command to copy the report from the running container instance to your Docker host:

~~~bash
docker cp <container-id>:</path/to/report> </path/to/local/copy>
~~~

* For example, if the container ID is `a8d70ee4ced8`, and the report is stored in `/root/scout-report` on that container, the following command could be used to copy the report data from the container to the current directory: 

~~~bash
docker cp a8d70ee4ced8:/root/scout-report ./
~~~

You can shortcut this process by simply combining the `docker ps` command with the `docker cp` command like so: 

~~~bash
docker cp $(docker ps -f ancestor=rossja/ncc-scoutsuite --format "{{.ID}}"):/root/scout-report ./
~~~


----


## Viewing the Output File

The report itself can be viewed using a web browser, by opening the file `./scout-report/aws-<profile>.html`. 
For example, if you ran the scout tool against AWS using the profile `scout-user01`, the report HTML file is at `./scout-report/aws-scout-01.html`. 

**NOTES**: 

**AWS**: If you used the default AWS profile credentials, the profile name is the numerical ID portion of the ARN for the user, rather than a specific profile or user name.
**GCP**: The scout report will be named using the project ID that was passed in.


----

<a name="setup-providers" href="#"></a>

# Cloud Provider Setup

This section of the documentation outlines how to configure accounts in the various cloud providers to enable ScoutSuite to run properly.

<a name="setup-aws" href="#"></a>

## AWS 

### IAM Configuration

This section defines how to configure AWS with a minimal ScoutSuite configuration policy. Reference: [ScoutSuite Wiki Policy Page](https://github.com/nccgroup/ScoutSuite/wiki/AWS-Minimal-Privileges-Policy)

#### Policy Setup

* Login to AWS Web Console
* Go to : IAM -> Policies
* Click on "Create Policy"
* Click the "JSON" tab
* Replace the contents of the JSON Window with the policy statement below:

~~~json
{
    "Version": "2012-10-17",
    "Statement": [
        {
                "acm:DescribeCertificate",
                "acm:ListCertificates",
                "acm:GetCertificate",
                "acm:ListTagsForCertificate",
                "cloudformation:DescribeStacks",
                "cloudformation:GetStackPolicy",
                "cloudformation:ListStacks",
                "cloudformation:GetTemplate",
                "cloudtrail:DescribeTrails",
                "cloudtrail:GetEventSelectors",
                "cloudtrail:GetTrailStatus",
                "cloudwatch:DescribeAlarms",
                "config:DescribeConfigRules",
                "config:DescribeConfigurationRecorderStatus",
                "config:DescribeConfigurationRecorders",
                "directconnect:DescribeConnections",
                "dynamodb:DescribeContinuousBackups",
                "dynamodb:DescribeTable",
                "dynamodb:ListBackups",
                "dynamodb:ListTables",
                "ec2:DescribeCustomerGateways",
                "ec2:DescribeFlowLogs",
                "ec2:DescribeImages",
                "ec2:DescribeInstances",
                "ec2:DescribeRegions",
                "ec2:DescribeNetworkAcls",
                "ec2:DescribeNetworkInterfaceAttribute",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeRouteTables",
                "ec2:DescribeInstanceAttribute",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSnapshotAttribute",
                "ec2:DescribeSnapshots",
                "ec2:DescribeSubnets",
                "ec2:DescribeVolumes",
                "ec2:DescribeVpcPeeringConnections",
                "ec2:DescribeVpcs",
                "ec2:DescribeVpnConnections",
                "ec2:DescribeVpnGateways",
                "elasticache:DescribeCacheClusters",
                "elasticache:DescribeCacheParameterGroups",
                "elasticache:DescribeCacheSecurityGroups",
                "elasticache:DescribeCacheSubnetGroups",
                "elasticfilesystem:DescribeFileSystems",
                "elasticfilesystem:DescribeMountTargetSecurityGroups",
                "elasticfilesystem:DescribeMountTargets",
                "elasticfilesystem:DescribeTags",
                "elasticloadbalancing:DescribeListeners",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeLoadBalancerPolicies",
                "elasticloadbalancing:DescribeSSLPolicies",
                "elasticmapreduce:DescribeCluster",
                "elasticmapreduce:ListClusters",
                "iam:GenerateCredentialReport",
                "iam:GetAccountPasswordPolicy",
                "iam:GetCredentialReport",
                "iam:GetGroup",
                "iam:GetGroupPolicy",
                "iam:GetLoginProfile",
                "iam:GetPolicyVersion",
                "iam:GetRolePolicy",
                "iam:GetUserPolicy",
                "iam:ListAccessKeys",
                "iam:ListEntitiesForPolicy",
                "iam:ListGroupPolicies",
                "iam:ListGroups",
                "iam:ListGroupsForUser",
                "iam:ListInstanceProfilesForRole",
                "iam:ListMFADevices",
                "iam:ListPolicies",
                "iam:ListRolePolicies",
                "iam:ListRoles",
                "iam:ListUserPolicies",
                "iam:ListUsers",
                "kms:DescribeKey",
                "kms:GetKeyRotationStatus",
                "kms:ListAliases",
                "kms:ListKeys",
                "lambda:ListFunctions",
                "rds:DescribeDBClusters",
                "rds:DescribeDBInstances",
                "rds:DescribeDBParameterGroups",
                "rds:DescribeDBParameters",
                "rds:DescribeDBSecurityGroups",
                "rds:DescribeDBSnapshotAttributes",
                "rds:DescribeDBSnapshots",
                "rds:DescribeDBSubnetGroups",
                "redshift:DescribeClusterParameterGroups",
                "redshift:DescribeClusterParameters",
                "redshift:DescribeClusterSecurityGroups",
                "redshift:DescribeClusters",
                "route53:ListHostedZones",
                "route53:ListResourceRecordSets",
                "route53domains:ListDomains",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation",
                "s3:GetBucketLogging",
                "s3:GetBucketPolicy",
                "s3:GetBucketVersioning",
                "s3:GetBucketWebsite",
                "s3:GetEncryptionConfiguration",
                "s3:GetBucketTagging",
                "s3:ListAllMyBuckets",
                "ses:GetIdentityDkimAttributes",
                "ses:GetIdentityPolicies",
                "ses:ListIdentities",
                "ses:ListIdentityPolicies",
                "sns:GetTopicAttributes",
                "sns:ListSubscriptions",
                "sns:ListTopics",
                "sqs:GetQueueAttributes",
                "sqs:ListQueues"
            ],
            "Resource": "*"
        }
    ]
}
~~~

* Click on "Review Policy"
* Give the Policy a name, and description
* Click "Create Policy"

#### Assigning the Policy to a User

* In AWS IAM click on "Users"
* Create a new user: example username could be: `scout-user01`
* Click on "Programmatic Access", then click "Next"
* Click on the "Attach existing policies directly" tab
* Search for the Policy created above and select it
* Click on "Next:Tags"
* Add any applicable tags. For example: `role: scout`
* Click on "Next:Review"
* Click on "Create User"
* **CRITICAL**: Click on "Download .csv". Name the CSV something meaningful. Example: `aws-scout-user01`. If this file is not preserved, the secret key will be lost with no way to recover it. You will need the keys contained in this file to set up the AWS CLI environment ScoutSuite uses.

### AWS CLI Credential Management

The AWS credentials created get stored in the home directory of the user: in this container that means root. Look for the `config` and `credentials` files in `$HOME/.aws`. The examples below show how these files might look after setting up a default user profile only:

* default profile only `$HOME/.aws/config` example:

~~~yaml
[default]
region = us-east-1
output = json
~~~

* default profile only `$HOME/.aws/credentials` example:
	
~~~yaml
[default]
aws_access_key_id = <access-key>
aws_secret_access_key = <secret key>
~~~

#### Using Multiple AWS Profiles

If you need to create specific profiles, you can do this by passing the `--profile` flag to the `config` command of the AWS CLI. 

You can also simply edit the YAML in the config and credentials files. 

For example, to create a profile called `scout-user01` in addition to the default profile, you could use the following config and credentials files:

* multiple profile `$HOME/.aws/config` example:

~~~yaml
[default]
region = us-east-1
output = json

[profile scout-user01]
region = us-east-1
output = json
~~~

* multiple profile `$HOME/.aws/credentials` example:
	
~~~yaml
[default]
aws_access_key_id = <access-key>
aws_secret_access_key = <secret key>

[scout-user01]
aws_access_key_id = <access-key>
aws_secret_access_key = <secret key>
~~~

#### Verification of Credentials

To test that the AWS CLI credentials have been set up correctly, you can run any of the commands available to the user you have set up. For example, to list the IAM users:

`aws2 iam list-users` (or `aws2 --profile <profile-name> iam list-users` if you are using multiple profiles)

You should see output similar to the following: 

~~~json
{
    "Users": [
        {
            "Path": "/",
            "UserName": "user01",
            "UserId": "AIDAIUZF4IL2CAWNIBRC4",
            "Arn": "arn:aws:iam::758548986810:user/user01",
            "CreateDate": "2018-10-22T22:10:22+00:00"
        },
        {
            "Path": "/",
            "UserName": "user02",
            "UserId": "AIDAI5XVDDRXPSIVEZJGS",
            "Arn": "arn:aws:iam::758548986810:user/user02",
            "CreateDate": "2019-04-20T05:31:46+00:00"
        }
    ]
}
~~~

### Running ScoutSuite

You can run scout either using the default AWS profile, or a specific profile:

* To run using the default profile, simply run `scout aws`. 
* To use a specific profile use the `--profile` flag: `scout aws --profile <profile-name>`. Because this is running inside a docker container, pass the `--no-browser` flag to prevent auto-opening the report.


----

<a name="setup-azure" href="#"></a>

## Azure

### Permissions Setup

1. Create a user in the desired directory
2. Grant the given user the role of `Global Reader` in the directory
3. Add the user to the desired subscription, with both `Reader` and `Security Reader` roles

### Configuring the Azure CLI

1. In the container run `az login -u <user> -p <pass> -t <tenant>`

### Running Scoutsuite

Once the permissions have been set up and the CLI configured, running scout can be done using the following:

~~~bash
# scout azure --cli --no-browser --report-dir /root/scout-report
~~~


----

<a name="setup-gcp" href="#"></a>

## Google Cloud (GCP)

### Assigning GCP privileges

1. Create a user in the Google Cloud console, in the project that will be tested.
2. Assign the following roles to the user: `Viewer`, `Security Reviewer`, `Stackdriver Account Viewer`.
3. Additionally, you may need to assign the following using <https://console.developers.google.com/iam-admin/iam/project?project=[project-id]>: 
  - `serviceusage.services.use` for the project
  - `storage.buckets.getIamPolicy` for all buckets that should be reviewed
4. Ensure that the `cloud resource manager API` is enabled for the project that will be tested.
5. If the project uses KMS, ensure that the `Cloud Key Management Service (KMS) API` is enabled.


### Configuring the gCloud SDK

Once the user is created and permissions assigned, you need to login to GCP using the SDK `auth` method:

~~~bash
# gcloud auth application-default login

Go to the following link in your browser:

    https://accounts.google.com/o/oauth2/auth?code_challenge=[snipped]


Enter verification code:
~~~

Running the command above will provide a URL that you need to paste into a browser. Login to the Google account that has the required privileges, and you will see a verification code that you need to enter at the command prompt. This will add the credentials to the gcloud json file. 

### Running Scoutsuite

Once the gcloud sdk is configured, running scout can be done using the following: 

~~~bash
# scout gcp -u --project-id <project-id> --no-browser --report-dir /root/scout-report
~~~

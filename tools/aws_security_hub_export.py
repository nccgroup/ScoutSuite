#!/usr/bin/env python3

from ScoutSuite.providers.aws.utils import get_caller_identity
from ScoutSuite.core.console import set_logger_configuration, print_info, print_exception
from tools.utils import results_file_to_dict

import datetime
import argparse
import boto3


def upload_findigs_to_securityhub(session, formatted_findings_list):
    try:
        if formatted_findings_list:
            print_info('Batch uploading {} findings'.format(len(formatted_findings_list)))
            securityhub = session.client('securityhub')
            response = securityhub.batch_import_findings(Findings=formatted_findings_list)
            print_info('Upload completed, {} succeeded, {} failed'.format(response.get('SuccessCount'),
                                                                          response.get('FailedCount')))
            return response
    except Exception as e:
        print_exception(f'Unable to upload findings to Security Hub: {e}')


def format_finding_to_securityhub_format(aws_account_id,
                                         region,
                                         creation_date,
                                         finding_key,
                                         finding_value):
    try:

        if finding_value.get('level') == 'danger':
            label = 'HIGH'
        elif finding_value.get('level') == 'warning':
            label = 'MEDIUM'
        else:
            label = 'INFORMATIONAL'

        format_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

        formatted_finding = {
            'SchemaVersion': '2018-10-08',
            'Id': finding_key,
            'ProductArn':
                'arn:aws:securityhub:' + region + ':' + aws_account_id + ':product/' + aws_account_id + '/default',
            'GeneratorId': f'scoutsuite-{aws_account_id}',
            'AwsAccountId': aws_account_id,
            'Types': ['Software and Configuration Checks/AWS Security Best Practices'],
            'FirstObservedAt': creation_date,
            'CreatedAt': format_time,
            'UpdatedAt': format_time,
            'Severity': {
                'Label': label
            },
            'Title': finding_value.get('description'),
            'Description': finding_value.get('rationale') if finding_value.get('rationale') else 'None',
            'Remediation': {
                'Recommendation': {
                    'Text': finding_value.get('remediation', 'None') if finding_value.get('remediation') else 'None'
                }
            },
            'ProductFields': {'Product Name': 'Scout Suite'},
            'Resources': [  # TODO this lacks affected resources
                {
                    'Type': 'AwsAccount',
                    'Id': 'AWS::::Account:' + creation_date,
                    'Partition': 'aws',
                    'Region': region
                }
            ],
            'Compliance': {
                'Status': 'FAILED'
            },
            'RecordState': 'ACTIVE'
        }
        return formatted_finding
    except Exception as e:
        print_exception(f'Unable to process finding: {e}')


def process_results_file(f,
                         region):
    try:
        formatted_findings_list = []
        results = results_file_to_dict(f)

        aws_account_id = results["account_id"]
        creation_date = datetime.datetime.strptime(results["last_run"]["time"], '%Y-%m-%d %H:%M:%S%z').isoformat()

        for service in results.get('service_list'):
            for finding_key, finding_value in results.get('services', {}).get(service).get('findings').items():
                if finding_value.get('items'):
                    formatted_finding = format_finding_to_securityhub_format(aws_account_id,
                                                                             region,
                                                                             creation_date,
                                                                             finding_key,
                                                                             finding_value)
                    formatted_findings_list.append(formatted_finding)

        return formatted_findings_list
    except Exception as e:
        print_exception(f'Unable to process results file: {e}')


def run(profile, file):
    session = boto3.Session(profile_name=profile)
    # Test querying for current user
    get_caller_identity(session)
    print_info(f'Authenticated with profile {profile}')

    try:
        with open(file) as f:
            formatted_findings_list = process_results_file(f,
                                                           session.region_name)
    except Exception as e:
        print_exception(f'Unable to open file {file}: {e}')

    upload_findigs_to_securityhub(session, formatted_findings_list)


if __name__ == "__main__":

    # Configure the debug level
    set_logger_configuration()

    parser = argparse.ArgumentParser(description='Tool to upload a JSON report to AWS Security Hub')
    parser.add_argument('-p', '--profile',
                        required=False,
                        default="default",
                        help="The named profile to use to authenticate to AWS. Defaults to \"default\".")
    parser.add_argument('-f', '--file',
                        required=True,
                        help="The path of the JSON results file to process, e.g. "
                             "\"scoutsuite-report/scoutsuite-results/scoutsuite_results_aws-<profile>.js\".")
    args = parser.parse_args()

    try:
        run(args.profile, args.file)
    except Exception as e:
        print_exception(f'Unable to complete: {e}')

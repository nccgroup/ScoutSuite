# Import future print
from __future__ import print_function

import boto3
import datetime
import dateutil.parser
import json
import fileinput
import os
import re
import requests # TODO: get rid of that and make sure urllib2 validates certs ?
import string

from opinel.utils.console import printException, printError, printInfo
from opinel.utils.console import prompt_4_mfa_code
from opinel.utils.fs import save_blob_as_json
from opinel.utils.aws import connect_service


########################################
# Globals
########################################

re_profile_name = re.compile(r'\[(.*)\]')
re_access_key = re.compile(r'aws_access_key_id')
re_secret_key = re.compile(r'aws_secret_access_key')
re_role_arn = re.compile(r'role_arn')
re_session_token = re.compile(r'aws_session_token')
re_security_token = re.compile(r'aws_security_token')
re_expiration = re.compile(r'expiration')
re_source_profile = re.compile(r'source_profile')
re_external_id = re.compile(r'aws_external_id')

re_gov_region = re.compile(r'(.*?)-gov-(.*?)')
re_cn_region = re.compile(r'^cn-(.*?)')

re_port_range = re.compile(r'(\d+)\-(\d+)')
re_single_port = re.compile(r'(\d+)')

mfa_serial = r'(aws_mfa_serial|mfa_serial)'
mfa_serial_format = r'arn:aws:iam::\d+:mfa/[a-zA-Z0-9\+=,.@_-]+'
re_mfa_serial = re.compile(mfa_serial)
re_mfa_serial_format = re.compile(mfa_serial_format)


aws_config_dir = os.path.join(os.path.expanduser('~'), '.aws')
aws_credentials_file = os.path.join(aws_config_dir, 'credentials')
aws_credentials_file_tmp = os.path.join(aws_config_dir, 'credentials.tmp')
aws_config_file = os.path.join(aws_config_dir, 'config')


########################################
# Credentials read/write functions
########################################


def assume_role(role_name, credentials, role_arn, role_session_name, silent = False):
    """
    Assume role and save credentials

    :param role_name:
    :param credentials:
    :param role_arn:
    :param role_session_name:
    :param silent:
    :return:
    """
    external_id = credentials.pop('ExternalId') if 'ExternalId' in credentials else None
    # Connect to STS
    sts_client = connect_service('sts', credentials, silent = silent)
    # Set required arguments for assume role call
    sts_args = {
      'RoleArn': role_arn,
      'RoleSessionName': role_session_name
    }
    # MFA used ?
    if 'mfa_serial' in credentials and 'mfa_code' in credentials:
      sts_args['TokenCode'] = credentials['mfa_code']
      sts_args['SerialNumber'] = credentials['mfa_serial']
    # External ID used ?
    if external_id:
      sts_args['ExternalId'] = external_id
    # Assume the role
    sts_response = sts_client.assume_role(**sts_args)
    credentials = sts_response['Credentials']
    cached_credentials_filename = get_cached_credentials_filename(role_name, role_arn)
    #with open(cached_credentials_filename, 'wt+') as f:
    #   write_data_to_file(f, sts_response, True, False)
    cached_credentials_path = os.path.dirname(cached_credentials_filename)
    if not os.path.isdir(cached_credentials_path):
        os.makedirs(cached_credentials_path)
    save_blob_as_json(cached_credentials_filename, sts_response, True, False) # blob, force_write, debug):
    return credentials


def get_cached_credentials_filename(role_name, role_arn):
    """
    Construct filepath for cached credentials (AWS CLI scheme)

    :param role_name:
    :param role_arn:
    :return:
    """
    filename_p1 = role_name.replace('/','-')
    filename_p2 = role_arn.replace('/', '-').replace(':', '_')
    return os.path.join(os.path.join(os.path.expanduser('~'), '.aws'), 'cli/cache/%s--%s.json' %
                        (filename_p1, filename_p2))


def get_profiles_from_aws_credentials_file(credentials_files = [aws_credentials_file, aws_config_file]):
    """

    :param credentials_files:

    :return:
    """
    profiles = []
    for filename in credentials_files:
        if os.path.isfile(filename):
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    groups = re_profile_name.match(line)
                    if groups:
                        profiles.append(groups.groups()[0])
    return sorted(profiles)


def generate_password(length=16):
    """
    Generate a password using random characters from uppercase, lowercase, digits, and symbols

    :param length:                      Length of the password to be generated
    :return:                            The random password
    """
    chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{};:,<.>?|'
    modulus = len(chars)
    pchars = os.urandom(16)
    if type(pchars) == str:
        return ''.join(chars[i % modulus] for i in map(ord, pchars))
    else:
        return ''.join(chars[i % modulus] for i in pchars)


def init_creds():
    """
    Create a dictionary with all the necessary keys set to "None"

    :return:
    """
    return { 'AccessKeyId': None, 'SecretAccessKey': None, 'SessionToken': None,
             'Expiration': None, 'SerialNumber': None, 'TokenCode': None }


def init_sts_session(profile_name, credentials, duration = 28800, session_name = None, save_creds = True):
    """
    Fetch STS credentials

    :param profile_name:
    :param credentials:
    :param duration:
    :param session_name:
    :param save_creds:
    :return:
    """
    # Set STS arguments
    sts_args = {
        'DurationSeconds': duration
    }
    # Prompt for MFA code if MFA serial present
    if 'SerialNumber' in credentials and credentials['SerialNumber']:
        if not credentials['TokenCode']:
            credentials['TokenCode'] = prompt_4_mfa_code()
            if credentials['TokenCode'] == 'q':
                credentials['SerialNumber'] = None
        sts_args['TokenCode'] = credentials['TokenCode']
        sts_args['SerialNumber'] = credentials['SerialNumber']
    # Init session
    sts_client = boto3.session.Session(credentials['AccessKeyId'], credentials['SecretAccessKey']).client('sts')
    sts_response = sts_client.get_session_token(**sts_args)
    if save_creds:
        # Move long-lived credentials if needed
        if not profile_name.endswith('-nomfa') and credentials['AccessKeyId'].startswith('AKIA'):
            write_creds_to_aws_credentials_file(profile_name + '-nomfa', credentials)
        # Save STS values in the .aws/credentials file
        write_creds_to_aws_credentials_file(profile_name, sts_response['Credentials'])
    return sts_response['Credentials']


def read_creds_from_aws_credentials_file(profile_name, credentials_file = aws_credentials_file):
    """
    Read credentials from AWS config file

    :param profile_name:
    :param credentials_file:
    :return:
    """
    credentials = init_creds()
    profile_found = False
    try:
        # Make sure the ~.aws folder exists
        if not os.path.exists(aws_config_dir):
            os.makedirs(aws_config_dir)
        with open(credentials_file, 'rt') as cf:
            for line in cf:
                profile_line = re_profile_name.match(line)
                if profile_line:
                    if profile_line.groups()[0] == profile_name:
                        profile_found = True
                    else:
                        profile_found = False
                if profile_found:
                    if re_access_key.match(line):
                        credentials['AccessKeyId'] = line.split("=")[1].strip()
                    elif re_secret_key.match(line):
                        credentials['SecretAccessKey'] = line.split("=")[1].strip()
                    elif re_mfa_serial.match(line):
                        credentials['SerialNumber'] = (line.split('=')[1]).strip()
                    elif re_session_token.match(line) or re_security_token.match(line):
                        credentials['SessionToken'] = ('='.join(x for x in line.split('=')[1:])).strip()
                    elif re_expiration.match(line):
                        credentials['Expiration'] = ('='.join(x for x in line.split('=')[1:])).strip()
    except Exception as e:
        # Silent if error is due to no ~/.aws/credentials file
        if not hasattr(e, 'errno') or e.errno != 2:
            printException(e)
    return credentials


def read_creds_from_csv(filename):
    """
    Read credentials from a CSV file

    :param filename:
    :return:
    """
    key_id = None
    secret = None
    mfa_serial = None
    secret_next = False
    with open(filename, 'rt') as csvfile:
        for i, line in enumerate(csvfile):
            values = line.split(',')
            for v in values:
                if v.startswith('AKIA'):
                    key_id = v.strip()
                    secret_next = True
                elif secret_next:
                    secret = v.strip()
                    secret_next = False
                elif re_mfa_serial_format.match(v):
                    mfa_serial = v.strip()
    return key_id, secret, mfa_serial


def read_creds_from_ec2_instance_metadata():
    """
    Read credentials from EC2 instance metadata (IAM role)

    :return:
    """
    creds = init_creds()
    try:
        has_role = requests.get('http://169.254.169.254/latest/meta-data/iam/security-credentials', timeout = 1)
        if has_role.status_code == 200:
            iam_role = has_role.text
            credentials = requests.get('http://169.254.169.254/latest/meta-data/iam/security-credentials/%s/' %
                                       iam_role.strip()).json()
            for c in ['AccessKeyId', 'SecretAccessKey']:
                creds[c] = credentials[c]
            creds['SessionToken'] = credentials['Token']
        return creds
    except Exception as e:
        return False


def read_creds_from_ecs_container_metadata():
    """
    Read credentials from ECS instance metadata (IAM role)

    :return:
    """
    creds = init_creds()
    try:
        ecs_metadata_relative_uri = os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']
        credentials = requests.get('http://169.254.170.2' + ecs_metadata_relative_uri, timeout = 1).json()
        for c in ['AccessKeyId', 'SecretAccessKey']:
            creds[c] = credentials[c]
            creds['SessionToken'] = credentials['Token']
        return creds
    except Exception as e:
        return False


def read_creds_from_environment_variables():
    """
    Read credentials from environment variables

    :return:
    """
    creds = init_creds()
    # Check environment variables
    if 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:
        creds['AccessKeyId'] = os.environ['AWS_ACCESS_KEY_ID']
        creds['SecretAccessKey'] = os.environ['AWS_SECRET_ACCESS_KEY']
        if 'AWS_SESSION_TOKEN' in os.environ:
            creds['SessionToken'] = os.environ['AWS_SESSION_TOKEN']
    return creds


def read_profile_from_environment_variables():
    """
    Read profiles from env

    :return:
    """
    role_arn = os.environ.get('AWS_ROLE_ARN', None)
    external_id = os.environ.get('AWS_EXTERNAL_ID', None)
    return role_arn, external_id


def read_profile_from_aws_config_file(profile_name, config_file = aws_config_file):
    """
    Read profiles from AWS config file

    :param profile_name:
    :param config_file:
    :return:
    """
    role_arn = None
    source_profile = 'default'
    mfa_serial = None
    profile_found = False
    external_id = None
    try:
        with open(config_file, 'rt') as config:
            for line in config:
                profile_line = re_profile_name.match(line)
                if profile_line:
                    role_profile_name = profile_line.groups()[0].split()[-1]
                    if role_profile_name == profile_name:
                        profile_found = True
                    else:
                        profile_found = False
                if profile_found:
                    if re_role_arn.match(line):
                        role_arn = line.split('=')[1].strip()
                    elif re_source_profile.match(line):
                        source_profile = line.split('=')[1].strip()
                    elif re_mfa_serial.match(line):
                        mfa_serial = line.split('=')[1].strip()
                    elif re_external_id.match(line):
                        external_id = line.split('=')[1].strip()
    except Exception as e:
        # Silent if error is due to no .aws/config file
        if not hasattr(e, 'errno') or e.errno != 2:
            printException(e)
    return role_arn, source_profile, mfa_serial, external_id


def show_profiles_from_aws_credentials_file(credentials_files = [aws_credentials_file, aws_config_file]):
    """
    Show profile names from ~/.aws/credentials

    :param credentials_files:
    :return:
    """
    profiles = get_profiles_from_aws_credentials_file(credentials_files)
    for profile in set(profiles):
        printInfo(' * %s' % profile)


def write_creds_to_aws_credentials_file(profile_name, credentials, credentials_file = aws_credentials_file):
    """
    Write credentials to AWS config file

    :param profile_name:
    :param credentials:
    :param credentials_file:
    :return:
    """
    profile_found = False
    profile_ever_found = False
    session_token_written = False
    security_token_written = False
    mfa_serial_written = False
    expiration_written = False
    # Create the .aws folder if needed
    if not os.path.isdir(aws_config_dir):
        os.mkdir(aws_config_dir)
    # Create an empty file if target does not exist
    if not os.path.isfile(credentials_file):
        open(credentials_file, 'a').close()
    # Open and parse/edit file
    for line in fileinput.input(credentials_file, inplace=True):
        profile_line = re_profile_name.match(line)
        if profile_line:
            if profile_line.groups()[0] == profile_name:
                profile_found = True
                profile_ever_found = True
            else:
                profile_found = False
            print(line.rstrip())
        elif profile_found:
            if re_access_key.match(line) and 'AccessKeyId' in credentials and credentials['AccessKeyId']:
                print('aws_access_key_id = %s' % credentials['AccessKeyId'])
            elif re_secret_key.match(line) and 'SecretAccessKey' in credentials and credentials['SecretAccessKey']:
                print('aws_secret_access_key = %s' % credentials['SecretAccessKey'])
            elif re_mfa_serial.match(line) and 'SerialNumber' in credentials and credentials['SerialNumber']:
                print('aws_mfa_serial = %s' % credentials['SerialNumber'])
                mfa_serial_written = True
            elif re_session_token.match(line) and 'SessionToken' in credentials and credentials['SessionToken']:
                print('aws_session_token = %s' % credentials['SessionToken'])
                session_token_written = True
            elif re_security_token.match(line) and 'SessionToken' in credentials and credentials['SessionToken']:
                print('aws_security_token = %s' % credentials['SessionToken'])
                security_token_written = True
            elif re_expiration.match(line) and 'Expiration' in credentials and credentials['Expiration']:
                print('expiration = %s' % credentials['Expiration'])
                expiration_written = True
            else:
                print(line.rstrip())
        else:
            print(line.rstrip())

    # Complete the profile if needed
    if profile_found:
        with open(credentials_file, 'a') as f:
            complete_profile(f, credentials, session_token_written, mfa_serial_written)

    # Add new profile if not found
    if not profile_ever_found:
        with open(credentials_file, 'a') as f:
            f.write('[%s]\n' % profile_name)
            f.write('aws_access_key_id = %s\n' % credentials['AccessKeyId'])
            f.write('aws_secret_access_key = %s\n' % credentials['SecretAccessKey'])
            complete_profile(f, credentials, session_token_written, mfa_serial_written)


def complete_profile(f, credentials, session_token_written, mfa_serial_written):
    """
    Append session token and mfa serial if needed

    :param f:
    :param credentials:
    :param session_token_written:
    :param mfa_serial_written:
    :return:
    """
    session_token = credentials['SessionToken'] if 'SessionToken' in credentials else None
    mfa_serial = credentials['SerialNumber'] if 'SerialNumber' in credentials else None
    if session_token and not session_token_written:
        f.write('aws_session_token = %s\n' % session_token)
    if mfa_serial and not mfa_serial_written:
        f.write('aws_mfa_serial = %s\n' % mfa_serial)

########################################
# Main function
########################################


def read_creds(profile_name, csv_file = None, mfa_serial_arg = None, mfa_code = None, force_init = False,
               role_session_name = 'opinel'):
    """
    Read credentials from anywhere (CSV, Environment, Instance metadata, config/credentials)

    :param profile_name:
    :param csv_file:
    :param mfa_serial_arg:
    :param mfa_code:
    :param force_init:
    :param role_session_name:

    :return:
    """
    first_sts_session = False
    source_profile = None
    role_mfa_serial = None
    expiration = None
    credentials = init_creds()
    role_arn, external_id = read_profile_from_environment_variables()
    if csv_file:
        # Read credentials from a CSV file that was provided
        credentials['AccessKeyId'], credentials['SecretAccessKey'], credentials['SerialNumber'] = \
            read_creds_from_csv(csv_file)
    elif profile_name == 'default':
        # Try reading credentials from environment variables (Issue #11) if the profile name is 'default'
        credentials = read_creds_from_environment_variables()
    if ('AccessKeyId' not in credentials or not credentials['AccessKeyId']) \
            and not csv_file and profile_name == 'default':
        ec2_credentials = read_creds_from_ec2_instance_metadata()
        if ec2_credentials:
            credentials = ec2_credentials
        else:
            ecs_credentials = read_creds_from_ecs_container_metadata()
            if ecs_credentials:
                credentials = ecs_credentials
        # TODO support lambda
    if role_arn or (not credentials['AccessKeyId'] and not csv_file):
        # Lookup if a role is defined in ~/.aws/config
        if not role_arn:
            role_arn, source_profile, role_mfa_serial, external_id = read_profile_from_aws_config_file(profile_name)
        # Scout2 issue 237 - credentials file may be used to configure role-based profiles...
        if not role_arn:
            role_arn, source_profile, role_mfa_serial, external_id = \
                read_profile_from_aws_config_file(profile_name, config_file = aws_credentials_file)
        if role_arn:
            # Lookup cached credentials
            try:
                cached_credentials_filename = get_cached_credentials_filename(profile_name, role_arn)
                with open(cached_credentials_filename, 'rt') as f:
                    assume_role_data = json.load(f)
                    oldcred = credentials
                    credentials = assume_role_data['Credentials']
                    expiration = dateutil.parser.parse(credentials['Expiration'])
                    expiration = expiration.replace(tzinfo=None)
                    current = datetime.datetime.utcnow()
                    if expiration < current:
                        print('Role\'s credentials have expired on %s' % credentials['Expiration'])
                        credentials = oldcred
            except Exception as e:
                pass
            if not expiration or expiration < current or credentials['AccessKeyId'] == None:
                if source_profile:
                    credentials = read_creds(source_profile)
                if role_mfa_serial:
                    credentials['SerialNumber'] = role_mfa_serial
                    # Auto prompt for a code...
                    if not mfa_code:
                        credentials['TokenCode'] = prompt_4_mfa_code()
                if external_id:
                    credentials['ExternalId'] = external_id
                credentials = assume_role(profile_name, credentials, role_arn, role_session_name)
        # Read from ~/.aws/credentials
        else:
            credentials = read_creds_from_aws_credentials_file(profile_name)
            if credentials['SessionToken']:
                if 'Expiration' in credentials and credentials['Expiration']:
                    expiration = dateutil.parser.parse(credentials['Expiration'])
                    expiration = expiration.replace(tzinfo=None)
                    current = datetime.datetime.utcnow()
                    if expiration < current:
                        printInfo('Saved STS credentials expired on %s' % credentials['Expiration'])
                        force_init = True
                else:
                    force_init = True
                    sts_credentials = credentials
            else:
                first_sts_session = True
            if force_init or (mfa_serial_arg and mfa_code):
                credentials = read_creds_from_aws_credentials_file(profile_name if first_sts_session
                                                                   else '%s-nomfa' % profile_name)
                if not credentials['AccessKeyId']:
                    printInfo('Warning: Unable to determine STS token expiration; later API calls may fail.')
                    credentials = sts_credentials
                else:
                    if mfa_serial_arg:
                        credentials['SerialNumber'] = mfa_serial_arg
                    if mfa_code:
                        credentials['TokenCode'] = mfa_code
                    if 'AccessKeyId' in credentials and credentials['AccessKeyId']:
                        credentials = init_sts_session(profile_name, credentials)
    # If we don't have valid creds by now, print an error message
    if 'AccessKeyId' not in credentials or credentials['AccessKeyId'] == None or \
            'SecretAccessKey' not in credentials or credentials['SecretAccessKey'] == None:
        printError('Error: could not find AWS credentials. Use the --help option for more information.')
    if not 'AccessKeyId' in credentials:
        credentials = { 'AccessKeyId': None }
    return credentials

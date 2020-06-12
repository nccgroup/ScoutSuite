import binascii
import copy
import os
import sys
import time
import unittest
import ScoutSuite.providers.aws.authentication_strategy

#from opinel.services.iam import *
#from opinel.utils.aws import connect_service
#from opinel.utils.console import configPrintException, printDebug
#from opinel.utils.credentials import read_creds, read_creds_from_environment_variables


class TestOpinelServicesIAM(unittest.TestCase):

    def setup(self):
        creds = {'AccessKeyId': None, 'SecretAccessKey': None, 'SessionToken': None,
                'Expiration': None, 'SerialNumber': None, 'TokenCode': None};
        # Check environment variables
        if 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:
            creds['AccessKeyId'] = os.environ['AWS_ACCESS_KEY_ID']
            creds['SecretAccessKey'] = os.environ['AWS_SECRET_ACCESS_KEY']
            if 'AWS_SESSION_TOKEN' in os.environ:
                creds['SessionToken'] = os.environ['AWS_SESSION_TOKEN']

        #if self.creds['AccessKeyId'] == None:
            #self.creds = read_creds('travislike')
        #self.api_client = connect_service('iam', self.creds)
        #self.python = re.sub(r'\W+', '', sys.version)
        self.cleanup = {'groups': [], 'users': []}


    def make_travisname(self, testname):
        return '%s-%s-%s' % (testname, binascii.b2a_hex(os.urandom(4)).decode('utf-8'), self.python)


    def assert_group_create(self, groups_data, error_count, force_add = False):
        for group_data in groups_data:
            self.assert_create('groups', group_data, error_count, force_add)


    def assert_user_create(self, user_data, error_count, force_add = False):
        self.assert_create('users', user_data, error_count, force_add)


    def assert_create(self, resource_type, resource_data, error_count, force_add = False):
        assert len(resource_data['errors']) == error_count
        nameattr = '%sname' % resource_type[:-1]
        if force_add or error_count == 0:
            #printDebug('Successfully created %s %s' % (resource_type[:-1], resource_data[nameattr]))
            self.cleanup[resource_type].append(resource_data[nameattr])


    def test_create_user(self):
        user_data = create_user(self.api_client, self.make_travisname('OpinelUnitTest001'))
        self.assert_user_create(user_data, 0)
        user_data = create_user(self.api_client, self.cleanup['users'][0])
        self.assert_user_create(user_data, 1)
        user_data = create_user(self.api_client, self.make_travisname('OpinelUnitTest002'), 'BlockedUsers')
        self.assert_user_create(user_data, 0)
        user_data = create_user(self.api_client, self.make_travisname('OpinelUnitTest003'), ['BlockedUsers', 'AllUsers'])
        self.assert_user_create(user_data, 1, True)
        user_data = create_user(self.api_client, self.make_travisname('OpinelUnitTest004'), with_password = True)
        self.assert_user_create(user_data, 0)
        assert 'password' in user_data
        assert len(user_data['password']) == 16
        user_data = create_user(self.api_client, self.make_travisname('OpinelUnitTest005'), with_password=True ,require_password_reset = True)
        self.assert_user_create(user_data, 0)
        assert 'password' in user_data
        assert len(user_data['password']) == 16
        user_data = create_user(self.api_client, self.make_travisname('OpinelUnitTest006'), with_access_key = True)
        self.assert_user_create(user_data, 0)
        assert 'AccessKeyId' in user_data
        assert user_data['AccessKeyId'].startswith('AKIA')
        assert 'SecretAccessKey' in user_data


    def test_delete_user(self):
        # Mostly tested as part of teardown
        try:
            delete_user(self.api_client, 'PhonyUserWithMFA')
        except Exception as e:
            pass
        pass


    def test_add_user_to_group(self):
        user010 = create_user(self.api_client, self.make_travisname('OpinelUnitTest010'))
        self.assert_user_create(user010, 0)
        user011 = create_user(self.api_client, self.make_travisname('OpinelUnitTest011'))
        self.assert_user_create(user011, 0)
        add_user_to_group(self.api_client, user010['username'], 'BlockedUsers', True)
        add_user_to_group(self.api_client, user011['username'], 'BlockedUsers', False)


    def test_delete_virtual_mfa_device(self):
        try:
            delete_virtual_mfa_device(self.api_client, 'arn:aws:iam::179374595322:mfa/PhonyUserWithMFA')
        except Exception as e:
            assert (e.response['Error']['Code'] == 'AccessDenied')


    def test_get_access_keys(self):
        user020 = create_user(self.api_client, self.make_travisname('OpinelUnitTest020'), with_access_key = True)
        self.assert_user_create(user020, 0)
        access_keys = get_access_keys(self.api_client, self.cleanup['users'][0])
        assert len(access_keys) == 1


    def test_show_access_keys(self):
        user021 = create_user(self.api_client, self.make_travisname('OpinelUnitTest021'), with_access_key = True)
        self.assert_user_create(user021, 0)
        show_access_keys(self.api_client, self.cleanup['users'][0])


    def test_init_group_category_regex(self):
        result = init_group_category_regex(['a', 'b'], ['', '.*hello.*'])
        assert (type(result) == list)
        result = init_group_category_regex(['a', 'b'], ['', ''])
        assert (result == None)
        result = init_group_category_regex(['a', 'b', 'c'], ['.*hello.*'])
        assert (result == None)


    def test_create_groups(self):
        group001 = self.make_travisname('OpinelUnitTest001')
        groups = create_groups(self.api_client, group001)
        self.assert_group_create(groups, 0)
        group002 = self.make_travisname('OpinelUnitTest002')
        group003 = self.make_travisname('OpinelUnitTest003')
        groups = create_groups(self.api_client, [ group002, group003 ])
        self.assert_group_create(groups, 0)
        group004 = self.make_travisname('HelloWorld')
        groups = create_groups(self.api_client, group004)
        self.assert_group_create(groups, 1)


    def teardown(self):
        if len(self.cleanup['users']):
            self.delete_resources('users')
        if len(self.cleanup['groups']):
            self.delete_resources('groups')


    def delete_resources(self, resource_type):
        resources = copy.deepcopy(self.cleanup[resource_type])
        while True:
            unmodifiable_resource = False
            remaining_resources = []
            printDebug('Deleting the following %s: %s' % (resource_type, str(resources))            )
            time.sleep(5)
            for resource in resources:
                if resource_type == 'groups':
                    errors = []
                    try:
                        self.api_client.delete_group(GroupName = resource)
                    except:
                        errors = [ 'EntityTemporarilyUnmodifiable' ]
                else:
                    method = globals()['delete_%s' % resource_type[:-1]]
                    errors = method(self.api_client, resource)
                if len(errors):
                    printDebug('Errors when deleting %s' % resource)
                    remaining_resources.append(resource)
                    for handled_code in ['EntityTemporarilyUnmodifiable', 'DeleteConflict']:
                        if handled_code in errors:
                            unmodifiable_resource = True
                        else:
                            printError('Failed to delete %s %s' % (resource_type[:-1], resource))
                            assert (False)
            resources = copy.deepcopy(remaining_resources)
            if not unmodifiable_resource:
                break
def create_user(iam_client, user, groups = [], with_password= False, with_mfa = False, with_access_key = False, require_password_reset = True):
    """
    :param iam_client:                  AWS API client for IAM
    :param user:                        Name of the user to create
    :param groups:                      Name of the IAM groups to add the user to
    :param with_password:               Boolean indicating whether creation of a password should be done
    :param with_mfa:                    Boolean indicating whether creation of an MFA device should be done
    :param with_access_key:             Boolean indicating whether creation of an API access key should be done
    :param require_password_reset:      Boolean indicating whether users should reset their password after first login
    :return:
    """
    user_data = {'username': user, 'errors': []}
    printInfo('Creating user %s...' % user)
    try:
        iam_client.create_user(UserName = user)
    except Exception as e:
        user_data['errors'].append('iam:createuser')
        return user_data
    # Add user to groups
    if type(groups) != list:
        groups = [ groups ]
    for group in groups:
        try:
            add_user_to_group(iam_client, user, group)
        except Exception as e:
            printException(e)
            user_data['errors'].append('iam:addusertogroup - %s' % group)
    # Generate password
    if with_password:
        try:
            printInfo('Creating a login profile...')
            user_data['password'] = generate_password()
            iam_client.create_login_profile(UserName = user, Password = user_data['password'] , PasswordResetRequired = require_password_reset)
        except Exception as e:
            printException(e)
            user_data['errors'].append('iam:createloginprofile')
    # Enable MFA
    if False and with_mfa:
        printInfo('Enabling MFA...')
        serial = ''
        mfa_code1 = ''
        mfa_code2 = ''
        # Create an MFA device, Display the QR Code, and activate the MFA device
        try:
            mfa_serial = False # enable_mfa(iam_client, user, '%s/qrcode.png' % user)
        except Exception as e:
            return 42
    # Request access key
    if with_access_key:
        try:
            printInfo('Creating an API access key...')
            access_key = iam_client.create_access_key(UserName=user)['AccessKey']
            user_data['AccessKeyId'] = access_key['AccessKeyId']
            user_data['SecretAccessKey'] = access_key['SecretAccessKey']
        except Exception as e:
            printException(e)
            user_data['errors'].append('iam:createaccesskey')
    return user_data
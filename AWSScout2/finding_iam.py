from AWSScout2.finding import *

# Import stock packages
import datetime

# Import third-party packages
import dateutil.parser

#
# IAM findings
#
class IamFinding(Finding):

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.keyword_prefix = 'iam'
        Finding.__init__(self, description, entity, callback, callback_args, level, questions)

    def checkAccessKeys(self, key, obj):
        for access_key in obj['AccessKeys']:
            status = self.callback_args[0]
            if len(self.callback_args) > 1:
                max_age = int(self.callback_args[1])
            else:
                max_age = 90
            self.isOlderThan(key, access_key, max_age, status)

    def belongsToGroup(self, key, obj):
        membership_count = 0
        for group in obj['Groups']:
            mandatory_groups = self.callback_args[0].split(' ')
            for mandatory_group in mandatory_groups:
                if group['GroupName'] == mandatory_group:
                    membership_count = membership_count + 1
        if membership_count < int(self.callback_args[1]):
            self.addItem(obj['Name'])

    def isOlderThan(self, key, obj, max_age, status):
        today = datetime.datetime.today()
        key_creation_date = dateutil.parser.parse(str(obj['CreateDate'])).replace(tzinfo=None)
        key_age = (today - key_creation_date).days
        key_status = obj['Status']
        if (key_age > max_age) and key_status == status:
            self.addItem(obj['AccessKeyId'], obj['UserName'])

    def lacksMFA(self, key, obj):
        # IAM user
        if 'MFADevices' in obj:
            if len(obj['MFADevices']) == 0 and 'LoginProfile' in obj:
                self.addItem(obj['Name'])
        # Root account
        elif 'user' in obj:
            if obj['user'] == '<root_account>':
                self.checkedNewItem()
                if obj['mfa_active'].lower() != 'true':
                    self.addItem('')

    def passwordAndKeyEnabled(self, key, obj):
        if len(obj['AccessKeys']) > 0 and 'LoginProfile' in obj:
            self.addItem(obj['Name'])
            return True
        else:
            return False

    def hasUserPolicy(self, key, obj):
        policy_type = self.callback_args[0]
        if policy_type in obj and len(obj[policy_type]) > 0:
            self.addItem(obj['Name'])

    def recentlyUsed(self, key, obj):
        max_age = 15
        if obj['user'] == '<root_account>':
            self.checkedNewItem()
            today = datetime.datetime.today()
            last_used_date = dateutil.parser.parse(obj['password_last_used']).replace(tzinfo=None)
            age = (today - last_used_date).days
            if (age < max_age):
                self.addItem("")

    def hasActiveKeys(self, key, obj):
        if key == '<root_account>':
            self.checkedNewItem()
            if obj['access_key_1_active'].lower() == 'true':
                self.addItem('access_key_1_active')
            if obj['access_key_2_active'].lower() == 'true':
                self.addItem('access_key_2_active')

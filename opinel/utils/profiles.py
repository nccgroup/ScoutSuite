# -*- coding: utf-8 -*-

import fileinput
import os
import re

from opinel.utils.aws import get_aws_account_id
from opinel.utils.console import printDebug
from opinel.utils.credentials import read_creds

aws_dir = os.path.join(os.path.expanduser('~'), '.aws')
aws_credentials_file = os.path.join(aws_dir, 'credentials')
aws_config_file = os.path.join(aws_dir, 'config')

re_profile_name = re.compile(r'(\[(profile\s+)?(.*?)\])')

class AWSProfile(object):

    def __init__(self, filename = None, raw_profile = None, name = None, credentials = None, account_id = None):
        self.filename = filename
        self.raw_profile = raw_profile
        self.name = name
        self.account_id = account_id
        self.attributes = {}
        if self.raw_profile:
            self.parse_raw_profile()


    def get_credentials(self):
        # For now, use the existing code...
        self.credentials = read_creds(self.name)
        try:
            self.account_id = get_aws_account_id(self.credentials)
        except:
            pass
        return self.credentials


    def set_attribute(self, attribute, value):
        self.attributes[attribute] = value


    def parse_raw_profile(self):
        for line in self.raw_profile.split('\n')[1:]:
            line = line.strip()
            if line:
                values = line.split('=')
                attribute = values[0].strip()
                value = ''.join(values[1:]).strip()
                self.attributes[attribute] = value


    def write(self):
        tmp = AWSProfiles.get(self.name, quiet = True)
        if not self.raw_profile:
            self.raw_profile = tmp[0].raw_profile if len(tmp) else None
        if not self.filename:
            self.filename = tmp[0].filename if len(tmp) else self.filename
        if not self.raw_profile:
            if 'role_arn' in self.attributes and 'source_profile' in self.attributes:
                self.filename = aws_config_file
                new_raw_profile = '\n[profile %s]' % self.name
            else:
                self.filename = aws_credentials_file
                new_raw_profile = '\n[%s]' % self.name
            for attribute in self.attributes:
                new_raw_profile += '\n%s=%s' % (attribute, self.attributes[attribute])
            with open(self.filename, 'a') as f:
                f.write(new_raw_profile)
        else:
            new_raw_profile = ''
            for line in self.raw_profile.splitlines():
                line_updated = False
                for attribute in self.attributes:
                    if line.startswith(attribute):
                        new_raw_profile += '%s=%s\n' % (attribute, self.attributes[attribute])
                        line_updated = True
                        break
                if not line_updated:
                    new_raw_profile += '%s\n' % line
            with open(self.filename, 'rt') as f:
                contents = f.read()
            contents = contents.replace(self.raw_profile, new_raw_profile)
            with open(self.filename, 'wt') as f:
                f.write(contents)



class AWSProfiles(object):

    @staticmethod
    def list(names = []):
        """
        @brief

        :return:                        List of all profile names found in .aws/config and .aws/credentials
        """
        return [p.name for p in AWSProfiles.get(names)]


    @staticmethod
    def get(names = [], quiet = False):
        """
        """
        profiles = []
        profiles += AWSProfiles.find_profiles_in_file(aws_credentials_file, names, quiet)
        profiles += AWSProfiles.find_profiles_in_file(aws_config_file, names, quiet)
        return profiles


    @staticmethod
    def find_profiles_in_file(filename, names = [], quiet = True):
        profiles = []
        if type(names) != list:
            names = [ names ]
        if not quiet:
            printDebug('Searching for profiles matching %s in %s ... ' % (str(names), filename))
        name_filters = []
        for name in names:
            name_filters.append(re.compile('^%s$' % name))
        if os.path.isfile(filename):
            with open(filename, 'rt') as f:
                aws_credentials = f.read()
                existing_profiles = re_profile_name.findall(aws_credentials)
                profile_count = len(existing_profiles) - 1
                for i, profile in enumerate(existing_profiles):
                    matching_profile = False
                    raw_profile = None
                    for name_filter in name_filters:
                        if name_filter.match(profile[2]):
                            matching_profile = True
                            i1 = aws_credentials.index(profile[0])
                            if i < profile_count:
                                i2 = aws_credentials.index(existing_profiles[i+1][0])
                                raw_profile = aws_credentials[i1:i2]
                            else:
                                raw_profile = aws_credentials[i1:]
                    if len(name_filters) == 0 or matching_profile:
                        profiles.append(AWSProfile(filename = filename, raw_profile = raw_profile, name = profile[2]))
        return profiles


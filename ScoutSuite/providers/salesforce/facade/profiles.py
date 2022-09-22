import requests
import json
from xml.etree import ElementTree

from ScoutSuite.providers.salesforce.authentication_strategy import SalesforceCredentials
from ScoutSuite.core.console import print_exception


class ProfileFacade:
    def __init__(self, credentials: SalesforceCredentials):
        self._credentials = credentials

    async def get_profiles(self):
        try:

            rest_headers = {'Authorization': 'Bearer ' + self._credentials.session_id}

            try:
                response = requests.get('https://{}/services/data/v48.0/query/?q='
                                        'SELECT+Id,Name,PermissionsApiEnabled,PermissionsApexRestServices+from+Profile'.
                                        format(self._credentials.endpoint),
                                        headers=rest_headers)
            except Exception as e:
                print_exception('Failed to get profiles: {}'.format(e))
                return []

            try:
                profile_json = json.loads(response.text)['records']
            except Exception as e:
                print_exception('Failed to parse profiles: {}'.format(e))
            else:
                return profile_json

        except Exception as e:
            print_exception('Failed to get profiles: {}'.format(e))
            return []

    async def get_profile_full_name(self, profile_id):

        try:

            rest_headers = {'Authorization': 'Bearer ' + self._credentials.session_id}

            response = requests.get('https://{}/services/data/v48.0/tooling/query/?q='
                                    'SELECT+fullName+from+Profile+WHERE+Id%3d%27{}%27'.
                                    format(self._credentials.endpoint,
                                           profile_id),
                                    headers=rest_headers)
        except Exception as e:
            print_exception('Failed to get profile full name: {}'.format(e))
            return None
        else:

            try:
                full_name = json.loads(response.text)['records'][0]['FullName']
            except Exception as e:
                print_exception('Failed to parse profile data from Tooling API: {}'.format(e))
                return None
            else:
                return full_name

    async def get_profile_login_restrictions(self, profile_full_name):

        try:

            profile_headers = {'Content-Type': 'text/xml', 'SOAPAction': '""'}
            profile_payload = '''<?xml version="1.0" encoding="utf-8"?>
                                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://soap.sforce.com/2006/04/metadata">
                                    <soapenv:Header>
                                    <tns:SessionHeader>
                                        <tns:sessionId>{}</tns:sessionId></tns:SessionHeader>
                                    </soapenv:Header>
                                    <soapenv:Body>
                                        <tns:readMetadata>
                                            <tns:type>Profile</tns:type>
                                            <tns:fullNames>{}</tns:fullNames>
                                        </tns:readMetadata>
                                    </soapenv:Body>
                                </soapenv:Envelope>'''.format(self._credentials.session_id,
                                                              profile_full_name)

            response = requests.post(self._credentials.metadata_url, data=profile_payload, headers=profile_headers)

        except Exception as e:
            print_exception('Failed to get profile login restrictions: {}'.format(e))
            return []
        else:
            try:
                # TODO
                #  "The xml.etree.ElementTree module is not secure against maliciously constructed data.
                #  If you need to parse untrusted or unauthenticated data see XML vulnerabilities."
                root = ElementTree.fromstring(response.text)
                login_ip_ranges = root.findall('.//{http://soap.sforce.com/2006/04/metadata}loginIpRanges')
            except Exception as e:
                print_exception('Failed to parse profile login restructions: {}'.format(e))
                return []
            else:
                login_ip_ranges_formated = []
                if len(login_ip_ranges) > 0:
                    for range in login_ip_ranges:
                        formated_range = '{}-{}'.format(
                            range.find('./{http://soap.sforce.com/2006/04/metadata}startAddress').text,
                            range.find('./{http://soap.sforce.com/2006/04/metadata}endAddress').text)
                        login_ip_ranges_formated.append(formated_range)
                return login_ip_ranges_formated

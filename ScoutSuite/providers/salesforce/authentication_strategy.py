import requests
import logging
from xml.etree import ElementTree

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException


class SalesforceCredentials:

    def __init__(self,
                 username,
                 endpoint,
                 session_id,
                 metadata_url):

        self.username = username
        self.endpoint = endpoint
        self.session_id = session_id
        self.metadata_url = metadata_url


class SalesforceAuthenticationStrategy(AuthenticationStrategy):
    """
    Implements authentication for the Salesforce provider
    """

    def authenticate(self,
                     sf_username,
                     sf_password,
                     sf_endpoint,
                     **kwargs):

        logging.getLogger('urllib3').setLevel(logging.ERROR)

        try:

            login_payload = '''<?xml version="1.0" encoding="utf-8" ?>
                               <env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                   xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
                                 <env:Body>
                                   <n1:login xmlns:n1="urn:partner.soap.sforce.com">
                                     <n1:username>{}</n1:username>
                                     <n1:password>{}</n1:password>
                                   </n1:login>
                                 </env:Body>
                               </env:Envelope>'''.format(sf_username, sf_password)

            login_headers = {'Content-Type': 'text/xml', 'SOAPAction': 'login'}

            try:
                # Validate the endpoint URL
                response = requests.post('https://{}/services/Soap/u/48.0'.format(sf_endpoint),
                                         data=login_payload, headers=login_headers)
            except Exception as e:
                raise AuthenticationException('Login request failed, validate endpoint: {}'.format(e))

            else:

                # TODO
                #  "The xml.etree.ElementTree module is not secure against maliciously constructed data.
                #  If you need to parse untrusted or unauthenticated data see XML vulnerabilities."
                try:
                    root = ElementTree.fromstring(response.text)
                except Exception as e:
                    raise AuthenticationException('Could not parse XML login response: {}'.format(e))
                else:
                    sessionIdElement = root.find('.//{urn:partner.soap.sforce.com}sessionId')
                    if sessionIdElement is None:
                        raise AuthenticationException('No session ID found: check credentials')
                    else:
                        session_id = sessionIdElement.text
                        metadata_url = root.find('.//{urn:partner.soap.sforce.com}metadataServerUrl').text
                        return SalesforceCredentials(sf_username, sf_endpoint,
                                                     session_id, metadata_url)

        except Exception as e:
            raise AuthenticationException(e)

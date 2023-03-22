import hmac
import hashlib
import urllib.parse
import urllib.request
from ksyun.common.common_client import CommonClient
from ksyun.common import credential
from ksyun.common.exception.ksyun_sdk_exception import KsyunSDKException
from ksyun.common.profile.client_profile import ClientProfile
from ksyun.common.profile.http_profile import HttpProfile

from ScoutSuite.core.console import print_exception


def sign(params, secret_key):
    try:
        str_encode = ''
        param_keys = sorted(params.keys())
        for key in param_keys:
            str_encode += urllib.request.quote(key, '~') + '=' + urllib.request.quote(str(params[key]), '~') + '&'

        return hmac.new(bytes(secret_key, 'utf-8'), bytes(str_encode[:-1], 'utf-8'), hashlib.sha256).hexdigest()
    except Exception as e:
        print_exception(e)
        return None


def ksc_open_api(ak, sk, endpoint, callfunc, region):
    cred = credential.Credential(ak, sk)
    httpProfile = HttpProfile()
    httpProfile.endpoint = endpoint + ".api.ksyun.com"
    httpProfile.reqMethod = "GET"
    httpProfile.reqTimeout = 60
    httpProfile.scheme = "http"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile

    common_client = CommonClient(endpoint, '2019-04-01', cred, region, profile=clientProfile)
    return common_client.call(callfunc, {})

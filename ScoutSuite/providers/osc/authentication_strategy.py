# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException
from osc_sdk_python import Gateway


class OutscaleAuthenticationStrategy(AuthenticationStrategy):
    def authenticate(self, profile=None, access=None, **kwargs):
        if profile:
            try:
                session = Gateway(**{"profile": profile})
            except Exception as e:
                raise AuthenticationException(e)
        elif access:
            session = Gateway({"custom": {
                "access_key": access[0],
                "secret_key": access[1],
                "region": "eu-west-2"
            }})
        else:
            try:
                session = Gateway()
            except Exception as e:
                raise AuthenticationException(e)
        return session
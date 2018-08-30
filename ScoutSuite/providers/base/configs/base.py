# -*- coding: utf-8 -*-

from ScoutSuite.providers.base.configs.threads import thread_configs

class GlobalConfig(object):

    def __init__(self, thread_config=4):
        """

        :param thread_config:
        """
        self.service = type(self).__name__.replace('Config','').lower()  # TODO: use regex with EOS instead of plain replace
        self.thread_config = thread_configs[thread_config]

    def get_non_provider_id(self, name):
        """
        Not all AWS resources have an ID and some services allow the use of "." in names, which break's Scout2's
        recursion scheme if name is used as an ID. Use SHA1(name) instead.

        :param name:                    Name of the resource to
        :return:                        SHA1(name)
        """
        m = sha1()
        m.update(name.encode('utf-8'))
        return m.hexdigest()

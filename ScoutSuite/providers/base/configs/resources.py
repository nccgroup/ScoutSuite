# -*- coding: utf-8 -*-

import abc


class Resources(dict, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def fetch_all(self, **kwargs):
        raise NotImplementedError()

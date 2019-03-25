from ScoutSuite.providers.aws.resources.regions import Regions

from .topics import Topics


class SNS(Regions):
    _children = [
        (Topics, 'topics')
    ]

    def __init__(self):
        super(SNS, self).__init__('sns')

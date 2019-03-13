import boto3


class AWSBaseFacade(object):
    def __init__(self, session: boto3.session.Session):
        self.session = session
        
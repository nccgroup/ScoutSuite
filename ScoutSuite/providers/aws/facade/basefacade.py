import boto3


class AWSBaseFacade:
    def __init__(self, session: boto3.session.Session = None):
        self.session = session

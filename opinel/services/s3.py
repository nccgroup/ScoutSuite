# -*- coding: utf-8 -*-


def get_s3_bucket_location(s3_client, bucket_name):
    """

    :param s3_client:
    :param bucket_name:
    :return:
    """
    location = s3_client.get_bucket_location(Bucket = bucket_name)
    return location['LocationConstraint'] if location['LocationConstraint'] else 'us-east-1'

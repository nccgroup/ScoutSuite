# -*- coding: utf-8 -*-

def get_trails(api_client):
    return api_client.describe_trails()['trailList']

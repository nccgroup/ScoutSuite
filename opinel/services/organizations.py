# -*- coding: utf-8 -*-

from opinel.utils.aws import handle_truncated_response
from opinel.utils.console import printDebug, printInfo


def get_organization_account_ids(api_client, exceptions = [], quiet = True):

    # List all accounts in the organization
    org_accounts = get_organization_accounts(api_client, exceptions, quiet)
    return [ account['Id'] for account in org_accounts ]


def get_organization_accounts(api_client, exceptions = [], quiet = True):

    # List all accounts in the organization
    org_accounts = handle_truncated_response(api_client.list_accounts, {}, ['Accounts'])['Accounts']
    if not quiet:
        printInfo('Found %d accounts in the organization.' % len(org_accounts))
        for account in org_accounts:
            printDebug(str(account))
    if len(exceptions):
        filtered_accounts = []
        for account in org_accounts:
            if account['Id'] not in exceptions:
                filtered_accounts.append(account)
        org_accounts = filtered_accounts
    return org_accounts


def get_organizational_units(api_client):
    ous = []
    roots = api_client.list_roots()['Roots']
    return get_children_organizational_units(api_client, roots)


def get_children_organizational_units(api_client, parents):
    ous = []
    for parent in parents:
        children = handle_truncated_response(api_client.list_organizational_units_for_parent, {'ParentId': parent['Id']}, ['OrganizationalUnits'])['OrganizationalUnits']
        if len(children):
            ous += get_children_organizational_units(api_client, children)
        else:
            ous.append(parent)
    return ous

def list_accounts_for_parent(api_client, parent):
    return handle_truncated_response(api_client.list_accounts_for_parent, {'ParentId': parent['Id']}, ['Accounts'])['Accounts']


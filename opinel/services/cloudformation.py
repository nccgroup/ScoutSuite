# -*- coding: utf-8 -*-

import json
import os
import re
import time

from opinel.utils.aws import connect_service, handle_truncated_response
from opinel.utils.console import printDebug, printInfo, printError, printException, prompt_4_yes_no
from opinel.utils.fs import read_file
from opinel.utils.globals import snake_to_camel, snake_to_words

re_iam_capability = re.compile('.*?AWS::IAM.*?', re.DOTALL | re.MULTILINE)

def create_cloudformation_resource_from_template(api_client, resource_type, name, template_path, template_parameters=[], tags=[], quiet=False, wait_for_completion = False, need_on_failure=False):
    """

    :param callback:
    :param name:
    :param template_path:
    :param template_parameters:
    :param quiet:
    :return:
    """
    create = getattr(api_client, 'create_%s' % resource_type)
    api_resource_type = snake_to_camel(resource_type)
    # Add a timestamps
    tags.append({'Key': 'OpinelTimestamp', 'Value': str(time.time())})
    params = prepare_cloudformation_params(name, template_path, template_parameters, api_resource_type, tags)
    if not quiet:
        printInfo('Creating the %s %s..' % (resource_type, name))
    response = create(**params)
    resource_id_attribute = '%sId' % api_resource_type
    resource_id = response[resource_id_attribute] if resource_id_attribute in response else None
    operation_id = response['OperationId'] if 'OperationId' in response else None
    if wait_for_completion:
        cloudformation_wait(api_client, resource_type, name, operation_id)
    return resource_id


def create_stack(api_client, stack_name, template_path, template_parameters=[], tags=[], quiet=False, wait_for_completion = False):
    """

    :param api_client:
    :param stack_name:
    :param template_path:
    :param template_parameters:         List of parameter keys and values
    :param quiet:
    :return:
    """
    return create_cloudformation_resource_from_template(api_client, 'stack', stack_name, template_path, template_parameters, tags, quiet, wait_for_completion, need_on_failure=True)


def create_or_update_stack(api_client, stack_name, template_path, template_parameters=[], tags=[], quiet=False, wait_for_completion = False):
    """

    :param api_client:
    :param stack_name:
    :param template_path:
    :param template_parameters:         List of parameter keys and values
    :param quiet:
    :return:
    """
    try:
        stack = api_client.describe_stacks(StackName = stack_name)
        printInfo('Stack already exists... ', newLine = False)
        stack_id = update_stack(api_client, stack_name, template_path, template_parameters, quiet, wait_for_completion)
    except Exception as e:
        if hasattr(e, 'response') and type(e.response) == dict and 'Error' in            e.response and e.response['Error']['Code'] == 'ValidationError':
            stack_id = create_stack(api_client, stack_name, template_path, template_parameters, tags, quiet, wait_for_completion)
        else:
            stack_id = None
            printException(e)
    return stack_id



def create_stack_set(api_client, stack_set_name, template_path, template_parameters=[], tags=[], quiet=False, wait_for_completion = False):
    """

    :param api_client:
    :param stack_set_name:
    :param template_path:
    :param template_parameters:
    :param quiet:
    :return:
    """
    return create_cloudformation_resource_from_template(api_client, 'stack_set', stack_set_name, template_path, template_parameters, tags, quiet, wait_for_completion)


def create_or_update_stack_set(api_client, stack_set_name, template_path, template_parameters=[], tags=[], quiet=False, wait_for_completion = False):
    """

    :param api_client:
    :param stack_name:
    :param template_path:
    :param template_parameters:         List of parameter keys and values
    :param quiet:
    :return:
    """
    operation_id = stack_set_id = None
    try:
        stack_set = api_client.describe_stack_set(StackSetName = stack_set_name)
        printInfo('Stack set already exists... ', newLine = False)
        operation_id = update_stack_set(api_client, stack_set_name, template_path, template_parameters, quiet, wait_for_completion)
    except Exception as e:
        if hasattr(e, 'response') and type(e.response) == dict and 'Error' in e.response and e.response['Error']['Code'] == 'StackSetNotFoundException':
            stack_set_id = create_stack_set(api_client, stack_set_name, template_path, template_parameters, tags, quiet, wait_for_completion)
        else:
            printException(e)
    return (stack_set_id, operation_id)


def create_stack_instances(api_client, stack_set_name, account_ids, regions, quiet=False):
    """

    :param api_client:
    :param stack_set_name:
    :param account_ids:
    :param regions:
    :return:
    """
    operation_preferences = {'FailureTolerancePercentage': 100,
       'MaxConcurrentPercentage': 100
       }
    if not quiet:
        printInfo('Creating stack instances in %d regions and %d accounts...' % (len(regions), len(account_ids)))
        printDebug(' %s' % ', '.join(regions))
    response = api_client.create_stack_instances(StackSetName=stack_set_name, Accounts=account_ids, Regions=regions, OperationPreferences=operation_preferences)
    if not quiet:
        printInfo('Successfully started operation Id %s' % response['OperationId'])
    return response['OperationId']


def delete_stack_set(api_client, stack_set_name, timeout = 60 * 5):
    """
    """
    printDebug('Deleting stack set %s' % stack_set_name)
    # Check for instances
    stack_instances = handle_truncated_response(api_client.list_stack_instances, {'StackSetName': stack_set_name}, ['Summaries'])['Summaries']
    account_ids = []
    regions = []
    if len(stack_instances) > 0:
        for si in stack_instances:
            if si['Account'] not in account_ids:
                account_ids.append(si['Account'])
            if si['Region'] not in regions:
                regions.append(si['Region'])
        operation_id = api_client.delete_stack_instances(StackSetName = stack_set_name, Accounts = account_ids, Regions = regions, RetainStacks = False)['OperationId']
        wait_for_operation(api_client, stack_set_name, operation_id)
    api_client.delete_stack_set(StackSetName = stack_set_name)


def get_stackset_ready_accounts(credentials, account_ids, quiet=True):
    """
    Verify which AWS accounts have been configured for CloudFormation stack set by attempting to assume the stack set execution role

    :param credentials:                 AWS credentials to use when calling sts:assumerole
    :param org_account_ids:             List of AWS accounts to check for Stackset configuration

    :return:                            List of account IDs in which assuming the stackset execution role worked
    """
    api_client = connect_service('sts', credentials, silent=True)
    configured_account_ids = []
    for account_id in account_ids:
        try:
            role_arn = 'arn:aws:iam::%s:role/AWSCloudFormationStackSetExecutionRole' % account_id
            api_client.assume_role(RoleArn=role_arn, RoleSessionName='opinel-get_stackset_ready_accounts')
            configured_account_ids.append(account_id)
        except Exception as e:
            pass

    if len(configured_account_ids) != len(account_ids) and not quiet:
        printInfo('Only %d of these accounts have the necessary stack set execution role:' % len(configured_account_ids))
        printDebug(str(configured_account_ids))
    return configured_account_ids


def make_awsrecipes_stack_name(template_path):
    """

    :param template_path:
    :return:
    """
    return make_prefixed_stack_name('AWSRecipes', template_path)


def make_opinel_stack_name(template_path):
    """

    :param template_path:"
    :return:
    """
    return make_prefixed_stack_name('Opinel', template_path)


def make_prefixed_stack_name(prefix, template_path):
    """

    :param prefix:
    :param template_path:
    """
    parts = os.path.basename(template_path).split('-')
    parts = parts if len(parts) == 1 else parts[:-1]
    return ('%s-%s' % (prefix, '-'.join(parts))).split('.')[0]


def prepare_cloudformation_params(stack_name, template_path, template_parameters, resource_type, tags=[], need_on_failure=False):
    """

    :param api_client:
    :param stack_name:
    :param template_path:
    :param template_parameters:         List of parameter keys and values
    :param quiet:
    :return:
    """
    printDebug('Reading CloudFormation template from %s' % template_path)
    template_body = read_file(template_path)
    params = {}
    params['%sName' % resource_type] = stack_name
    params['TemplateBody'] = template_body
    if len(template_parameters):
        params['Parameters'] = []
        it = iter(template_parameters)
        for param in it:
            printError('Param:: %s' % param)
            params['Parameters'].append({'ParameterKey': param,'ParameterValue': next(it)})

    if len(tags):
        params['Tags'] = tags
    if re_iam_capability.match(template_body):
        params['Capabilities'] = [
         'CAPABILITY_NAMED_IAM']
    if need_on_failure:
        params['OnFailure'] = 'ROLLBACK'
    return params


def update_stack(api_client, stack_name, template_path, template_parameters = [], quiet = False, wait_for_completion = False):
    """

    :param api_client:
    :param stack_name:
    :param template_path:
    :param template_parameters:         List of parameter keys and values
    :param quiet:
    :return:
    """
    update_cloudformation_resource_from_template(api_client, 'stack', stack_name, template_path, template_parameters, quiet = quiet, wait_for_completion = wait_for_completion)


def update_stack_set(api_client, stack_set_name, template_path, template_parameters=[], quiet=False, wait_for_completion = False):
    """

    :param api_client:
    :param stack_set_name:
    :param template_path:
    :param template_parameters:
    :param quiet:
    :return:
    """
    return update_cloudformation_resource_from_template(api_client, 'stack_set', stack_set_name, template_path, template_parameters, [], quiet, wait_for_completion)


def update_cloudformation_resource_from_template(api_client, resource_type, name, template_path, template_parameters=[], tags=[], quiet=False, wait_for_completion = False):
    """

    :param callback:
    :param name:
    :param template_path:
    :param template_parameters:
    :param quiet:
    :return:
    """
    try:
        update = getattr(api_client, 'update_%s' % resource_type)
        api_resource_type = snake_to_camel(resource_type)
        # Add a timestamps
        tags.append({'Key': 'OpinelTimestamp', 'Value': str(time.time())})
        params = prepare_cloudformation_params(name, template_path, template_parameters, api_resource_type, tags)
        if not quiet:
            printInfo('Updating the %s...' % resource_type, newLine=False)
        response = update(**params)
        operation_id = response['OperationId'] if resource_type == 'stack_set' else None
        if wait_for_completion:
            cloudformation_wait(api_client, resource_type, name, operation_id)

    except Exception as e:
        if api_resource_type == 'Stack' and hasattr(e, 'response') and type(e.response == dict) and e.response['Error']['Code'] == 'ValidationError' and e.response['Error']['Message'] == 'No updates are to be performed.':
            printInfo(' Already up to date.')
        else:
            printException(e)
            printError(' Failed.')


def wait_for_operation(api_client, stack_set_name, operation_id, timeout = 5 * 60, increment = 5):
    printDebug('Waiting for operation %s on stack set %s...' % (operation_id, stack_set_name))
    timer = 0
    status = ''
    while True:
        if timer >= timeout:
            printError('Timed out.')
            break
        info = api_client.describe_stack_set_operation(StackSetName = stack_set_name, OperationId = operation_id)
        status = info['StackSetOperation']['Status']
        if status not in ['RUNNING', 'STOPPING']:
            break
        printError('Operation status is \'%s\'... waiting %d seconds until next check...' % (status, increment))
        time.sleep(increment)
        timer += increment
    return 'Operation %s is %s' % (operation_id, status)


def wait_for_stack_set(api_client, stack_set_name, timeout = 60, increment = 5):
    printDebug('Waiting for stack set %s to be ready...' % stack_set_name)
    timer = 0
    while True:
        if timer >= timeout:
            printError('Timed out.')
            break
        printError('Checking the stack set\'s status...')
        time.sleep(increment)
        timer += increment
        info = api_client.describe_stack_set(StackSetName = stack_set_name)
        if info['StackSet']['Status'] == 'ACTIVE':
            break


def still_running(callback, params, resource_type):
    rc = True
    response = callback(**params)
    if resource_type == 'stack':
        status = response['Stacks'][0]['StackStatus']
        if status.endswith('_COMPLETE') or status.endswith('_FAILED'):
            rc = False
    elif resource_type == 'stack_set':
        status = response['StackSet']['Status']
        if status == 'ACTIVE':
            rc = False
    elif resource_type == 'operation':
        status = response['StackSetOperation']['Status']
        if status != 'RUNNING':
            rc = False
    return (rc, status)


def cloudformation_wait(api_client, resource_type, resource_name, operation_id = None, timeout = 5 * 60, increment = 5):
    if resource_type == 'stack':
        callback = api_client.describe_stacks
        params = {'StackName': resource_name}
    elif resource_type == 'stack_set':
        params = {'StackSetName': resource_name}
        if operation_id:
            callback = api_client.describe_stack_set_operation
            params['OperationId'] = operation_id
            resource_type = 'operation'
        else:
            callback = api_client.describe_stack_set
    else:
        printError('Unknown resource type: %s' % resource_type)
        return
    timer = 0
    while True:
        if timer >= timeout:
            printError('Timed out.')
            break
        rc, status = still_running(callback, params, resource_type)
        if rc == False:
            printInfo('Status: %s' % status)
            break
        printInfo('Status: %s... waiting %d seconds until next check...' % (status, increment))
        timer += increment
        time.sleep(increment)

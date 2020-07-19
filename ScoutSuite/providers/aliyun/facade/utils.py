import json
from ScoutSuite.providers.utils import run_concurrently
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ScoutSuite.core.console import print_exception


async def get_response(client, request):
    try:
        response = await run_concurrently(lambda: client.do_action_with_exception(request))
        response_decoded = json.loads(response)

        truncated = response_decoded.get('IsTruncated', False)

        # handle truncated responses
        while truncated:
            request.set_Marker(response_decoded['Marker'])
            response_latest = await run_concurrently(lambda: client.do_action_with_exception(request))
            response_latest_decoded = json.loads(response_latest)
            truncated = response_latest_decoded.get('IsTruncated', False)
            response_decoded = await merge_responses(response_decoded, response_latest_decoded)

        return response_decoded
    except ServerException as e:
        if False:  # TODO define exceptions to handle
            print_exception(e)
        else:
            raise
    except ClientException as e:
        if False:  # TODO define exceptions to handle
            print_exception(e)
        else:
            raise
    except Exception as e:
        print_exception(f'Unhandled exception {e} for request {request}')


async def merge_responses(response_1, response_2):
    """
    Compares two responses and adds to the second one the content of the first one, unless they are specific fields
    we don't want to overwrite.

    :param response_1: the first response
    :param response_2: the second (latest) response
    :return: modified response_2
    """
    ignored_fields = ['IsTruncated', 'RequestId', 'Marker']
    for k in response_1:
        if k not in response_2 and k not in ignored_fields:
            response_2[k] = response_1[k]
        elif k in response_2 and k not in ignored_fields:
            if type(response_1[k]) == list and type(response_2[k]) == list:
                response_2[k] += response_1[k]
            # will recursively merge until it finds a list
            elif type(response_1[k]) == dict and type(response_2[k]) == dict:
                response_2[k] = await merge_responses(response_1[k], response_2[k])
            else:
                # TODO implement other cases (which ones?)
                print_exception('Unhandled response merge')
        else:
            pass
    return response_2

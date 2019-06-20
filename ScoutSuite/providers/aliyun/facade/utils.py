import json
from ScoutSuite.providers.utils import run_concurrently
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from ScoutSuite.core.console import print_exception


async def get_response(client, request):
    # TODO handle truncated responses
    try:
        response = await run_concurrently(lambda: client.do_action_with_exception(request))
        response_decoded = json.loads(response)
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

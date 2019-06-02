import json
from ScoutSuite.providers.utils import run_concurrently
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException


async def get_response(client, request):
    # TODO handle truncated response
    try:
        response = await run_concurrently(lambda: client.do_action_with_exception(request))
        response_decoded = json.loads(response)
        return response_decoded
    except ServerException as e:
        print(e)  # TODO log
    except ClientException as e:
        print(e)  # TODO log

from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkram.request.v20150501 import ListUsersRequest

# Construct an Aliyun Client for initiating a request
# Set AccessKeyID and AccessKeySevcret when constructing the Aliyun Client
# RAM is a Global Service, and its API ingress is located in the East China 1 (Hangzhou) region.
apiClient = AcsClient(ak='TODO', secret='TODO', region_id='cn-hangzhou')

# Construct a "ListUsers" request
request = ListUsersRequest.ListUsersRequest()

# # Set the parameters
# request.set_RepoNamespace("repoNamespaceName")
# request.set_RepoName("repoName")
# request.set_Tag("tag")
# request.set_endpoint("cr.cn-hangzhou.aliyuncs.com")

try:
    # Initiate a request and obtain the response
    response = apiClient.do_action_with_exception(request)
    print(response)
except ServerException as e:
    print(e)
except ClientException as e:
    print(e)




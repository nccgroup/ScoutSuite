from oci.config import from_file
from oci.identity import IdentityClient
from oci.pagination import list_call_get_all_results

# Using a different profile from the default location
config = from_file(profile_name="test-user")
compartment_id = config["tenancy"]

# Service client
identity = IdentityClient(config)

'''
User with multiple api keys
'''
# list all users
users = list_call_get_all_results(identity.list_users, compartment_id)
for user in users.data:
    print('User: {}'.format(user.name))
    keys = list_call_get_all_results(identity.list_api_keys, user.id)

    for key in keys.data:
        print(key)
        #print('key: {}'.format(user))

'''
Policy statement applies to users
'''
# list all policies
policies = list_call_get_all_results(identity.list_policies, compartment_id)
for policy in policies.data:
    for statement in policy.statements:
        if 'allow any-user' in statement.lower():
            print(policy)
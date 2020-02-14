import json

#TODO Open the correct json file
with open('scoutsuite-report/scoutsuite-results/scoutsuite_results_aws-635327450130.js') as f:
    json_payload = f.readlines()
    json_payload.pop(0)
    json_payload = ''.join(json_payload)
    json_file = json.loads(json_payload)
    print(json_file)

    #TODO parse json_file into new JSON variable
    json_aws_account = {"AwsAccountId": json_file["account_id"]}
    print(json_aws_account)
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
    json_aws_account["CreatedAt"] = json_file["last_run"]["time"]
    json_aws_account["Description"] = json_file["services"]["config"]["findings"]["config-recorder-not-configured"]["description"]
    json_aws_account["GeneratorId"] = "PLACEHOLDER"
    json_aws_account["Id"] = "PLACEHOLDER"
    json_aws_account["ProductArn"] = "PLACEHOLDER"

    #TODO insert correct Resources
    json_aws_resources = {"test": "PLACEHOLDER"}

    json_aws_account["Resources"] = json_aws_resources

    json_aws_account["SchemaVersion"] = "PLACEHOLDER"
    json_aws_account["Severity"] = "PLACEHOLDER"
    json_aws_account["Title"] = "PLACEHOLDER"
    json_aws_account["Types"] = "PLACEHOLDER"
    json_aws_account["UpdatedAt"] = "PLACEHOLDER"

    print(json_aws_account)
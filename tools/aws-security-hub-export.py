import json

def parse_resource_security_hub(resource, json_file):
    json_aws_finding = {"AwsAccountId": json_file["account_id"]}
    json_aws_finding["CreatedAt"] = json_file["last_run"]["time"]
    json_aws_finding["Description"] = json_file["services"]["config"]["findings"]["config-recorder-not-configured"][
        "description"]
    json_aws_finding["GeneratorId"] = "PLACEHOLDER"
    json_aws_finding["Id"] = "PLACEHOLDER"
    json_aws_finding["ProductArn"] = "PLACEHOLDER"

    json_aws_resources = {"test": "PLACEHOLDER"}

    json_aws_finding["Resources"] = json_aws_resources

    json_aws_finding["SchemaVersion"] = "PLACEHOLDER"
    json_aws_finding["Severity"] = "PLACEHOLDER"
    json_aws_finding["Title"] = "PLACEHOLDER"
    json_aws_finding["Types"] = "PLACEHOLDER"
    json_aws_finding["UpdatedAt"] = "PLACEHOLDER"

    return json_aws_finding

# TODO Open the correct json file
with open('scoutsuite-report/scoutsuite-results/scoutsuite_results_aws-635327450130.js') as f:
    json_payload = f.readlines()
    json_payload.pop(0)
    json_payload = ''.join(json_payload)
    json_file = json.loads(json_payload)
    print(json_file)

    json_aws_security_hub = {"Resources": []}

    # EC2 findings
    for finding in json_file["services"]["ec2"]["findings"]:
        json_aws_security_hub["Resources"].append(parse_resource_security_hub(json_file["services"]["ec2"]["findings"][finding], json_file))
        print (parse_resource_security_hub(json_file["services"]["ec2"]["findings"][finding], json_file))

    print(json_aws_security_hub)
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

    json_aws_security_hub = {"Resources": []}

    # ACM findings
    for finding in json_file["services"]["acm"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["acm"]["findings"][finding], json_file))

    # AWSLambda findings
    for finding in json_file["services"]["awslambda"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["awslambda"]["findings"][finding], json_file))

    # Cloudformation findings
    for finding in json_file["services"]["cloudformation"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["cloudformation"]["findings"][finding], json_file))

    # Cloudtrail findings
    for finding in json_file["services"]["cloudtrail"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["cloudtrail"]["findings"][finding], json_file))

    # Cloudwatch findings
    for finding in json_file["services"]["cloudwatch"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["cloudwatch"]["findings"][finding], json_file))

    # Config findings
    for finding in json_file["services"]["config"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["config"]["findings"][finding], json_file))

    # DirectConnect findings
    for finding in json_file["services"]["directconnect"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["directconnect"]["findings"][finding], json_file))

    # EC2 findings
    for finding in json_file["services"]["ec2"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["ec2"]["findings"][finding], json_file))

    # EFS findings
    for finding in json_file["services"]["efs"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["efs"]["findings"][finding], json_file))

    # Elasticache findings
    for finding in json_file["services"]["elasticache"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["elasticache"]["findings"][finding], json_file))

    # ELB findings
    for finding in json_file["services"]["elb"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["elb"]["findings"][finding], json_file))

    # ELBv2 findings
    for finding in json_file["services"]["elbv2"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["elbv2"]["findings"][finding], json_file))

    # EMR findings
    for finding in json_file["services"]["emr"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["emr"]["findings"][finding], json_file))

    # IAM findings
    for finding in json_file["services"]["iam"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["iam"]["findings"][finding], json_file))

    # RDS findings
    for finding in json_file["services"]["rds"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["rds"]["findings"][finding], json_file))

    # Redshift findings
    for finding in json_file["services"]["redshift"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["redshift"]["findings"][finding], json_file))

    # Route53 findings
    for finding in json_file["services"]["route53"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["route53"]["findings"][finding], json_file))

    # S3 findings
    for finding in json_file["services"]["s3"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["s3"]["findings"][finding], json_file))

    # SES findings
    for finding in json_file["services"]["ses"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["ses"]["findings"][finding], json_file))

    # SNS findings
    for finding in json_file["services"]["sns"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["sns"]["findings"][finding], json_file))

    # SQS findings
    for finding in json_file["services"]["sqs"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["sqs"]["findings"][finding], json_file))

    # VPC findings
    for finding in json_file["services"]["vpc"]["findings"]:
        json_aws_security_hub["Resources"].append(
            parse_resource_security_hub(json_file["services"]["vpc"]["findings"][finding], json_file))

    print(json_aws_security_hub)
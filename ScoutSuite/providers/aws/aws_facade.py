import boto3

class AwsFacade(object):
    def get_lambda_functions(self, region):
        aws_lambda = boto3.client('lambda', region_name=region)
        
        functions = []
        
        marker = None
        while True:
            response = aws_lambda.list_functions()

            functions.extend(response['Functions'])
            marker = response.get('NextMarker', None)
            if marker is None:
                break

        return functions
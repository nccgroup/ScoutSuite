class AWSFacadeUtils:
    @staticmethod
    def get_all_pages(api_call, parse_response):
        resources = []

        while True:
            response = api_call()

            resources.extend(parse_response(response))
            marker = response.get('NextMarker', None)
            if marker is None:
                break

        return resources
class AWSFacadeUtils:
    @staticmethod
    def get_all_pages(api_call, parse_response):
        resources = []

        while True:
            response = api_call()
            resources.extend(parse_response(response))

            # TODO: this marker should be passed to te api call. Also, some calls return a NextMarker, some return a NextToken.
            marker = response.get('NextMarker', None) 
            if marker is None:
                break

        return resources
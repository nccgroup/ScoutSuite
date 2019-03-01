from typing import Callable


class AWSFacadeUtils:
    @staticmethod
    def get_all_pages(get_resources: Callable[[str], object], parse_response: Callable[[], object], next_page_marker_key: str):
        resources = []

        marker = ''
        while True:
            response = get_resources(marker)
            resources.extend(parse_response(response))

            # TODO: this marker should be passed to the api call. Also, some calls return a NextMarker, some return a NextToken.
            marker = response.get(next_page_marker_key, None) 
            if marker is None:
                break

        return resources

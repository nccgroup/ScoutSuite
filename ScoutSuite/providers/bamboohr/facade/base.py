import requests
import os

class BambooHRFacade:
    def __init__(self, credentials):
        self._credentials = credentials

    async def fetch_all(self):
        domain = os.environ.get("BAMBOOHR_DOMAIN")
        url = "https://" + str(self._credentials) + ":x@api.bamboohr.com/api/gateway.php/" + domain + "/v1/employees/directory"
        headers = {'accept': 'application/json'}

        response = requests.request("GET", url, headers=headers).json()
        result = {}

        for employee in response["employees"]:
          result[employee["id"]] = employee

        return result
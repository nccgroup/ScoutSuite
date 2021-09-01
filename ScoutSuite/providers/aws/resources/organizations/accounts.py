from ScoutSuite.providers.aws.resources.base import AWSResources


class Accounts(AWSResources):
    async def fetch_all(self):
        raw_accounts = await self.facade.organizations.get_accounts()
        for raw_account in raw_accounts:
            name, resource = self._parse_account(raw_account)
            self[name] = resource

    def _parse_account(self, raw_account):
        if raw_account["Name"] in self:
            return

        account = {}
        account["id"] = raw_account.get("Id")
        account["name"] = raw_account.get("Name")
        account["arn"] = raw_account.get("Arn")
        account["status"] = raw_account.get("Status")
        account["joined_method"] = raw_account.get("JoinedMethod")
        account["joined_timestamp"] = raw_account.get("JoinedTimestamp")

        return account["id"], account

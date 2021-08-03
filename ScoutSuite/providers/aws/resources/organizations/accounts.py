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
        account["id"] = raw_account.pop("Id")
        account["name"] = raw_account.pop("Name")
        account["arn"] = raw_account.pop("Arn")
        account["status"] = raw_account.pop("Status")
        account["joined_method"] = raw_account.pop("JoinedMethod")
        account["joined_timestamp"] = raw_account.pop("JoinedTimestamp")

        return account["id"], account

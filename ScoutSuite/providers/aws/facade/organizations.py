from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils


class OrganizationsFacade(AWSBaseFacade):
    async def get_accounts(self):

        accounts = await AWSFacadeUtils.get_all_pages(
            "organizations", None, self.session, "list_accounts", "Accounts"
        )

        return accounts

    async def get_service_policies(self):
        policies = await AWSFacadeUtils.get_all_pages(
            "organizations",
            None,
            self.session,
            "list_policies",
            "Policies",
            Filter="SERVICE_CONTROL_POLICY",
        )

        return policies

    async def get_tag_policies(self):
        policies = await AWSFacadeUtils.get_all_pages(
            "organizations",
            None,
            self.session,
            "list_policies",
            "Policies",
            Filter="TAG_POLICY",
        )

        for policy in policies:
            targets = await AWSFacadeUtils.get_all_pages(
                "organizations",
                None,
                self.session,
                "list_targets_for_policy",
                "Targets",
                PolicyId=policy["Id"],
            )
            policy["Targets"] = targets
            tags = await AWSFacadeUtils.get_all_pages(
                "organizations",
                None,
                self.session,
                "list_tags_for_resource",
                "Tags",
                ResourceId=policy["Id"],
            )
            policy["Tags"] = tags

        return policies

    async def get_backup_policies(self):
        policies = await AWSFacadeUtils.get_all_pages(
            "organizations",
            None,
            self.session,
            "list_policies",
            "Policies",
            Filter="BACKUP_POLICY",
        )

        for policy in policies:
            targets = await AWSFacadeUtils.get_all_pages(
                "organizations",
                None,
                self.session,
                "list_targets_for_policy",
                "Targets",
                PolicyId=policy["Id"],
            )
            policy["Targets"] = targets

            tags = await AWSFacadeUtils.get_all_pages(
                "organizations",
                None,
                self.session,
                "list_tags_for_resource",
                "Tags",
                ResourceId=policy["Id"],
            )
            policy["Tags"] = tags

        return policies

    async def get_optout_policies(self):
        policies = await AWSFacadeUtils.get_all_pages(
            "organizations",
            None,
            self.session,
            "list_policies",
            "Policies",
            Filter="AISERVICES_OPT_OUT_POLICY",
        )

        for policy in policies:
            targets = await AWSFacadeUtils.get_all_pages(
                "organizations",
                None,
                self.session,
                "list_targets_for_policy",
                "Targets",
                PolicyId=policy["Id"],
            )
            policy["Targets"] = targets

            tags = await AWSFacadeUtils.get_all_pages(
                "organizations",
                None,
                self.session,
                "list_tags_for_resource",
                "Tags",
                ResourceId=policy["Id"],
            )
            policy["Tags"] = tags
            childs=[]
            for target in targets:
                if target['Type'] != "ACCOUNT":
                    children = await AWSFacadeUtils.get_all_pages(
                        "organizations",
                        None,
                        self.session,
                        "list_children",
                        "Children",
                        ParentId=target['TargetId'],
                        ChildType="ACCOUNT",
                    )

                    children_ous = await AWSFacadeUtils.get_all_pages(
                        "organizations",
                        None,
                        self.session,
                        "list_children",
                        "Children",
                        ParentId=target['TargetId'],
                        ChildType="ORGANIZATIONAL_UNIT",
                    )
                    if len(children) != 0:
                        childs.append(children)
                    if len(children_ous) != 0:    
                        childs.append(children_ous)
                else:
                    acc=[]
                    acc.append({'Id':target['TargetId'], 'Type': 'ACCOUNT'})
                    childs.append(acc)
            if len(childs) != 0:
                policy["children"] = childs

        return policies

    async def add_ou(self, ids, ou_list):
        for id in ids:
            name = self.get_ou_name(id)
            ou_list.update({name: id})
            child_ids = await self.get_children(id)
            while child_ids:
                if len(child_ids) > 1:
                    await self.add_ou(child_ids, ou_list)
                    child_ids = []
                else:
                    child_name = self.get_ou_name(child_ids[0])
                    ou_list.update({child_name: child_ids[0]})
                    child_ids = await self.get_children(child_ids[0])

    def get_ou_name(self, id):
        client = AWSFacadeUtils.get_client("organizations", self.session, None)
        ou_description = client.describe_organizational_unit(OrganizationalUnitId=id)
        return ou_description["OrganizationalUnit"]["Name"]

    async def get_children(self, id):
        childs = []
        children = await AWSFacadeUtils.get_all_pages(
            "organizations",
            None,
            self.session,
            "list_children",
            "Children",
            ParentId=id,
            ChildType="ORGANIZATIONAL_UNIT",
        )
        for child in children:
            childs.append(child["Id"])
        return childs

    async def collect_ous(self):
        roots = await AWSFacadeUtils.get_all_pages(
            "organizations", None, self.session, "list_roots", "Roots"
        )
        root_id = roots[0]["Id"]
        childs = await self.get_children(root_id)
        ou_list = {"Root": root_id}
        await self.add_ou(childs, ou_list)
        return ou_list

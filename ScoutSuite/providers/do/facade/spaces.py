from botocore.exceptions import ClientError
import boto3
from ScoutSuite.core.console import print_exception, print_debug, print_warning
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently
from ScoutSuite.providers.do.authentication_strategy import DoCredentials


class SpacesFacade:
    def __init__(self, credentials: DoCredentials):
        self._credentials = credentials
        self._client = credentials.client
        self.session = credentials.session

    async def get_all_buckets(self):
        buckets = []
        # TODO no api avaialible to get do regions that support spaces.
        region_list = ["nyc3", "sfo2", "sfo3", "ams3", "fra1", "sgp1", "syd1", "blr1"]
        for region in region_list:
            region_buckets = await self.get_buckets(region)
            buckets.extend(region_buckets)
        return buckets

    async def get_buckets(self, region=None):
        try:
            buckets = []
            exception = None
            try:
                client = self.get_client("s3", self.session, region)
                buckets = await run_concurrently(
                    lambda: client.list_buckets()["Buckets"]
                )
            except Exception as e:
                exception = e
            else:
                exception = None  # Fix for https://github.com/nccgroup/ScoutSuite/issues/916#issuecomment-728783965
            if not buckets:
                if exception:
                    print_exception(f"Failed to list buckets: {exception}")
                return []
        except Exception as e:
            print_exception(f"Failed to list buckets: {e}")
            return []
        else:
            # We need first to retrieve bucket locations before retrieving bucket details
            await get_and_set_concurrently(
                [self._get_and_set_s3_bucket_location], buckets, region=region
            )

            # Then we can retrieve bucket details concurrently
            await get_and_set_concurrently(
                [
                    self._get_and_set_s3_acls,
                    self._get_CORS
                ],
                buckets,
            )
            return buckets

    async def _get_CORS(self, bucket: {}, region=None):
        client = self.get_client("s3", self.session, bucket["region"])        
        try:
            # Attempt to get the CORS configuration
            response = client.get_bucket_cors(Bucket=bucket["Name"])
            if 'CORSRules' in response:
                bucket["CORS"] = response['CORSRules']
            else:
                print("CORS rules are not set for this bucket.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidAccessKeyId':
                print("The AWS Access Key Id provided does not exist in our records.")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    async def _get_and_set_s3_bucket_location(self, bucket: {}, region=None):
        client = self.get_client("s3", self.session, region)
        try:
            location = await run_concurrently(
                lambda: client.get_bucket_location(Bucket=bucket["Name"])
            )
        except Exception as e:
            if "NoSuchBucket" in str(e) or "InvalidToken" in str(e):
                print_warning(
                    "Failed to get bucket location for {}: {}".format(bucket["Name"], e)
                )
            else:
                print_exception(
                    "Failed to get bucket location for {}: {}".format(bucket["Name"], e)
                )
            location = None

        if location:
            region = (
                location["LocationConstraint"]
                if location["LocationConstraint"]
                else "us-east-1"
            )

            # Fixes issue #59: location constraint can be either EU or eu-west-1 for Ireland...
            if region == "EU":
                region = "eu-west-1"
        else:
            region = None

        bucket["region"] = region

    async def _get_and_set_s3_acls(self, bucket: {}, key_name=None):
        bucket_name = bucket["Name"]
        client = self.get_client("s3", self.session, bucket["region"])
        try:
            grantees = {}
            if key_name:
                grants = await run_concurrently(
                    lambda: client.get_object_acl(Bucket=bucket_name, Key=key_name)
                )
            else:
                grants = await run_concurrently(
                    lambda: client.get_bucket_acl(Bucket=bucket_name)
                )
            for grant in grants["Grants"]:
                if "ID" in grant["Grantee"]:
                    grantee = grant["Grantee"]["ID"]
                    display_name = (
                        grant["Grantee"]["DisplayName"]
                        if "DisplayName" in grant["Grantee"]
                        else grant["Grantee"]["ID"]
                    )
                elif "URI" in grant["Grantee"]:
                    grantee = grant["Grantee"]["URI"].split("/")[-1]
                    display_name = self._s3_group_to_string(grant["Grantee"]["URI"])
                else:
                    grantee = display_name = "Unknown"
                permission = grant["Permission"]
                grantees.setdefault(grantee, {})
                grantees[grantee]["DisplayName"] = display_name
                if "URI" in grant["Grantee"]:
                    grantees[grantee]["URI"] = grant["Grantee"]["URI"]
                grantees[grantee].setdefault("permissions", self._init_s3_permissions())
                self._set_s3_permissions(grantees[grantee]["permissions"], permission)
            bucket["grantees"] = grantees
        except Exception as e:
            if "NoSuchBucket" in str(e) or "InvalidToken" in str(e):
                print_warning(f"Failed to get ACL configuration for {bucket_name}: {e}")
            else:
                print_exception(
                    f"Failed to get ACL configuration for {bucket_name}: {e}"
                )
            bucket["grantees"] = {}

    @staticmethod
    def get_client(service: str, session: boto3.session.Session, region: str = None):
        """
        Instantiates an AWS API client

        :param service: Service targeted, e.g. ec2
        :param session: The aws session
        :param region:  Region desired, e.g. us-east-2

        :return:
        """

        try:
            return (
                session.client(
                    service,
                    region_name=region,
                    endpoint_url="https://" + region + ".digitaloceanspaces.com",
                )
                if region
                else session.client(service)
            )
        except Exception as e:
            print_exception(f"Failed to create client for the {service} service: {e}")
            return None

    @staticmethod
    def _init_s3_permissions():
        permissions = {
            "read": False,
            "write": False,
            "read_acp": False,
            "write_acp": False,
        }
        return permissions

    @staticmethod
    def _set_s3_permissions(permissions: str, name: str):
        if name == "READ" or name == "FULL_CONTROL":
            permissions["read"] = True
        if name == "WRITE" or name == "FULL_CONTROL":
            permissions["write"] = True
        if name == "READ_ACP" or name == "FULL_CONTROL":
            permissions["read_acp"] = True
        if name == "WRITE_ACP" or name == "FULL_CONTROL":
            permissions["write_acp"] = True

    @staticmethod
    def _s3_group_to_string(uri: str):
        if uri == "http://acs.amazonaws.com/groups/global/AuthenticatedUsers":
            return "Authenticated users"
        elif uri == "http://acs.amazonaws.com/groups/global/AllUsers":
            return "Everyone"
        elif uri == "http://acs.amazonaws.com/groups/s3/LogDelivery":
            return "Log delivery"
        else:
            return uri

    @staticmethod
    def _status_to_bool(value: str):
        """Converts a string to True if it is equal to 'Enabled' or to False otherwise."""
        return value == "Enabled"

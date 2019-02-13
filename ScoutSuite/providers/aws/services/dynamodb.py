from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients


########################################
# DynamoDBRegionConfig
########################################

class DynamoDBRegionConfig(RegionConfig):
    """
    DynamoDB configuration for a single AWS region
    """

    def parse_table(self, global_params, region, table):
        """
        Parse a single table and fetch additional attributes

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param table:                   Table

        """
        api_client = api_clients[region]
        self.tables[len(self.tables)] = api_client.describe_table(TableName=table)['Table']


########################################
# DynamoDBConfig
########################################

class DynamoDBConfig(RegionalServiceConfig):
    """
    DynamoDB configuration for all AWS regions
    """

    region_config_class = DynamoDBRegionConfig

    def __init__(self, service_metadata, thread_config=4):
        super(DynamoDBConfig, self).__init__(service_metadata, thread_config)

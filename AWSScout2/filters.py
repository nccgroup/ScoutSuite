# Import AWS Scout2 filter-related classes
from AWSScout2.filter import *
from AWSScout2.filter_ec2 import *
from AWSScout2.filter_iam import *

# Import opinel
from opinel.utils import *

########################################
# filter dictionaries
########################################
cloudtrail_filter_dictionary = {}
iam_filter_dictionary = {}
ec2_filter_dictionary = {}
rds_filter_dictionary = {}
redshift_filter_dictionary = {}
s3_filter_dictionary = {}

########################################
# Common functions
########################################

#
# Populate filters from JSON configuration files
#
def load_filters(service):

    # Load filters from JSON file
    try:
        filename = 'rules/filters-' + service + '.json'
        with open(filename) as f:
            filters = json.load(f)
    except Exception as e:
        printError('Error: no filters are defined for the %s service.' % service)
        return

    # Parse rules
    for f in filters:
        new_filter(service, f,
            filters[f]['description'],
            filters[f]['entity'],
            filters[f]['callback'],
            filters[f]['callback_args'])

#
# Update the filter dictionaries
#
def new_filter(service, key, description, entity, callback_name, callback_args):
    filter_dictionary, filter_class = get_filter_variables(service)
    filter_dictionary[key] = filter_class(description, entity, callback_name, callback_args)

#
# Helper
#
def get_filter_variables(keyword):
    if keyword == 'ec2':
        return ec2_filter_dictionary, Ec2Filter
    elif keyword == 'iam':
        return iam_filter_dictionary, IamFilter
    elif keyword == 's3':
        return s3_filter_dictionary, S3Filter
    elif keyword == 'cloudtrail':
        return cloudtrail_filter_dictionary, CloudTrailFilter
    elif keyword == 'rds':
        return rds_filter_dictionary, RdsFilter
    else:
        return None, None

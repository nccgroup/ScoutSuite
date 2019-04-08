#!/usr/bin/env python

import sys

from ScoutSuite.core.cli_parser import ScoutSuiteArgumentParser
from ScoutSuite.scout import run


def main():
    parser = ScoutSuiteArgumentParser()
    args = parser.parse_args()

    # Get the dictionary to get None instead of a crash
    args = args.__dict__

    run(args.get('provider'),
        args.get('profile'),
        args.get('user_account'), args.get('service_account'),
        args.get('cli'), args.get('msi'), args.get('service_principal'), args.get('file_auth'), args.get('tenant_id'),
        args.get('subscription_id'),
        args.get('client_id'), args.get('client_secret'),
        args.get('username'), args.get('password'),
        args.get('project_id'), args.get('folder_id'), args.get('organization_id'), args.get('all_projects'),
        args.get('report_name'), args.get('report_dir'),
        args.get('timestamp'),
        args.get('services'), args.get('skipped_services'),
        args.get('thread_config'),  # todo deprecate
        args.get('database_name'),
        args.get('max_workers'),
        args.get('regions'),
        args.get('fetch_local'), args.get('update'),
        args.get('ip_ranges'), args.get('ip_ranges_name_key'),
        args.get('ruleset'), args.get('exceptions'),
        args.get('force_write'),
        args.get('debug'),
        args.get('no_browser'))


if __name__ == "__main__":
    main()
    sys.exit()

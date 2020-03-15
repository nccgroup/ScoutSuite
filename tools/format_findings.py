#!/usr/bin/env python3

from os import walk
import os
import json
import argparse
from collections import OrderedDict


def get_folder_files(folder_path):
    files = []
    for (dirpath, dirnames, filenames) in walk(folder_path):
        files.extend(filenames)
        break
    return files


def format_folder(folder_path):
    files = get_folder_files(folder_path)

    for fn in files:

        loc = '{}/{}'.format(folder_path, fn)

        with open(loc, 'r+') as json_file:
            try:
                data = json.load(json_file)
            except Exception as e:
                print('exception {} for \"{}\"'.format(e, fn))
            else:
                # change legacy field name - TODO remove once there are none left
                if 'description' in data:
                    data['title'] = data['description']
                    data.pop('description', None)
                # remove legacy HTML from rationale - TODO remove once there are none left
                if 'rationale' in data.keys():
                    data['rationale'] = data['rationale'].replace('<b>Description:</b><br><br>', '')
                    # check for legacy content - TODO remove once there are none left
                    if 'References' in data['rationale'] or 'CIS' in data['rationale']:
                        print('Potentially legacy rationale for {}: {}'.format(fn, data['rationale']))
                # back to start
                json_file.seek(0)
                # sort keys
                sort_order = ['title', 'rationale', 'remediation', 'compliance', 'references',
                              'dashboard_name', 'display_path', 'path', 'conditions',
                              'key', 'keys', 'arg_names', 'id_suffix']
                try:
                    ordered_data = OrderedDict(sorted(data.items(), key=lambda i: sort_order.index(i[0])))
                except Exception as e:
                    print('{}: {}'.format(fn, e))
                # save to file
                json.dump(ordered_data, json_file, sort_keys=False, indent=4)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Tool to help properly format findings.')
    parser.add_argument('-f', '--folder',
                        required=False,
                        help="The path of the folder containing the findings. If not provided will format all folders")
    args = parser.parse_args()

    if args.folder:
        format_folder(args.folder)
    else:
        # provider_odes = ['aliyun', 'aws', 'azure', 'gcp', 'oci']
        provider_codes = ['aws', 'gcp']

        for provider_code in provider_codes:
            current_file_dirname = os.path.dirname(__file__)
            findings_path = os.path.abspath(
                os.path.join(current_file_dirname, "../ScoutSuite/providers/{}/rules/findings/".format(provider_code)))
            print('Formatting findings in {}'.format(findings_path))
            format_folder(findings_path)

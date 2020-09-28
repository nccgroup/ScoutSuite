#!/usr/bin/env python3

import argparse
import json
import os
import sys
from collections import OrderedDict

from utils import get_capitalized_title


def get_folder_files(folder_path):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        files.extend(filenames)
        break
    return files


def format_folder(folder_path):
    print(f'Formatting findings in {folder_path}')

    files = get_folder_files(folder_path)
    finding_with_no_rationale = 0

    for fn in files:

        loc = f'{folder_path}/{fn}'

        with open(loc, 'r+') as json_file:
            try:
                data = json.load(json_file)
            except Exception as e:
                print(f'exception {e} for \"{fn}\"')
            else:
                try:
                    # change legacy field name - TODO remove once there are none left
                    if 'title' in data:
                        data['description'] = data['title']
                        data.pop('title', None)
                    # remove legacy HTML from rationale - TODO remove once there are none left
                    if 'rationale' in data.keys() and data.get('rationale'):
                        data['rationale'] = data['rationale'].replace('<b>Description:</b><br><br>', '')
                        # check for legacy content - TODO remove once there are none left
                        if 'References' in data['rationale'] or 'CIS' in data['rationale']:
                            print('Potentially legacy rationale for {}: {}'.format(fn, data['rationale']))
                    else:
                        finding_with_no_rationale += 1
                    # capitalize titles
                    data['description'] = get_capitalized_title(data['description'])
                    # back to start
                    json_file.seek(0)
                    # sort keys
                    sort_order = ['description', 'rationale', 'remediation', 'compliance', 'references',
                                  'dashboard_name', 'display_path', 'path', 'conditions',
                                  'key', 'keys', 'arg_names', 'id_suffix', 'class_suffix']
                    try:
                        ordered_data = OrderedDict(sorted(data.items(), key=lambda i: sort_order.index(i[0])))
                    except Exception as e:
                        print(f'{fn}: {e}')
                    # save to file
                    json.dump(ordered_data, json_file, sort_keys=False, indent=4)
                except Exception as e:
                    print(f'Failed to process {fn}: {e}')

    print('Found {}/{} findings with no rationale'.format(finding_with_no_rationale, len(files)))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Tool to help properly format findings.')
    parser.add_argument('-f', '--folder',
                        required=False,
                        help="The path of the folder containing the findings. If not provided will format all folders")
    args = parser.parse_args()

    if args.folder:
        if not os.path.isdir(args.folder):
            print('Error, the path provided is not valid.')
            sys.exit(1)
        else:
            format_folder(args.folder)
    else:
        provider_codes = ['aliyun', 'aws', 'azure', 'gcp', 'oci']

        for provider_code in provider_codes:
            current_file_dirname = os.path.dirname(__file__)
            findings_path = os.path.abspath(
                os.path.join(current_file_dirname, f"../ScoutSuite/providers/{provider_code}/rules/findings/"))
            format_folder(findings_path)

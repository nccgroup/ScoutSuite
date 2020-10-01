#!/usr/bin/env python3

import argparse
import json
import os
import sys


def get_folder_files(folder_path):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        files.extend(filenames)
        break
    return files


def format_folder(folder_path):
    print(f'Formatting rulesets in {folder_path}')

    files = get_folder_files(folder_path)

    for fn in files:

        loc = f'{folder_path}/{fn}'

        with open(loc, 'rt') as f:
            ruleset = json.load(f)

        ruleset = json.dumps(ruleset, indent=4, sort_keys=True)

        with open(loc, 'wt') as f:
            for line in ruleset.split('\n'):
                f.write('%s\n' % line.rstrip())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Tool to help properly format rulesets.')
    parser.add_argument('-f', '--folder',
                        required=False,
                        help="The path of the folder containing the rulesets. If not provided will format all folders")
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
            rulesets_path = os.path.abspath(
                os.path.join(current_file_dirname, f"../ScoutSuite/providers/{provider_code}/rules/rulesets/"))
            format_folder(rulesets_path)

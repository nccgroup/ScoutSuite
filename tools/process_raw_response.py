import argparse
import json
import re
from ast import literal_eval

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(name, upper=False):
    s1 = first_cap_re.sub(r'\1_\2', name)
    if upper:
        return all_cap_re.sub(r'\1_\2', s1)
    else:
        return all_cap_re.sub(r'\1_\2', s1).lower()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Tool to help parsing raw responses.')
    parser.add_argument('-p', '--provider', required=True, help="The cloud provider (e.g. \"aws\")")
    parser.add_argument('-s', '--service', required=True, help="The response's service (e.g. \"iam\")")
    parser.add_argument('-n', '--name', required=True, help="The response object's name (e.g. \"user\")")
    parser.add_argument('-v', '--value', required=True, help="The raw response")
    args = parser.parse_args()

    if args.provider not in ['aliyun', 'oci']:
        print('Provider not implemented')
        exit()

    if args.provider == 'aliyun':
        object_value_dict = literal_eval(args.value)
    elif args.provider == 'oci':
        object_value_dict = json.loads(args.value)

    parsed_html = ''

    parsed_string = ''
    parsed_string += '{}_dict = {{}}\n'.format(args.name)

    for k in object_value_dict.keys():
        parsed_string += '{}_dict[\'{}\'] = raw_{}.get(\'{}\')\n'.format(args.name, camel_to_snake(k), args.name, k)
        parsed_html += '\n<div class="list-group-item-text item-margin">{}: <span id="{}.{}s.{{{{@key}}}}.{}"><samp>{{{{{}}}}}</samp></span></div>'.format(
            camel_to_snake(k, True).replace('_', ' '), args.service, args.name, camel_to_snake(k), camel_to_snake(k))

    parsed_string += 'return {}_dict[\'id\'], {}_dict'.format(args.name, args.name)

    print(parsed_string)
    print('\n')
    print(parsed_html)

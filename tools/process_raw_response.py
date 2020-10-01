#!/usr/bin/env python3

import argparse
import json
import datetime
import re
from ast import literal_eval


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

html_boilerplate = \
"""<!-- {} {}s -->
<script id="services.{}{}.{}s.partial" type="text/x-handlebars-template">
    <div id="resource-name" class="list-group-item active">
        <h4 class="list-group-item-heading">{{{{name}}}}</h4>
    </div>
    <div class="list-group-item">
        <h4 class="list-group-item-heading">Information</h4>{}
    </div>
</script>

<script>
    Handlebars.registerPartial("services.{}{}.{}s", $("#services\\\\.{}{}\\\\.{}s\\\\.partial").html());
</script>

<!-- Single {} {} template -->
<script id="single_{}_{}-template" type="text/x-handlebars-template">
    {{{{> modal-template template='services.{}{}.{}s'}}}}
</script>
<script>
    var single_{}_{}_template = Handlebars.compile($("#single_{}_{}-template").html());
</script>"""


def camel_to_snake(name, upper=False):
    s1 = first_cap_re.sub(r'\1_\2', name)
    if upper:
        return all_cap_re.sub(r'\1_\2', s1).title()
    else:
        return all_cap_re.sub(r'\1_\2', s1).lower()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Tool to help parsing raw responses.')
    parser.add_argument('-p', '--provider', required=True, help="The cloud provider (e.g. \"aws\")")
    parser.add_argument('-s', '--service', required=True, help="The response's service (e.g. \"iam\")")
    parser.add_argument('-n', '--name', required=True, help="The response object's name (e.g. \"user\")")
    parser.add_argument('-a', '--additional-path', required=False, help="Additional path values(e.g. \"vpc\", \"subscriptions\')")
    parser.add_argument('-v', '--value', required=True, help="The raw response")
    args = parser.parse_args()

    if args.provider not in ['aws', 'azure', 'aliyun', 'gcp', 'oci']:
        # TODO support more providers
        print('Provider not implemented')
        exit()

    if args.provider == 'aws':
        object_format = 'raw_{}.get(\'{}\')'
        cleaned_value = args.value.replace('<class \'dict\'>: ', '')
        cleaned_value = args.value.replace('\}', '}')
        cleaned_value = cleaned_value.replace(", tzinfo=tzlocal()", "")
        cleaned_value = cleaned_value.replace(", tzinfo=tzutc()", "")
        object_value_dict = eval(cleaned_value)
    elif args.provider == 'azure':
        object_format = 'raw_{}.{}'
        pattern = re.compile(r'<[\w\'.:_\s]*>')
        cleaned_value = pattern.sub('None', args.value)
        cleaned_value = cleaned_value.replace(' {}', ' \'{}\'')
        object_value_dict = eval(cleaned_value)
    elif args.provider == 'aliyun':
        object_format = 'raw_{}.get(\'{}\')'
        object_value_dict = literal_eval(args.value)
    elif args.provider == 'gcp':
        object_format = 'raw_{}.{}'
        object_value_dict = json.loads(args.value)
    elif args.provider == 'oci':
        object_format = 'raw_{}.{}'
        object_value_dict = json.loads(args.value)

    parsed_html = ''

    parsed_string = ''
    parsed_string += f'{args.name}_dict = {{}}\n'

    for k in object_value_dict.keys():
        object_format_value = object_format.format(args.name, k)
        parsed_string += '{}_dict[\'{}\'] = {}\n'.format(args.name, camel_to_snake(k), object_format_value)
        parsed_html += '\n        <div class="list-group-item-text item-margin">{}: <span id="{}{}.{}s.{{{{@key}}}}.{}"><samp>{{{{value_or_none {}}}}}</samp></span></div>'.format(
            camel_to_snake(k, True).replace('_', ' '), args.service,
            '.{}.{{{{{}}}}}'.format(args.additional_path, args.additional_path[:-1]) if args.additional_path else '',
            args.name, camel_to_snake(k), camel_to_snake(k))

    parsed_string += f'return {args.name}_dict[\'id\'], {args.name}_dict'

    print(parsed_string)
    print('\n')
    print(html_boilerplate.format(
        args.service, args.name,
        args.service, f'.{args.additional_path}.id' if args.additional_path else '', args.name,
        parsed_html,
        args.service, f'.{args.additional_path}.id' if args.additional_path else '', args.name,
        args.service, f'\\\\.{args.additional_path}\\\\.id' if args.additional_path else '', args.name,
        args.service, args.name,
        args.service, args.name,
        args.service, f'.{args.additional_path}.id' if args.additional_path else '', args.name,
        args.service, args.name,
        args.service, args.name
    ))

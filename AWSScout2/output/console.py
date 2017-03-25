# -*- coding: utf-8 -*-

from AWSScout2.configs.browser import get_value_at


########################################
# Functions
########################################

def format_listall_output(format_file, format_item_dir, format, config, option_prefix = None, template = None, skip_options = False):
    """
    Prepare listall output template

    :param format_file:
    :param format_item_dir:
    :param format:
    :param config:
    :param option_prefix:
    :param template:
    :param skip_options:
    :return:
    """
    # Set the list of keys if printing from a file spec
    # _LINE_(whatever)_EOL_
    # _ITEM_(resource)_METI_
    # _KEY_(path_to_value)
    if format_file and os.path.isfile(format_file):
        if not template:
            with open(format_file, 'rt') as f:
                template = f.read()
        # Optional files
        if not skip_options:
            re_option = re.compile(r'(%_OPTION_\((.*?)\)_NOITPO_)')
            optional_files = re_option.findall(template)
            for optional_file in optional_files:
                if optional_file[1].startswith(option_prefix + '-'):
                    with open(os.path.join(format_item_dir, optional_file[1].strip()), 'rt') as f:
                        template = template.replace(optional_file[0].strip(), f.read())
        # Include files if needed
        re_file = re.compile(r'(_FILE_\((.*?)\)_ELIF_)')
        while True:
            requested_files = re_file.findall(template)
            available_files = os.listdir(format_item_dir)
            for requested_file in requested_files:
                if requested_file[1].strip() in available_files:
                    with open(os.path.join(format_item_dir, requested_file[1].strip()), 'rt') as f:
                        template = template.replace(requested_file[0].strip(), f.read())
            # Find items and keys to be printed
            re_line = re.compile(r'(_ITEM_\((.*?)\)_METI_)')
            re_key = re.compile(r'_KEY_\(*(.*?)\)', re.DOTALL|re.MULTILINE) # Remove the multiline ?
            format_item_mappings = os.listdir(format_item_dir)
            lines = re_line.findall(template)
            for (i, line) in enumerate(lines):
                lines[i] = line + (re_key.findall(line[1]),)
            requested_files = re_file.findall(template)
            if len(requested_files) == 0:
                break
    elif format and format[0] == 'csv':
        keys = config['keys']
        line = ', '.join('_KEY_(%s)' % k for k in keys)
        lines = [ (line, line, keys) ]
        template = line
    return (lines, template)


def generate_listall_output(lines, resources, aws_config, template, arguments, nodup = False):
    """
    Format and print the output of ListAll

    :param lines:
    :param resources:
    :param aws_config:
    :param template:
    :param arguments:
    :param nodup:
    :return:
    """
    for line in lines:
        output = []
        for resource in resources:
            current_path = resource.split('.')
            outline = line[1]
            for key in line[2]:
                outline = outline.replace('_KEY_('+key+')', get_value_at(aws_config['services'], current_path, key, True))
            output.append(outline)
        output = '\n'.join(line for line in sorted(set(output)))
        template = template.replace(line[0], output)
    for (i, argument) in enumerate(arguments):
        template = template.replace('_ARG_%d_' % i, argument)
    return template
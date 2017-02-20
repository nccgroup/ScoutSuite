# -*- coding: utf-8 -*-
"""
Exceptions handling
"""



def process_exceptions(aws_config, exceptions_filename = None):
    """
    DDDD

    :param aws_config:
    :param exceptions_filename:
    :return:
    """

    # Load exceptions
    if not exceptions_filename:
        return
    with open(exceptions_filename, 'rt') as f:
        exceptions = json.load(f)

    # Process exceptions
        for service in exceptions['services']:
            for rule in exceptions['services'][service]['exceptions']:
                filtered_items = []
                for item in aws_config['services'][service]['violations'][rule]['items']:
                    if item not in exceptions['services'][service]['exceptions'][rule]:
                        filtered_items.append(item)
                aws_config['services'][service]['violations'][rule]['items'] = filtered_items
                aws_config['services'][service]['violations'][rule]['flagged_items'] = len(aws_config['services'][service]['violations'][rule]['items'])
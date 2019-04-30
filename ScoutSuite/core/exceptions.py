from ScoutSuite.core.console import print_debug

from ScoutSuite.output.result_encoder import JavaScriptEncoder


class RuleExceptions(object):
    """
    Exceptions handling
    """

    def __init__(self, file_path=None):
        self.jsrw = JavaScriptEncoder()
        self.exceptions = self.jsrw.load_from_file(file_type='EXCEPTIONS',
                                                   file_path=file_path,
                                                   first_line=True)

    def process(self, cloud_provider):
        for service in self.exceptions:
            for rule in self.exceptions[service]:
                filtered_items = []
                if rule not in cloud_provider.services[service]['findings']:
                    print_debug('Warning:: key error should not be happening')
                    continue
                for item in cloud_provider.services[service]['findings'][rule]['items']:
                    if item not in self.exceptions[service][rule]:
                        filtered_items.append(item)
                cloud_provider.services[service]['findings'][rule]['items'] = filtered_items
                cloud_provider.services[service]['findings'][rule]['flagged_items'] = \
                    len(cloud_provider.services[service]['findings'][rule]['items'])

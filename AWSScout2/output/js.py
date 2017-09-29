# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import dateutil
import json
import os

from opinel.utils.console import printException, printInfo

from AWSScout2 import DEFAULT_REPORT_DIR
from AWSScout2.output.utils import get_filename, prompt_4_overwrite



class Scout2Encoder(json.JSONEncoder):
    """
    JSON encoder class
    """
    def default(self, o):
        if type(o) == datetime.datetime:
            return str(o)
        else:
            return vars(o)



class JavaScriptReaderWriter(object):
    """
    Reader/Writer for JS and JSON files
    """

    def __init__(self, profile, report_dir=None, timestamp=None):
        # self.metadata = {}
        self.report_dir = report_dir if report_dir else DEFAULT_REPORT_DIR
        self.profile = profile.replace('/', '_').replace('\\', '_')  # Issue 111
        self.current_time = datetime.datetime.now(dateutil.tz.tzlocal())
        if timestamp != False:
            self.timestamp = self.current_time.strftime("%Y-%m-%d_%Hh%M%z") if not timestamp else timestamp


    def load_from_file(self, config_type, config_path = None, first_line = None):
        if not config_path:
            config_path, first_line = get_filename(config_type, self.profile, self.report_dir)
        with open(config_path, 'rt') as f:
            json_payload = f.readlines()
            if first_line:
                json_payload.pop(0)
            json_payload = ''.join(json_payload)
        return json.loads(json_payload)


    def save_to_file(self, config, config_type, force_write, debug):
        config_path, first_line = get_filename(config_type, self.profile, self.report_dir)
        print('Saving data to %s' % config_path)
        try:
            with self.__open_file(config_path, force_write, False) as f:
                if first_line:
                    print('%s' % first_line, file=f)
                print('%s' % json.dumps(config, indent=4 if debug else None, separators=(',', ': '), sort_keys=True, cls=Scout2Encoder), file=f)
        except Exception as e:
            printException(e)


    def to_dict(self, config):
        return json.loads(json.dumps(config, separators=(',', ': '), cls=Scout2Encoder))


    def __open_file(self, config_filename, force_write, quiet=False):
        """

        :param config_filename:
        :param force_write:
        :param quiet:
        :return:
        """
        if not quiet:
            printInfo('Saving config...')
        if prompt_4_overwrite(config_filename, force_write):
            try:
                config_dirname = os.path.dirname(config_filename)
                if not os.path.isdir(config_dirname):
                    os.makedirs(config_dirname)
                return open(config_filename, 'wt')
            except Exception as e:
                printException(e)
        else:
            return None

from __future__ import print_function

import datetime
import dateutil
import json
import os
from sqlitedict import SqliteDict

from ScoutSuite.core.console import print_exception, print_info

from ScoutSuite import DEFAULT_REPORT_DIR
from ScoutSuite.output.utils import get_filename, prompt_for_overwrite


class ScoutJsonEncoder(json.JSONEncoder):
    """
    JSON encoder class
    """

    def default(self, o):
        try:
            if type(o) == datetime.datetime:
                return str(o)
            else:
                # remove unwanted attributes from the provider object during conversion to json
                if hasattr(o, 'profile'):
                    del o.profile
                if hasattr(o, 'credentials'):
                    del o.credentials
                if hasattr(o, 'metadata_path'):
                    del o.metadata_path
                if hasattr(o, 'services_config'):
                    del o.services_config
                return vars(o)
        except Exception as e:
            return str(o)


class ScoutResultEncoder(object):
    def __init__(self, profile, report_dir=None, timestamp=None):
        self.report_dir = report_dir if report_dir else DEFAULT_REPORT_DIR
        self.profile = profile.replace('/', '_').replace('\\', '_')  # Issue 111
        self.current_time = datetime.datetime.now(dateutil.tz.tzlocal())
        if timestamp:
            self.timestamp = self.current_time.strftime("%Y-%m-%d_%Hh%M%z") if not timestamp else timestamp

    @staticmethod
    def to_dict(config):
        return json.loads(json.dumps(config, separators=(',', ': '), cls=ScoutJsonEncoder))


class SqlLiteEncoder(ScoutResultEncoder):
    def load_from_file(self, config_type, config_path=None):
        if not config_path:
            config_path, _ = get_filename(config_type, self.profile, self.report_dir)
        return SqliteDict(config_path, autocommit=True).data

    def save_to_file(self, config, config_type, force_write, _debug):
        config_path, first_line = get_filename(config_type, self.profile, self.report_dir, extension="db")
        print('Saving data to %s' % config_path)
        try:
            with self.__open_file(config_path, force_write, False) as database:
                result_dict = self.to_dict(config)
                for k, v in result_dict.items():
                    database[k] = v
                database.commit()
        except Exception as e:
            print_exception(e)

    @staticmethod
    def __open_file(config_filename, force_write, quiet=False):
        """

        :param config_filename:
        :param force_write:
        :param quiet:
        :return:
        """
        if not quiet:
            print_info('Saving config...')
        if prompt_for_overwrite(config_filename, force_write):
            try:
                config_dirname = os.path.dirname(config_filename)
                if not os.path.isdir(config_dirname):
                    os.makedirs(config_dirname)
                if os.path.exists(config_filename):
                    os.remove(config_filename)
                return SqliteDict(config_filename)
            except Exception as e:
                print_exception(e)
        else:
            return None


class JavaScriptEncoder(ScoutResultEncoder):
    """
    Reader/Writer for JS and JSON files
    """

    def load_from_file(self, config_type, config_path=None, first_line=None):
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
                print('%s' % json.dumps(config, indent=4 if debug else None, separators=(',', ': '), sort_keys=True,
                                        cls=ScoutJsonEncoder), file=f)
        except AttributeError as e:
            # __open_file returned None
            pass
        except Exception as e:
            print_exception(e)

    @staticmethod
    def __open_file(config_filename, force_write, quiet=False):
        """

        :param config_filename:
        :param force_write:
        :param quiet:
        :return:
        """
        if not quiet:
            print_info('Saving config...')
        if prompt_for_overwrite(config_filename, force_write):
            try:
                config_dirname = os.path.dirname(config_filename)
                if not os.path.isdir(config_dirname):
                    os.makedirs(config_dirname)
                return open(config_filename, 'wt')
            except Exception as e:
                print_exception(e)
        else:
            return None

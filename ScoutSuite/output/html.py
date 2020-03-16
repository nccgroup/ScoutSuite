from __future__ import print_function

import datetime
import os
import shutil
import zipfile

import dateutil.tz

from ScoutSuite import DEFAULT_INCLUDES_DIRECTORY
from ScoutSuite import DEFAULT_REPORT_DIRECTORY, DEFAULT_REPORT_RESULTS_DIRECTORY, DEFAULT_INCLUDES_DIRECTORY
from ScoutSuite import ERRORS_LIST
from ScoutSuite.core.console import print_info, print_exception
from ScoutSuite.output.result_encoder import JavaScriptEncoder, SqlLiteEncoder
from ScoutSuite.output.utils import get_filename, prompt_for_overwrite


class HTMLReport(object):
    """
    Base HTML report
    """

    def __init__(self, report_name=None, report_dir=None, timestamp=False, exceptions=None, result_format=None):

        self.report_name = report_name
        self.report_name = report_name.replace('/', '_').replace('\\', '_')  # Issue 111
        self.report_dir = report_dir if report_dir else DEFAULT_REPORT_DIRECTORY
        self.current_time = datetime.datetime.now(dateutil.tz.tzlocal())
        self.timestamp = self.current_time.strftime("%Y-%m-%d_%Hh%M%z") if not timestamp else timestamp

        # exceptions = {} if exceptions is None else exceptions
        self.exceptions = exceptions if exceptions else {}
        self.scout_report_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        self.html_data_path = os.path.join(self.scout_report_data_path, 'html')
        self.exceptions_encoder = JavaScriptEncoder(self.report_name, report_dir, timestamp)

        if result_format == "sqlite":
            self.encoder = SqlLiteEncoder(self.report_name, report_dir, timestamp)
        else:
            self.encoder = JavaScriptEncoder(self.report_name, report_dir, timestamp)

    def get_content_from_folder(self, templates_type):
        contents = ''
        template_dir = os.path.join(self.html_data_path, templates_type)
        template_files = [os.path.join(template_dir, f) for f in os.listdir(template_dir) if
                          os.path.isfile(os.path.join(template_dir, f))]
        for filename in template_files:
            try:
                with open('%s' % filename, 'rt') as f:
                    contents = contents + f.read()
            except Exception as e:
                print_exception('Error reading filename %s: %s' % (filename, e))
        return contents

    def get_content_from_file(self, filename):
        contents = ''
        template_dir = os.path.join(self.html_data_path, 'conditionals')
        filename = template_dir + filename
        try:
            with open('%s' % filename, 'rt') as f:
                contents = contents + f.read()
        except Exception as e:
            print_exception('Error reading filename %s: %s' % (filename, e))
        return contents

    def prepare_html_report_dir(self):
        if not os.path.isdir(self.report_dir):
            os.makedirs(self.report_dir)
        run_results_dir = os.path.join(self.report_dir, DEFAULT_REPORT_RESULTS_DIRECTORY)
        if not os.path.isdir(run_results_dir):
            os.makedirs(run_results_dir)
        # Copy static 3rd-party files
        archive = os.path.join(self.scout_report_data_path, 'includes.zip')
        zip_ref = zipfile.ZipFile(archive)
        zip_ref.extractall(self.report_dir)
        zip_ref.close()
        # Copy static files
        inc_scout_dir = os.path.join(self.report_dir, DEFAULT_INCLUDES_DIRECTORY)
        src_inc_scout_dir = os.path.join(self.scout_report_data_path, DEFAULT_INCLUDES_DIRECTORY)
        if os.path.isdir(inc_scout_dir):
            shutil.rmtree(inc_scout_dir)
        shutil.copytree(src_inc_scout_dir, inc_scout_dir)


class ScoutReport(HTMLReport):
    """
    Scout HTML report
    """

    def __init__(self, provider, report_name=None, report_dir=None, timestamp=False, exceptions=None,
                 result_format='json'):
        exceptions = {} if exceptions is None else exceptions
        self.provider = provider
        self.result_format = result_format

        super(ScoutReport, self).__init__(report_name, report_dir, timestamp, exceptions, result_format)

    def save(self, config, exceptions, force_write=False, debug=False):
        self.prepare_html_report_dir()
        self.encoder.save_to_file(config, 'RESULTS', force_write, debug)
        self.exceptions_encoder.save_to_file(exceptions, 'EXCEPTIONS', force_write, debug)
        if ERRORS_LIST:
            self.exceptions_encoder.save_to_file(ERRORS_LIST, 'ERRORS', force_write, debug=True)
        return self.create_html_report(force_write)

    def create_html_report(self, force_write):
        contents = ''
        # Use the script corresponding to the result format
        contents += self.get_content_from_file('/%s_format.html' % self.result_format)
        # Use all scripts under html/partials/
        contents += self.get_content_from_folder('partials')
        contents += self.get_content_from_folder('partials/%s' % self.provider)
        # Use all scripts under html/summaries/
        contents += self.get_content_from_folder('summaries')
        contents += self.get_content_from_folder('summaries/%s' % self.provider)
        new_file, first_line = get_filename('REPORT', self.report_name, self.report_dir)
        print_info('Creating %s' % new_file)
        if prompt_for_overwrite(new_file, force_write):
            if os.path.exists(new_file):
                os.remove(new_file)
            with open(os.path.join(self.html_data_path, 'report.html')) as f:
                with open(new_file, 'wt') as nf:
                    for line in f:
                        newline = line
                        newline = newline.replace('<!-- CONTENTS PLACEHOLDER -->', contents)
                        newline = newline.replace('<!-- RESULTS PLACEHOLDER -->',
                                                  get_filename('RESULTS',
                                                               self.report_name,
                                                               self.report_dir,
                                                               relative_path=True)[0])
                        newline = newline.replace('<!-- EXCEPTIONS PLACEHOLDER -->',
                                                  get_filename('EXCEPTIONS',
                                                               self.report_name,
                                                               self.report_dir,
                                                               relative_path=True)[0])
                        newline = newline.replace('<!-- SQLITE JS PLACEHOLDER -->',
                                                  '{}/sqlite.js'.format(DEFAULT_INCLUDES_DIRECTORY))
                        nf.write(newline)
        return new_file

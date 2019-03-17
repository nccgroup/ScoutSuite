# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import os
import shutil
import zipfile

import dateutil.tz
from ScoutSuite.core.console import print_info, print_exception

from ScoutSuite import AWSCONFIG, EXCEPTIONS, HTMLREPORT, AWSCONFIG_FILE, EXCEPTIONS_FILE, HTMLREPORT_FILE
from ScoutSuite.output.result_encoder import JavaScriptEncoder, SqlLiteEncoder
from ScoutSuite.output.utils import get_filename, prompt_for_overwrite


class HTMLReport(object):
    """
    Base HTML report
    """

    def __init__(self, profile, report_dir, timestamp=False, exceptions=None, result_format=None):
        exceptions = {} if exceptions is None else exceptions
        self.report_dir = report_dir
        self.profile = profile.replace('/', '_').replace('\\', '_')  # Issue 111
        self.current_time = datetime.datetime.now(dateutil.tz.tzlocal())
        if timestamp:
            self.timestamp = self.current_time.strftime("%Y-%m-%d_%Hh%M%z") if not timestamp else timestamp
            self.profile = '%s-%s' % (self.profile, self.timestamp)
        self.exceptions = exceptions
        self.scout2_report_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        self.html_data_path = os.path.join(self.scout2_report_data_path, 'html')

        if result_format == "sqlite":
            self.encoder = SqlLiteEncoder(self.profile, report_dir, timestamp)
        else:
            self.encoder = JavaScriptEncoder(self.profile, report_dir, timestamp)

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
        run_results_dir = os.path.join(self.report_dir, 'scoutsuite-results')
        if not os.path.isdir(run_results_dir):
            os.makedirs(run_results_dir)
        # Copy static 3rd-party files
        archive = os.path.join(self.scout2_report_data_path, 'includes.zip')
        zip_ref = zipfile.ZipFile(archive)
        zip_ref.extractall(self.report_dir)
        zip_ref.close()
        # Copy static files
        inc_scout2_dir = os.path.join(self.report_dir, 'inc-scoutsuite')
        src_inc_scout2_dir = os.path.join(self.scout2_report_data_path, 'inc-scoutsuite')
        if os.path.isdir(inc_scout2_dir):
            shutil.rmtree(inc_scout2_dir)
        shutil.copytree(src_inc_scout2_dir, inc_scout2_dir)


class Scout2Report(HTMLReport):
    """
    Scout Suite HTML report
    """

    def __init__(self, provider, profile=None, report_dir=None, timestamp=False, exceptions=None, result_format=None):
        exceptions = {} if exceptions is None else exceptions
        self.html_root = HTMLREPORT_FILE
        self.provider = provider
        self.result_format = result_format
        super(Scout2Report, self).__init__(profile, report_dir, timestamp, exceptions, result_format)

    def save(self, config, exceptions, force_write=False, debug=False):
        self.prepare_html_report_dir()
        self.encoder.save_to_file(config, AWSCONFIG, force_write, debug)
        self.encoder.save_to_file(exceptions, EXCEPTIONS, force_write, debug)
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

        new_file, first_line = get_filename(HTMLREPORT, self.profile, self.report_dir)
        print_info('Creating %s ...' % new_file)
        if prompt_for_overwrite(new_file, force_write):
            if os.path.exists(new_file):
                os.remove(new_file)
            with open(os.path.join(self.html_data_path, self.html_root)) as f:
                with open(new_file, 'wt') as nf:
                    for line in f:
                        newline = line
                        newline = newline.replace('<!-- PLACEHOLDER -->', contents)
                        if self.profile != 'default':
                            newline = newline.replace(AWSCONFIG_FILE,
                                                      AWSCONFIG_FILE.replace('.js', '-%s.js' % self.profile))
                            newline = newline.replace(EXCEPTIONS_FILE,
                                                      EXCEPTIONS_FILE.replace('.js', '-%s.js' % self.profile))
                        nf.write(newline)
        return new_file

# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import dateutil.tz
import os
import shutil
import zipfile

from opinel.utils.console import printInfo

from AWSScout2 import AWSCONFIG, EXCEPTIONS, HTMLREPORT, AWSRULESET, AWSCONFIG_FILE, EXCEPTIONS_FILE, HTMLREPORT_FILE, GENERATOR_FILE, REPORT_TITLE
from AWSScout2.output.utils import get_filename, prompt_4_overwrite
from AWSScout2.output.js import JavaScriptReaderWriter



class HTMLReport(object):
    """
    Base HTML report
    """

    def __init__(self, profile, report_dir, timestamp = False, exceptions = {}):
        self.report_dir = report_dir
        self.profile = profile.replace('/', '_').replace('\\', '_') # Issue 111
        self.current_time = datetime.datetime.now(dateutil.tz.tzlocal())
        if timestamp != False:
            self.timestamp = self.current_time.strftime("%Y-%m-%d_%Hh%M%z") if not timestamp else timestamp
            self.profile = '%s-%s' % (self.profile, self.timestamp)
        self.exceptions = exceptions
        self.scout2_report_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        self.html_data_path = os.path.join(self.scout2_report_data_path, 'html')
        self.jsrw = JavaScriptReaderWriter(self.profile, report_dir, timestamp)

    def get_content_from(self, templates_type):
        contents = ''
        template_dir  = os.path.join(self.html_data_path, templates_type)
        template_files = [os.path.join(template_dir, f) for f in os.listdir(template_dir) if os.path.isfile(os.path.join(template_dir, f))]
        for filename in template_files:
            with open('%s' % filename, 'rt') as f:
                contents = contents + f.read()
        return contents

    def prepare_html_report_dir(self):
        if not os.path.isdir(self.report_dir):
            os.makedirs(self.report_dir)
        aws_config_dir = os.path.join(self.report_dir, 'inc-awsconfig')
        if not os.path.isdir(aws_config_dir):
            os.makedirs(aws_config_dir)
        # Copy static 3rd-party files
        archive = os.path.join(self.scout2_report_data_path, 'includes.zip')
        zip_ref = zipfile.ZipFile(archive)
        zip_ref.extractall(self.report_dir)
        zip_ref.close()
        # Copy static files
        inc_scout2_dir = os.path.join(self.report_dir, 'inc-scout2')
        src_inc_scout2_dir = os.path.join(self.scout2_report_data_path, 'inc-scout2')
        if os.path.isdir(inc_scout2_dir):
            shutil.rmtree(inc_scout2_dir)
        shutil.copytree(src_inc_scout2_dir, inc_scout2_dir)



class Scout2Report(HTMLReport):
    """
    Scout2 HTML report
    """

    def __init__(self, profile, report_dir = None, timestamp = False, exceptions = {}):
        self.html_root = HTMLREPORT_FILE
        super(Scout2Report, self).__init__(profile, report_dir, timestamp, exceptions)

    def save(self, config, exceptions, force_write = False, debug = False):
        self.prepare_html_report_dir()
        self.jsrw.save_to_file(config, AWSCONFIG, force_write, debug)
        self.jsrw.save_to_file(exceptions, EXCEPTIONS, force_write, debug)
        return self.create_html_report(force_write)

    def create_html_report(self, force_write):
        contents = ''
        # Use all scripts under html/partials/
        contents += self.get_content_from('partials')
        # Use all scripts under html/summaries/
        contents += self.get_content_from('summaries')
        new_file, first_line = get_filename(HTMLREPORT, self.profile, self.report_dir)
        printInfo('Creating %s ...' % new_file)
        if prompt_4_overwrite(new_file, force_write):
            if os.path.exists(new_file):
                os.remove(new_file)
            with open(os.path.join(self.html_data_path, self.html_root)) as f:
                with open(new_file, 'wt') as nf:
                    for line in f:
                        newline = line.replace(REPORT_TITLE, REPORT_TITLE + ' [' + self.profile + ']')
                        if self.profile != 'default':
                            new_config_filename = AWSCONFIG_FILE.replace('.js', '-%s.js' % self.profile)
                            new_exceptions_filename = EXCEPTIONS_FILE.replace('.js', '-%s.js' % self.profile)
                            newline = newline.replace(AWSCONFIG_FILE, new_config_filename)
                            newline = newline.replace(EXCEPTIONS_FILE, new_exceptions_filename)
                        newline = newline.replace('<!-- PLACEHOLDER -->', contents)
                        nf.write(newline)
        return new_file



class RulesetGenerator(HTMLReport):
    """
    HTML ruleset generator for Scout2
    """

    def __init__(self, ruleset_name, report_dir = None, timestamp = False, exceptions = {}):
        self.html_root = GENERATOR_FILE
        self.ruleset_name = ruleset_name
        super(RulesetGenerator, self).__init__(ruleset_name, report_dir, timestamp, exceptions)

    def create_html_report(self, force_write):
        src_rule_generator = os.path.join(self.html_data_path, GENERATOR_FILE)
        rule_generator = os.path.join(self.report_dir, GENERATOR_FILE)
        shutil.copyfile(src_rule_generator, rule_generator)
        return rule_generator

    def save(self, config, force_write = False, debug = False):
        self.prepare_html_report_dir()
        self.jsrw.save_to_file(config, AWSRULESET, force_write, debug)
        return self.create_html_report(force_write)

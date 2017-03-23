#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from opinel.utils import printException, printInfo, prompt_4_overwrite

import datetime
import dateutil
import json
import os
import shutil
import sys
import zipfile



########################################
# Globals
########################################

DEFAULT_REPORT_DIR = 'scout2-report'
AWSCONFIG_FILE = 'inc-awsconfig/aws_config.js'
EXCEPTIONS_FILE = 'inc-awsconfig/exceptions.js'
REPORT_FILE = 'report.html'

REPORT_TITLE  = 'AWS Scout2 Report'



########################################
# Classes
########################################

class Scout2Report(object):
    """
    HTML report
    """

    def __init__(self, environment_name, report_dir = None, timestamp = None, exceptions = {}):
        self.report_dir = report_dir if report_dir else DEFAULT_REPORT_DIR
        self.environment_name = environment_name.replace('/', '_').replace('\\', '_') # Issue 111
        self.current_time = datetime.datetime.now(dateutil.tz.tzlocal())
        if timestamp != False:
            self.timestamp = self.current_time.strftime("%Y-%m-%d_%Hh%M%z") if not timestamp else timestamp
            self.environment_name = '%s-%s' % (self.environment_name, self.timestamp)
        self.exceptions = exceptions
        self.scout2_report_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


    def __prepare_scout2_report_dir(self):
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


    def save(self, aws_config, exceptions, last_run, force_write = False, debug = False):
        if type(aws_config) == dict:
            aws_config['last_run'] = last_run
        self.__prepare_scout2_report_dir()
        self.__save_config_to_file(aws_config, 'config', force_write, debug)
        self.__save_config_to_file(exceptions, 'exceptions', force_write, debug)
        self.create_html_report(force_write)


    def __get_content_from(self, templates_type):
        contents = ''
        template_path = os.path.join(self.scout2_report_data_path, 'html')
        template_dir  = os.path.join(template_path, templates_type)
        template_files = [os.path.join(template_dir, f) for f in os.listdir(template_dir) if os.path.isfile(os.path.join(template_dir, f))]
        for filename in template_files:
            with open('%s' % filename, 'rt') as f:
                contents = contents + f.read()
        return contents


    def create_html_report(self, force_write):
        templates_path = os.path.join(self.scout2_report_data_path, 'html')
        contents = ''
        # Use all scripts under html/partials/
        contents += self.__get_content_from('partials')
        # Use all scripts under html/summaries/
        contents += self.__get_content_from('summaries')
        new_file, first_line = self.get_filename('report')
        printInfo('Creating %s ...' % new_file)
        if prompt_4_overwrite(new_file, force_write):
            if os.path.exists(new_file):
                os.remove(new_file)
            with open(os.path.join(templates_path, 'report.html')) as f:
                with open(new_file, 'wt') as nf:
                    for line in f:
                        newline = line.replace(REPORT_TITLE, REPORT_TITLE + ' [' + self.environment_name + ']')
                        if self.environment_name != 'default':
                            new_config_filename = AWSCONFIG_FILE.replace('.js', '-%s.js' % self.environment_name)
                            new_exceptions_filename = EXCEPTIONS_FILE.replace('.js', '-%s.js' % self.environment_name)
                            newline = newline.replace(AWSCONFIG_FILE, new_config_filename)
                            newline = newline.replace(EXCEPTIONS_FILE, new_exceptions_filename)
                        newline = newline.replace('<!-- PLACEHOLDER -->', contents)
                        nf.write(newline)


    def get_filename(self, file_type):
        """

        :param environment_name:
        :param type:
        :return:
        """
        if file_type == 'config':
            filename = AWSCONFIG_FILE
            first_line = 'aws_info ='
        elif file_type == 'exceptions':
            filename = EXCEPTIONS_FILE
            first_line = 'exceptions ='
        elif file_type == 'report':
            filename = REPORT_FILE
            first_line = None
        if self.environment_name != 'default':
            name, extention = filename.split('.')
            filename = '%s-%s.%s' % (name, self.environment_name, extention)
        return (os.path.join(self.report_dir, filename), first_line)


    def __save_config_to_file(self, aws_config, config_type, force_write, debug):
        config_path, first_line = self.get_filename(config_type)
        try:
            with open_file(config_path, force_write, False) as f:
                if first_line:
                    print('%s' % first_line, file=f)
                print('%s' % json.dumps(aws_config, indent=4 if debug else None, separators=(',', ': '), sort_keys=True,
                                        cls=Scout2Encoder), file=f)
        except Exception as e:
            printException(e)


    def load(self):
        config_path, first_line = self.get_filename('config')
        print('Config: %s' % config_path)
        with open(config_path, 'rt') as f:
            json_payload = f.readlines()
            if first_line:
                json_payload.pop(0)
            json_payload = ''.join(json_payload)
        return json.loads(json_payload)



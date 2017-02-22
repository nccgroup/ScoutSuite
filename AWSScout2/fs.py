#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from opinel.utils import printException, printError, printInfo, printDebug, prompt_4_overwrite
from AWSScout2.utils import Scout2Encoder

import glob
import json
import os
import zipfile

DEFAULT_REPORT_DIR = 'scout2-report'
AWSCONFIG_FILE = 'inc-awsconfig/aws_config.js'
EXCEPTIONS_FILE = 'inc-awsconfig/exceptions.js'
REPORT_FILE = 'report.html'

REPORT_TITLE  = 'AWS Scout2 Report'

class Scout2Report(object):

    def __init__(self, environment_name, report_dir = None, timestamp = None, exceptions = {}):
        self.report_dir = report_dir if report_dir else DEFAULT_REPORT_DIR
        self.environment_name = environment_name.replace('/', '_').replace('\\', '_') # Issue 111
        if timestamp:
            self.environment_name = '%s-%s' % (self.environment_name, timestamp)
        self.exceptions = exceptions
        self.scout2_path = os.path.dirname(os.path.realpath(__file__))

    def __prepare_scout2_report_dir(self):
        if not os.path.isdir(self.report_dir):
            os.makedirs(self.report_dir)
        aws_config_dir = os.path.join(self.report_dir, 'inc-awsconfig')
        if not os.path.isdir(aws_config_dir):
            os.makedirs(aws_config_dir)
        # Copy static files
        scout2_data_path = os.path.join(self.scout2_path, 'data')
        archive = os.path.join(scout2_data_path, 'includes.zip')
        zip_ref = zipfile.ZipFile(archive)
        zip_ref.extractall(self.report_dir)
        zip_ref.close()


    def save(self, aws_config, exceptions, force_write = False, debug = False):
        self.__prepare_scout2_report_dir()
        self.__save_config_to_file(aws_config, 'config', force_write, debug)
        self.__save_config_to_file(exceptions, 'exceptions', force_write, debug)
        self.create_html_report(force_write)


    def __get_content_from(self, templates_type):
        contents = ''
        template_path = os.path.join(self.scout2_path, 'data/html')
        template_dir  = os.path.join(template_path, templates_type)
        template_files = [os.path.join(template_dir, f) for f in os.listdir(template_dir) if os.path.isfile(os.path.join(template_dir, f))]
        for filename in template_files:
            with open('%s' % filename, 'rt') as f:
                contents = contents + f.read()
        return contents


    def create_html_report(self, force_write):
        templates_path = os.path.join(self.scout2_path, 'data/html')
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
                            newline = newline.replace(def_config_filename, new_config_filename)
                            newline = newline.replace(def_exceptions_filename, new_exceptions_filename)
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

        #save_config_to_file(self.report_dir, self.environment_name, 'config', aws_config, force_write, debug)



def load_from_json(environment_name, config_filename = None):
    if not config_filename:
        report_filename, config_filename = get_scout2_paths(environment_name)
    with open(config_filename) as f:
        json_payload = f.readlines()
        json_payload.pop(0)
        json_payload = ''.join(json_payload)
        return json.loads(json_payload)




def open_file(config_filename, force_write, quiet = False):
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






# -*- coding: utf-8 -*-

import unittest
from ScoutSuite.core.console import *

class TestOpinelUtilsConsoleClass(unittest.TestCase):

    def test_configPrintException(self):
        set_logger_configuration(False)
        set_logger_configuration(True)


    def test_printDebug(self):
        print_debug('hello')


    def test_printError(self):
        print_error('hello')


    def test_printException(self):
        set_logger_configuration(True)
        try:
            raise Exception('opinelunittest')
        except Exception as e:
            print_exception(e)
        set_logger_configuration(False)
        try:
            raise Exception('opinelunittest')
        except Exception as e:
            print_exception(e)
        try:
            raise Exception('opinelunittest')
        except Exception as e:
            print_exception(e, True)


    def test_printInfo(msg, newLine=True):
        print_info('hello')


    def test_printGeneric(self):
        print_generic('hello')


    def test_prompt(self):
        assert prompt('a') == 'a'
        assert prompt('') == ''
        test = ['a', 'b']
        assert prompt(test) == 'a'
        assert prompt(test) == 'b'
        assert prompt(test) == ''


    def test_prompt_4_value(self):
        assert prompt_value('prompt_4_value', no_confirm=True, test_input='inputvalue') == 'inputvalue'
        assert prompt_value('prompt_4_value', no_confirm=True, is_question=True, test_input='inputvalue') == 'inputvalue'
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], no_confirm=True, test_input='b') == 'b'
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], display_choices=False, no_confirm=True, test_input='b') == 'b'
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], display_indices=True, no_confirm=True, test_input='1') == 'b'
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], default='b', no_confirm=True, test_input='') == 'b'
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], no_confirm=True, authorize_list=True, test_input='a,b') == 'a,b'
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], required=True, no_confirm=True, test_input=['', 'b']) == 'b'
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], required=True, no_confirm=True, test_input=['invalid', 'b']) == 'b'
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], no_confirm=True, test_input='a,c') == None
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], no_confirm=True, test_input='a,b', authorize_list = True) == 'a,b'
        assert prompt_value('prompt_4_value', choices=['a', 'b', 'c'], no_confirm=True, test_input='a,e', authorize_list = True) == None

    def test_prompt_4_yes_no(self):
        assert prompt_yes_no('hello', 'N') == False
        assert prompt_yes_no('hello', 'no') == False
        assert prompt_yes_no('hello', 'Y') == True
        assert prompt_yes_no('hello', 'yes') == True
        assert prompt_yes_no('hello', ['foo', 'bar', 'no']) == False
        assert prompt_yes_no('hello', 'Ye') == None
        assert prompt_yes_no('hello', 'Non') == None
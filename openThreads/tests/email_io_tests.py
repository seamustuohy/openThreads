import unittest
import sys
import inspect
import re
import openThreads
import os

from openThreads import email_io

class testFunctions(unittest.TestCase):

    def setUp(self):
        self.list_file = "data/test_case/testEmail"
        self.unittest_name = testFunctions
        self.module = email_io
        self.module_class = False

    def test_all_tests(self):
        function_list = []
        test_suite = []
        if self.module_class != False:
            class_functions = inspect.getmembers(self.module_class, inspect.ismethod)
            #If Class Exists in module
            for i in class_functions:
                if re.match("^(?!__init__).*", i[0]):
                    function_list.append("test_"+i[0])

        functions = inspect.getmembers(self.module, inspect.isfunction)
        tests = inspect.getmembers(self.unittest_name, inspect.ismethod)

    #check for tests
        for i in tests:
            if re.match("^test_(?!all_tests).*", i[0]):
                test_suite.append(i[0])
        
    #If functions in module
        for i in functions:
            if re.match("^(?!__init__).*", i[0]):
                function_list.append("test_"+i[0])

        self.assertItemsEqual(function_list, test_suite)

    def test_get_site(self):
        """This test is found in net_tests as it requires internet connectivity."""
        pass

    def test_save_list_file(self):
        """This test is found in net_tests as it requires internet connectivity."""
        pass

    def test_check_url_exist(self):
        """This test is found in net_tests as it requires internet connectivity."""
        pass

    
    def test_check_plain_text(self):
        is_plain = email_io.check_plain_text("data/test_case/testEmail")
        self.assertEqual("plain_text", is_plain)


    def test_check_json(self):
        is_json = email_io.check_json("data/util/testEmail.json")
        is_JSON = email_io.check_json("data/util/testEmail.JSON")
        self.assertTrue(is_json)
        self.assertTrue(is_JSON)

    def test_check_plain_text(self):
        plain_text = email_io.check_plain_text("data/test_case/testEmail")
        self.assertEqual("plain_text", plain_text)

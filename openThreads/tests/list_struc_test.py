import unittest
import sys
import inspect
import re

from openThreads import list_struc

class testFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_all_tests(self):
        functions = inspect.getmembers(list_struc.list, inspect.ismethod)
        tests = inspect.getmembers(testFunctions, inspect.ismethod)
        test_suite = []
        for i in tests:
            if re.match("^test_(?!all_tests).*", i[0]):
                test_suite.append(i[0])
        function_list = []
        for i in functions:
            if re.match("^(?!__init__).*", i[0]):
                function_list.append("test_"+i[0])
        self.assertItemsEqual(function_list, test_suite)

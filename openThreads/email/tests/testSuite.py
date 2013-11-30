#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
import os
import sys

#import top level of openThreads to run tests from
sys.path.append(os.path.abspath('../../..'))

import openThreads

#import tests from suites
from openThreads.email.tests import email_io_tests
from openThreads.email.tests import list_struc_test
from openThreads.email.tests import util_tests
from openThreads.email.tests import net_tests


def build_suite(suite_type, net_test):
    suite = unittest.TestSuite()
    suite_types = {"all": [email_io_tests.testFunctions, util_tests.testFunctions, list_struc_test.testFunctions], "email_io":[email_io_tests.testFunctions]}
    for test_case in suite_types[suite_type]:
        suite.addTest (unittest.makeSuite(test_case))
    print(net_test)
    if net_test == "True":
        suite.addTest (unittest.makeSuite(net_tests.testFunctions))
    return suite

def create_runner(suite_type, net_test, verbosity_level=None, runner_type="text"):
    """creates a testing runner.

    suite_type: (string) suites to run [acceptable values = suite_types in build_suite()]
    runner_type: (string) type of runner to create. [implemented values = 'text']
    """
    if runner_type == "text":
        runner = unittest.TextTestRunner(verbosity=verbosity_level)
        
    test_suite = build_suite(suite_type, net_test)
    runner.run (test_suite)

if __name__ == '__main__':
    """Creates argument parser for required arguments and calls test runner"""
    import argparse
    parser = argparse.ArgumentParser(description='openThreads test suite')
    parser.add_argument("-s", "--suite", nargs="?", default="all", const="all", dest="suite_type", metavar="SUITE", help="Pick a specific test suite")
    parser.add_argument("-n", "--net", nargs="?", default="False", const="False", dest="net_test", metavar="NET", help="Allow networking connections")
    parser.add_argument("-v", "--verbosity", nargs="?", default=None, const=2, dest="verbosity_level", metavar="VERBOSITY", help="make test_suite verbose")
    
    args = parser.parse_args()
    create_runner(args.suite_type, args.net_test, args.verbosity_level)

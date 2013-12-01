import time
import logging
import sys
import os

if __name__ == '__main__':
    """Creates argument parser for required arguments and calls test runner"""
    import argparse
    parser = argparse.ArgumentParser(description='openThreads test suite')
    parser.add_argument("-s", "--suite", nargs="?", default="all", const="all", dest="suite_type", metavar="SUITE", help="Pick a specific test suite")
    parser.add_argument("-v", "--verbosity", nargs="?", default=None, const=2, dest="verbosity_level", metavar="VERBOSITY", help="make test_suite verbose")
    parser.add_argument("-l", "--logfile", nargs="?", default="text", const="commotion_test.log", dest="logfile", metavar="LOGFILE", help="Specify an alternative logfile name")

    args = parser.parse_args()
    create_runner(args.suite_type, args.verbosity_level, args.logfile)


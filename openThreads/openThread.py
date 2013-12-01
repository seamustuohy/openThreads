"""
OpenThreads starter function for the command line
"""
import argparse
from openThreads.utils import logger
from openThreads.utils import fs_utils
import yaml
import os

def main(config=None, verbosity=None, logfile=None):
    """
    Sets up logging and starts parsing
    :param config: relative path to config file
    :type config: string
    :param verbosity: verbosity level for openthreads
    :type verbosity: int or string
    :param logfile: relative path to log file
    :type logfile: string
    """
    logger.set(verbosity)
    if logfile:
        logger.file(logfile)
    config = check_config(config)
    if config:
        start(config)
    else:
        raise NameError("""No configuration file found. Please specifiy a config file to use.""")

def check_config(config):
    """
    Ensures that the config file exists.
    :param config: relative path to config file
    :type config: string
    """
    if config == None:
        config = check_prjects()
    if fs_utils.is_file(config):
        return config
    else:
        return False


def check_projects():
    """
    Checks for, and prompts user to choose, a project config file in the default directory.
    :return: False if no config is  config
    :return: Config name if chosen
    """
    config_files = os.listdir("../projects")
    print("No config file chosen. Please choose a config file from your projects or exit.")
    print("[0] exit")
    for cfile, idx in enumerate(config_files):
        print("["+(idx+1)+"]"+" "+cfile)
    u_input = raw_input("Enter Number Here: ")
    if type(u_input) == int:
        if u_input == 0:
            return False
        else:
            config = config_files[u_input-1]
    else:
        config = check_projects()

def run_tests():
    """
    Runs default test suite
    """    
    from openThreads.tests import testSuite
    testSuite.main()

def get_args():
    """Creates argument parser for required arguments and calls test runner"""
    parser = argparse.ArgumentParser(description='openThreads')
    parser.add_argument("-c", "--config", nargs="?", default=None, const=None, dest="config_file", metavar="CONFIG", help="Choose a config file")
    parser.add_argument("-v", "--verbosity", nargs="?", default=None, const=1, dest="verbosity_level", metavar="VERBOSITY", help="Set verbosity level [1-100] or [debug, info, warn, error, critical]")
    parser.add_argument("-l", "--logfile", nargs="?", default="text", const="openthreads.log", dest="logfile", metavar="LOGFILE", help="Specify an alternative logfile name")
    parser.add_argument("-t", "--test", nargs="?", default=None, const=True, dest="test_run", metavar="TEST", help="Run openthreads test suite. NOTE: This will override all other flags and simply run and output tests.")
    args = parser.parse_args()
    if args.test_run:
        run_tests()
    else:
        main(args.config_file, args.verbosity_level, args.logfile)


if __name__ == "__main__":
    get_args()

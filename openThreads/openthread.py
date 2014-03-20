#!/usr/bin/env python
#
#    Copyright (C) 2013 Seamus Tuohy
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
OpenThreads starter function for the command line
"""
import argparse
import os
import yaml

from openThreads.utils import logger
from openThreads.utils import fs_utils
from openThreads import project_builder

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
    if logfile:
        logfile = fs_utils.get_file_abs(logfile)
    logger.set_logging(verbosity, logfile)
    config = check_config(config)
    if config:
        config_dict = get_conf(config)
        if config_dict:
            project = project_builder.Project(config_dict)
            project.start()
            #TODO run project here
        else:
            raise SyntaxError("""Config file is malformed... a monster really. I don't see how it sleeps at night. Freak. Please ensure proper YAML formatting in configs.""")
    else:
        raise NameError("""No configuration file found. Please specifiy a config file to use.""")

def get_conf(config):
    """
    Load YAML formatted config file
    :param config: Config file location
    :type config: string
    :return: config file
    :return type: dictionary
    """
    conf_file = open(config)
    data_map = yaml.safe_load(conf_file)
    conf_file.close()
    return data_map
    
def check_config(config):
    """
    Ensures that the config file exists.
    :param config: relative path to config file
    :type config: string
    """
    if config == None:
        config = check_projects()
    if fs_utils.is_file(config):
        return config
    else:
        return False


def check_projects():
    """
    Checks for, and prompts user to choose, a project config file in the default directory.
    :return: False if no config
    :return: Config name if chosen
    """
    config = None
    config_files = []
    for root, dirs, files in fs_utils.walklevel("../projects"):
        for file_name in files:
            if file_name.endswith(".conf"):
                config_files.append(os.path.join(root, file_name))
    print("No config file chosen. Please choose a config file from your projects or exit.")
    print("[0] exit")
    for cfile, idx in enumerate(config_files):
        print("["+(idx+1)+"]"+" "+cfile)
    u_input = raw_input("Enter Number Here: ")
    choice = is_int(u_input)
    if choice:
        if choice == 0:
            return False
        else:
            config =  config_files[choice-1]
    else:
        config = check_projects()
    return config

def is_int(num):
    """
    Checks if string can be int
    :return: int or False if not int-able
    """
    try:
        mod = int(num)
        return mod
    except ValueError:
        return False

def run_tests():
    """
    Runs default test suite
    """    
    from openThreads.tests import testSuite
    testSuite.main()

def get_args():
    """
    Argument parser for Command line use
    """
    parser = argparse.ArgumentParser(description='openThreads')
    parser.add_argument("-c", "--config", nargs="?", default=None, const=None, dest="config_file", metavar="CONFIG", help="Choose a config file")
    parser.add_argument("-v", "--verbosity", nargs="?", default=None, const=1, dest="verbosity_level", metavar="VERBOSITY", help="Set verbosity level [1-5]")
    parser.add_argument("-l", "--logfile", nargs="?", default="text", const="openthreads.log", dest="logfile", metavar="LOGFILE", help="Specify an alternative logfile location")

    parser.add_argument("-t", "--test", nargs="?", default=None, const=True, dest="test_run", metavar="TEST", help="Run openthreads test suite. NOTE: This will override all other flags and simply run and output tests.")
    args = parser.parse_args()
    if args.test_run:
        run_tests()
    else:
        main(args.config_file, args.verbosity_level, args.logfile)


if __name__ == "__main__":
    get_args()

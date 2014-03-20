import os
import gzip
import json

import openThreads

from openThreads import logger

def create_if_necessary(directory):
    """Create the specified directory, if necessary. Stolen from https://github.com/isislovecruft/python-gnupg/blob/master/gnupg/_util.py
    
    :param str directory: The directory to use.
    :rtype: bool
    :returns: True if no errors occurred and the directory was created or
    existed beforehand, False otherwise.
    """
    if not os.path.isabs(directory):
        logger.debug("Got non-absolute path: %s" % directory)
        directory = os.path.abspath(directory)
                
    if not os.path.isdir(directory):
        logger.info("Creating directory: %s" % directory)
        try:
            os.makedirs(directory, 0x1C0)
        except OSError as ose:
            logger.error(ose, exc_info=1)
            return False
        else:
            logger.debug("Created directory.")
    return True

def read_gzip(filename):
    """opens a gzip file and returns the plain text.

    """
    input_file = gzip.open(filename, 'rb')
    try:
           plain_text  = input_file.read()
    finally:
            input_file.close()
    return plain_text

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def is_file(unknown):
    """Determines if a file is accessable. It does NOT check to see if the file contains any data. """
#stolen from https://github.com/isislovecruft/python-gnupg/blob/master/gnupg/_util.py
    try:
        assert os.lstat(unknown).st_size > 0, "not a file: %s" % unknown
    except (AssertionError, TypeError, IOError, OSError) as err:
#end stolen <3
        logger.debug("is_file():"+err.strerror)
        return False
    if os.access(unknown, os.R_OK):
        return True
    else:
        logger.warn("is_file():You do not have permission to access that file")
        return False

def get_file_abs(obj):
    if is_file(obj):
        return os.path.abspath(obj)
    else:
        return False
    
def open_listserv(filename):
    pass
    #TODO Atually write this.
    #TODO This will require that list_struc.py is finished and a data structure is chosen.
    #TODO will be able to identify the file and use another function to open any csv or json formatted versions and save them as a compiled version.

def get_json(fileName):
    """ This function uploads a list-serv in json format. This is not implemented yet... soo WTF are you doing?"""
    logger.warn("JSON data format is not yet supported")
    f = open(fileName, 'r');
    tmpMsg = f.read()
    try:
        data = json.loads(tmpMsg)
        logger.debug("file is JSON")
        return data
    except ValueError:
        logger.debug("file is not json")
        return False

def save_json(fileName, data):
        f = open(fileName + '.json', 'w');
        f.write(json.dumps(data));
        f.close()

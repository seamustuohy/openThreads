import os
import gzip

from . import logger

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
    input_file = gzip.open(filename, 'rb')
    try:
           plain_text  = input_file.read()
    finally:
            input_file.close()
    return plain_text
    

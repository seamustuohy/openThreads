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
Main logging controls for openthreads
"""

import logging
from . import fs_utils

def set_logging(verbosity=None, logfile=None):
    """
    Creates a logger object 
    """
    logger = logging.getLogger('openThreads')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if fs_utils.is_file(logfile):
        fh = logging.FileHandler(logfile)
    else:
        fh = logging.FileHandler("/var/logs/openthreads.log")
        fh.setFormatter(formatter)
        fh.setLevel(logging.WARN)
    stream = logging.StreamHandler()
    stream.setLevel(logging.ERROR)
    stream.setFormatter(formatter)
    #set alternate verbosity
    if 1 <= verbosity <= 5:
        levels = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
        stream.setLevel(levels[(verbosity-1)])
        fh.setLevel(levels[(verbosity-1)])
    else:
        raise TypeError("""The Logging level you have defined is not supported please enter a number between 1 and 4""")
    #Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(stream)


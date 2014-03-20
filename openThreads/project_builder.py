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
The openThreads project class creator. This is where all project logic is contained regarding loading and cleaning up after parsers.
"""
import logging
import os

from openThreads.utils import fs_utils

class Project():
    
    def __init__(self, config):
        self.name = config.name
        self.plugins = {}
        logger = logging.getLogger('openThreads.'+ self.name)
        for plugin in config.plugins:
            directory = os.path.abspath("plugin/"+plugin.name)
            #TODO eventually check if properly formatted parser obj... eventually
            if fs_utils.is_file(directory+plugin.name+"_plugin.py"):
                logger.debug(plugin.name+" plugin supported.")
                imported_plug = load_plugin(plugin.name)
                self.plugins[plugin.name] = imported_plug.build(plugin)
            else:
                logger.error(plugin.name+" plugin requested in "+self.name+" config and NOT found. Are you sure it is spelled correctly in the config file?")
                raise SyntaxError(plugin.name+" plugin requested in "+self.name+" config and NOT found. Are you sure it is spelled correctly in the config file?")

    def start(self):
        pass

def load_plugin(name):
    """
    Takes a plugin name and returns an importer for that plugin.
    """
    mod = __import__("openThreads.{0}.{0}_plugin".format(name))
    return mod

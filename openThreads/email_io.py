import archive_reader
import re
import os
import httplib
import urllib2
import inspect
import json

from . import logger
from . import util

def main(listserv_file):
    listserv = False
    listserv_types = {
        'plain_text': archive_reader.parse_archive,
        'json':util.get_json,
        'site':get_site,
        }
    curr_type = check_type(listserv_file)
    if curr_type in listserv_types:
        listserv = listserv_types[curr_type](listserv_file)
    if listserv:
        return listserv

def get_site(site):
    """Connects to site and grabs list-serv files and passes them back"""
    logger.info("Reading site "+site)
    html = urllib2.urlopen(site).read()
    files = re.findall("\<td\>\<A href=\"(.*?\.(txt)?(\.gz)?)", html)
    if files:
        directory = save_list_file(site, files)
        raw = get_all_raw(directory)
    if raw:
        return raw
    else:
        return False

def get_all_raw(path):
    ls = os.listdir(path)
    text = []
    for i in ls:
        logger.info("Reading"+i)
        if_filetype = re.findall(".*(txt$)|(gz$)", i)
        if len(if_filetype) != 0:
            filetype = if_filetype[0]
            if filetype[-1] == 'gz':
                logger.info("file is a gzip file")
                pt = util.read_gzip(path+i)
            elif filetype[0] == 'txt':
                logger.info("file is a plainText file")
                if check_plain_text(path+i):
                    raw = open(path+i)
                    pt = raw.read()
            text.append(pt)
        else:
            logger.error("File is corrupted, in an unfamiliar format, or an archive.")
    full_text = '\n'.join(text)
    f = open(path+"archiveFile", "w")
    f.write(full_text)
    f.close()
    parsed = archive_reader.parse_archive(path+"archiveFile")
    return parsed

def save_list_file(site, files):
    directories = re.findall("^https?\://(.*)", site)
    cmd_folder = os.path.realpath(os.path.split(os.path.split(inspect.getfile( inspect.currentframe() ))[0])[0])
    directory = str(cmd_folder+"/listserv/"+directories[0])
    util.create_if_necessary(directory)
    for i in files:
        logger.info("processing"+i[0])
        f = open(directory+i[0], "w")
        dl = str(site)+str(i[0])
        page = urllib2.urlopen(dl).read()
        f.write(page)
        f.close()
    return directory

def check_type(unknown):
    """Checks if the string passed to the function matches a folder, then a local file, and finally, a website address."""
    file_types = {
        'json':check_json,
        }
    if util.is_file(unknown):
        for i in file_types:
            if file_types[i](unknown):
                return i
        logger.debug("file is plain text")
        if check_plain_text(unknown):
            return 'plain_text'
        else:
            logger.error("File is malformatted or not a list-serv")
            return False
    else:
        #TODO create a site and a path from sites that have paths
        #TODO Check for http://x.x.x and http://x.x and any variation
        if re.search("^.*\..*\..*", unknown):
        #Clear all http/https that a user might add
            if re.findall("^https?\:\/\/(.*)", unknown):
                unknown = re.findall("^https?\:\/\/(.*)", unknown)[0]
                print(unknown)
            if check_url_exist(unknown):
                logger.debug("listserv object is website")
                return "site"
        else:
            logger.error("file does not match any known file types")
            return False

def check_plain_text(somefile):
    f = open(somefile, 'r');
    who = '\S*\sat\s\S*'
    headerFront = '^From\s' + who + '\s*'
    for line in f:
        if re.search(headerFront, line):
            return "plain_text"
        else:
            return False
        
def check_url_exist(site):
    """site given must be without the protocol header (http://)"""
    logger.debug("checking url")
    components = re.findall("(.*?)(\/.*)", site)[0]
    print(components)
    conn = httplib.HTTPConnection(components[0])
    conn.request('HEAD', components[1])
    response = conn.getresponse()
    print(response.status)
    conn.close()
    #TODO find out why so many of these pages return a 302 response?
    return response.status == 200 or response.status == 302

def check_json(somefile):
    """This only checks that the extension is json|JSON"""
    if re.match(".*[(?=\.json$)|(?=\.JSON$)]", somefile):
        return True
    else:
        return False


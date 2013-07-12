import archive_reader
import json
import re
import os
import httplib
import csv

from . import logger

def main(listserv_file):
    listserv = False
    listserv_types = {
        'plain_text': archive_reader.parse_archive,
        'json':get_json,
        'CSV':get_csv,
        'site':get_site,
        }
    curr_type = check_type(listserv_file)
    if curr_type in listserv_types:
        listserv = listserv_types[curr_type](listserv_file)
    if listserv:
        return listserv

def get_json(fileName):
    f = open(fileName, 'r');
    tmpMsg = f.read()
    return json.loads(tmpMsg)

def get_csv(somefile):
    """This should accept csv formatted data...I can't yet put a listserv into csv format, so it is kind of useless until that happens. """
    #TODO once save as CSV is completed re work this function to correctly parse the data.
    logger.warn("CSV data format is not yet supported... WTF are you uploading?")
    dev = []
    with open(somefile, 'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            dev.append(row)
    return dev

def get_site(site):
    """Connects to site and grabs list-serv files and passes them back"""
    #TODO All of this
    #1 See if messages on page
    #2 See if links to messages/.gz files
    #3 download site into a folder
    #4 if .gz then unzip files
    #5 concatinate files into full archive
    #6 use get_plain_text to grab the text and return it
    return site


def check_type(unknown):
    """Checks if the string passed to the function matches a folder, then a local file, and finally, a website address."""
    file_types = {
        'json':check_json,
        'CSV':check_csv,
        }
    if is_file(unknown):
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
            if re.findall("^https?\://(.*)", unknown):
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
    tmpMsg = f.read()
    #Here I just check for some simple header information. If the file is in a non csv or json format but does contain a listserv this will import it as if it is a plain-text dump... be warned!
    who = '\S*\sat\s\S*'
    headerFront = '\nFrom\s' + who + '\s*'
    if re.search(headerFront, tmpMsg):
        return "plain_text"
    else:
        return False
        
def check_url_exist(site):
    conn = httplib.HTTPConnection(site)
    #TODO DO we need to Check for malformed response like from my website?.. also fix your website seamus. Seriously!
    conn.request('HEAD', site)
    response = conn.getresponse()
    conn.close()
    return response.status == 200

def check_csv(somefile):
    csv_fileh = open(somefile, 'rb')
    try:
        dialect = csv.Sniffer().sniff(csv_fileh.read(1024))
        csv_fileh.seek(0)
        logger.debug("check_csv(): file is a csv")
        return True
    except csv.Error:
        logger.debug("check_csv(): file is not a csv")
        return False

def check_json(somefile):
    #TODO actually implement this.
    try:
        json.loads(somefile)
    except ValueError:
        logger.debug("file is not json")
        return False
    logger.debug("file is JSON")
    return True

def is_file(unknown):
    """Determines if a file is accessable, and contains actual data. It does NOT check to see if the file contains any data. """
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


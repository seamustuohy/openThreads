import archive_reader
import json
import re
import os
import httplib
import csv
import urllib2

from . import logger
from . import util

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
    #return dev

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
        filetype = re.findall(".*(txt$)|(gz$)", i)[0]
        print(filetype)
        if filetype[-1] == 'gz':
            logger.info("file is a gzip file")
            pt = util.read_gzip(path+i)
        elif filetype[0] == 'txt':
            logger.info("file is a plainText file")
            if check_plain_text(path+i):
                raw = open(path+i)
                pt = raw.read()
        else:
            logger.error("File is corrupted or in an unfamiliar format.")
        text.append(pt)
    full_text = '\n'.join(text)
    f = open(path+"archiveFile", "w")
    f.write(full_text)
    f.close()
    parsed = archive_reader.parse_archive(path+"archiveFile")
    return parsed

def save_list_file(site, files):
    directories = re.findall("^https?\://(.*)", site)
    directory = str("listserv/"+directories[0])
    util.create_if_necessary(directory)
    for i in files:
        logger.info("proicessing"+i[0])
        f = open(directory+i[0], "w")
        dl = str(site)+str(i[0])
        page = urllib2.urlopen(dl).read()
        print(page)
        f.write(page)
        f.close()
    return directory

def check_type(unknown):
    """Checks if the string passed to the function matches a folder, then a local file, and finally, a website address."""
    file_types = {
        'json':check_json,
        'CSV':check_csv,
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
    tmpMsg = f.read()
    #Here I just check for some simple header information. If the file is in a non csv or json format but does contain a listserv this will import it as if it is a plain-text dump... be warned!
    who = '\S*\sat\s\S*'
    headerFront = '\nFrom\s' + who + '\s*'
    if re.search(headerFront, tmpMsg):
        return "plain_text"
    else:
        return False
        
def check_url_exist(site):
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

def check_csv(somefile):
    #TODO try to actually import a csv of a mailing list
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
    #TODO actually try this with json saved email list.
    try:
        json.loads(somefile)
    except ValueError:
        logger.debug("file is not json")
        return False
    logger.debug("file is JSON")
    return True


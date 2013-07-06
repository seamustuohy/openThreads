import archive_reader
import json

def main(listserv_file):
    curr_type = check_type(listserv_file)
    if curr_type in listserv_types:
        listserv = listserv_types[curr_type](listserv_file)

listserv_types = {
    'plain_text' : archive_reader.parse_archive,
    'json' : get_json,
    'CSV' : get_csv,
    'site':get_site,
    }

def get_json(fileName):
    f = open(fileName, 'r');
    tmpMsg = f.read()
    return json.loads(tmpMsg)

def get_csv(filename):
    raise exception, "This functionality has not been implemented. Please convert the CSV file to JSON or import a plain text email list-serv dump"

def get_site(url):
    import gzip

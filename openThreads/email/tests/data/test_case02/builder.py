import os
import sys

cur = os.path.abspath(".")
print cur
sys.path.append("../../../../")


from openThreads import archive_reader
from openThreads import list_struc
from openThreads import util


def build_test_case_files():    
    """
    @param listserv plain text list-serv file to create otehr files from

    """
    email = archive_reader.parse_archive(cur+"/testEmail")
    
    basic_struc = open(cur+"/testEmail.py", "w")
    basic_struc.write("test = "+str(email))
    basic_struc.close()

    util.save_json(cur+"/testEmail", email)

    test_list = list_struc.list(listserv=email)
    index = open(cur+"/testEmailIndex.py", "w")
    index.write("index = "+str(test_list.index))
    index.close()


if __name__ == "__main__":
    build_test_case_files()

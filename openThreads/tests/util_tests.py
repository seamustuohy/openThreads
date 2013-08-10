import unittest
import sys
import os
import shutil

from openThreads import util
from openThreads import logger

class testFunctions(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = "data/util/testDir"
        if os.path.isdir(self.test_dir):
            try:
                os.rmdir(self.test_dir)
            except OSError as ose:
                logger.error(str(ose))
                try:
                    shutil.rmtree(self.test_dir)
                except OSError as ose:
                    log.error(str(ose))
        if os.path.isfile("data/util/DOOM"):
            os.remove("data/util/DOOM")

    def tearDown(self):
        """This tears down the tests"""
        dirs = [self.test_dir, self.test_dir + "/testCIN"]
        for i in dirs:
            if os.path.exists(i) and os.path.isdir(i):
                try:
                    shutil.rmtree(i)
                except OSError as ose:
                    log.error(ose + " I really hope you did not use a symbolic link...")

    def test_get_json(self):
        """Test that imported JSON  """
        sys.path.append("data/util")
        import testEmail
        #get the actual json dict from file
        json_msg_text = testEmail.test

        single_json = util.get_json("data/util/single_json.json")
        json_msg = util.get_json("data/util/testEmail.json")
        self.assertEqual(single_json, {'item': 'content'})
        self.assertEqual(json_msg, json_msg_text)

    def test_CIN(self):
        CINdir = self.test_dir + "/testCIN"
        dir_exist = os.path.isdir(CINdir)
        created = util.create_if_necessary(CINdir)
        self.assertNotEqual(dir_exist, created)
        dir_exist = os.path.isdir(CINdir)
        self.assertTrue(dir_exist)

    def test_gzip(self):
        gzip_file = "data/util/testFile.gz"
        file_text = "This is a test file.\nIt is zipped using gzip\n"
        read_text = util.read_gzip(gzip_file)
        self.assertEqual(file_text, read_text)

    def test_if_file(self):
        self.assertTrue(util.is_file("data/util/testFile.gz"))
        self.assertFalse(util.is_file("data/util/DOOM"))
        

    

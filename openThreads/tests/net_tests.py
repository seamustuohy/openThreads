import unittest
import shutil
import os
import inspect
import openThreads

from openThreads import email_io

class testFunctions(unittest.TestCase):

    def setUp(self):
        self.cmd_folder = os.path.realpath(os.path.split(os.path.split(inspect.getfile(openThreads))[0])[0])
        print(self.cmd_folder)

    def tearDown(self):
        """This tears down the tests"""
        if os.path.exists(self.cmd_folder+"/listserv/lists.chambana.net") and os.path.isdir(self.cmd_folder+"/listserv/lists.chambana.net"):
            try:
                shutil.rmtree(self.cmd_folder+"/listserv/lists.chambana.net")
            except OSError as ose:
                log.error(ose + " I really hope you did not use a symbolic link...")

    def test_save_list_file(self):
        https_site = "https://lists.chambana.net/pipermail/commotion-android/"
        http_site = "http://lists.chambana.net/pipermail/commotion-android/"
        files = [('2011-December.txt.gz', 'txt', '.gz')]

        directory = email_io.save_list_file(https_site, files)
        self.assertTrue(os.path.isfile(self.cmd_folder+"/listserv/lists.chambana.net/pipermail/commotion-android/2011-December.txt.gz"))
        shutil.rmtree(self.cmd_folder+"/listserv/lists.chambana.net")
        directory = email_io.save_list_file(http_site, files)
        self.assertTrue(os.path.isfile(self.cmd_folder+"/listserv/lists.chambana.net/pipermail/commotion-android/2011-December.txt.gz"))

    def test_get_site(self):
        print("THHIS NEEDS TONS OF OTHER FUNCTIONS CHECKED TO WORK")
        https_site = "https://lists.chambana.net/pipermail/commotion-android/"
        http_site ="http://lists.chambana.net/pipermail/commotion-android/"
        #Does not currently accept sites without http or https
        #site = "lists.chambana.net/pipermail/commotion-android/"
        data = email_io.get_site(https_site)
        self.assertIsNotNone(data)
        data = None
        data = email_io.get_site(http_site)
        self.assertIsNotNone(data)

        if os.path.exists(self.cmd_folder+"/listserv/lists.chambana.net") and os.path.isdir(self.cmd_folder+"/listserv/lists.chambana.net"):
            try:
                shutil.rmtree(self.cmd_folder+"/listserv/lists.chambana.net")
            except OSError as ose:
                log.error(ose + " I really hope you did not use a symbolic link...")


    def test_check_url_exist(self):
        site = "lists.chambana.net/pipermail/commotion-android/"
        exist = email_io.check_url_exist(site)
        self.assertTrue(exist)

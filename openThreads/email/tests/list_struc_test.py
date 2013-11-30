import unittest
import sys
import inspect
import re
from random import randrange


from openThreads.email import list_struc
from openThreads import logger

class testFunctions(unittest.TestCase):

    def setUp(self):
        self.unittest_name = testFunctions
        self.module = list_struc
        self.module_class = list_struc.list
        #create the test list_struc obj to test with
        sys.path.append("data/test_case")

        self.testEmail = None
        self.testEmailIndex = None
        list_serv = None
        self.test_list = None
        self.new_msg = None
        
        self.testEmail = __import__("testEmail")
        #get the actual list_serv from testEmail file
        list_serv = self.testEmail.test
        self.test_list = list_struc.list(listserv=list_serv)
        self.new_msg = {
            'Body': "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA384\n\nYou are all crazy\n\n>>>TOP POSTING IS FOR WINNERS!!!\n>>>\n>Is for losers\n>>>>I am a second messsage. I am From: testie McTesterson.\n>>>>\n>Who knows that inline posting is for winners.\n>>>>LOVE Testie\n>>\n>>Bottom Post FOO!!!\n>what a crazy idea.\n>\n>-Le' Testiei sux\n\nI can't beleive I found this thread nearly a year later!\n\n- -----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.11 (Darwin)\n\niQIaBAEBCQAGBQJQxu60AAoJELyJZYjffCjus3gP/jUw/74xihfI6F9VmHVGnvf0\noJEbdNZ/pLhLfwa2wHpVYhdJ1AXm+q/2vTYuL5QRshzvQ1pO1mH5Ua3s5ETuI3Xc\nSWmqmtwjSuq3xn7fWuiszw46cBv4rDa6slT1ImfWXkgHamhgIfB8ciXVSiqFu7Ct\nzDrvuF6dzM7C+BuZoAfTJX0rpDfDgmSA/lh3CuDb7T7QFV9aTO4FByCVsJ/hWwEG\n+tHsk42qLuew4ISz6eaogAYIJ86AZAkjKYz71AgU2vs87j2GKLRxX6iBdKHxwHo/\nnxXxVkpQTr/3OVUgHt3ICS+8x2GBgVFhZupXKiIvvbUG09DMgiqmETpryycVXSs4\nLAr0q2x8JwVlMh5acLXimYVRcSVZkSwI2PliLMFZpEguErnri0RRHhwfFlQ/pQKR\n/iHmTZ8it5fpxEkL6CrIR0raRk6Z8nY4ps2uDGkf1IlDYHWk7Tc068W3iP/GkDgB\nDYW9CakfsCJow38MD+1I1jsaMlm7k0quVPVveUaSvwMsg7RG7C+0L/meLwZBuXm8\n8fTjdZp4n57H+2++AweNIhxKPTSadRHtemQg2T+EPS6+u6OeEFNlC48hl5arMrtU\n7JfWSzy5J5z+VYeXBQpsiJZP/9w/KEbRF1xd/SPolqH7fC1O0fhajalS/yS3X9jd\n12z0RPuCBuWfSKNRnfcs\n=dIyX\n- -----END PGP SIGNATURE-----\n\n-------------- next part --------------\nAn HTML attachment was scrubbed...\nURL: <http://mailman.thisEmailList.edu/subdir/folder02/attachments/20090814/5Rsh6ec/attachment.html>",
            'day_number': '13',
            'Name': 'Jane Smith',
            'hour': '10',
            'seconds': '34',
            'day_name': 'Fri',
            'Address': 'janesmith@cs.nyu.edu',
            'year': '2009',
            'month_name': 'Aug',
            'zone': '-0700',
            'References': [
                '<01a101c8f07e$9ab703d0$d0250b70$@bcs@pineapple.edu>',
                '<a5ca47180807251726k34b5a5b5wda031814a3c36a4f@mail.gmail.com>',
                '<487BCB0B.8030005@cs.ucsc.edu>',
                '<fd43sdc8f07e$9af3f4fdsfw30$@bcs@pumpkin.edu>'
                ],
            'time': '10:10:34',
            'Reply_To': '<a5ca47180807251726k34b5a5b5wda031814a3c36a4f@mail.gmail.com>',
            'ID': '<K3dis83KLFE8DSFDlfd3$fdw@cs.nyu.edu>',
            'minute': '10',
            'Subject': '[email-list] Episode 2: A New Message'}
        
    def test_all_tests(self):
        function_list = []
        test_suite = []
        if self.module_class != False:
            class_functions = inspect.getmembers(self.module_class, inspect.ismethod)
        #If Class Exists in module
            for i in class_functions:
                if re.match("^(?!__init__).*", i[0]):
                    function_list.append("test_"+i[0])

        functions = inspect.getmembers(self.module, inspect.isfunction)
        tests = inspect.getmembers(self.unittest_name, inspect.ismethod)

    #check for tests
        for i in tests:
            if re.match("^test_(?!all_tests).*", i[0]):
                test_suite.append(i[0])
        
    #If functions in module
        for i in functions:
            if re.match("^(?!__init__).*", i[0]):
                function_list.append("test_"+i[0])

        self.assertItemsEqual(function_list, test_suite)


    def test_split_body(self):
        test_split_body = self.test_list.split_body(self.new_msg)
        #TODO pick a format for PGP keys and add a test for proper formatting.
        self.assertIsNotNone(test_split_body['PGP'])
        self.assertIsNotNone(test_split_body['content'])
        self.assertEqual(test_split_body['HTML'], True)

        
    def test_get_parsed_body(self):
        #TODO add better assertions about this test that pull from a list of users in a message.
        test_parse_body = self.test_list.get_parsed_body(self.new_msg)
        test_split_body = self.test_list.split_body(self.new_msg)
        #ensure no content lost
        self.assertEqual(len(test_parse_body['content']), len(test_split_body['content']))
        for i in test_parse_body:
            if i == 'content':
                for n in test_parse_body[i]:
                    #logger.debug(str(n))
                    self.assertGreater(n[2],0)
                    if n[0] == 'unknown':
                        self.assertEqual(n[1],'unknown')
                        self.assertEqual(n[4],"0.0")
                        self.assertEqual(n[2],len(n[3]))
                    if n[0] == 'user':
                        self.assertNotEqual(n[1],'unknown')
                        self.assertEqual(n[4],"1.0")
                        self.assertEqual(n[2],len(n[3]))
        
        #test old messages give similar data
        #logger.debug("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        list_serv = self.testEmail.test
        existing_msg = self.testEmail.test[randrange(len(list_serv))]
        test_old_body = self.test_list.get_parsed_body(existing_msg)
        for i in test_old_body:
            if i == 'content':
                for n in test_old_body[i]:
                    #logger.debug(str(n))
                    self.assertGreater(n[2],0)
                    if n[0] == 'unknown':
                        self.assertEqual(n[1],'unknown')
                        self.assertEqual(n[4],"0.0")
                        self.assertEqual(n[2],len(n[3]))
                    if n[0] == 'user':
                        self.assertNotEqual(n[1],'unknown')
                        self.assertEqual(n[4],"1.0")
                        self.assertEqual(n[2],len(n[3]))

    def test_get_quote_body(self):
        """Tested through test_get_parsed_body """
        pass

        
    def test_get_msg_data(self):
        """Test message addition """
        #TODO  convert all the index functions to actually use the data structures i have created instead of a set of nested dictionaries.
        list_serv = self.testEmail.test
        #get a random old message from the list
        existing_msg = self.testEmail.test[randrange(len(list_serv))]
        
        test_list_static = list_struc.list(listserv=list_serv)

        #ensure lists start equal
        self.assertItemsEqual(self.test_list.messages, test_list_static.messages)

        #Add the new message to the messages list
        self.test_list.get_msg_data(self.new_msg)
        
        #Message was added to list-serv
        self.assertIsNotNone(self.test_list.messages[self.new_msg['ID']])

        #message had its body content parsed
        #no message body content was not harmed in the making of this object.
        new_content = self.test_list.messages[self.new_msg['ID']].__dict__
        new_msg_items = ("Body", "day_number", "Name", "hour", "seconds", "year", "day_name",  "Reply_To", "month_name", "References", "time", "Address", "zone", "ID", "minute", "Subject")
        for item in new_content:
            if item in new_msg_items:
                self.assertEqual(self.new_msg[item], new_content[item])
            else:
                self.assertIn(item, ("content", "HTML", "PGP", "clean_body"))

        #test that adding existing adds parsed body contents to that old message
        self.test_list.get_msg_data(existing_msg)
        newer_content = self.test_list.messages[existing_msg['ID']].__dict__
        for item in new_content:
            if item in new_msg_items:
                #Cannot test reference and in-reply-to for first posts.
                if item != "Reply_To" or "References":
                    self.assertEqual(existing_msg[item], newer_content[item])
            else:
                self.assertIn(item, ("content", "HTML", "PGP", "clean_body"))

    
    def test_get_response_length(self):
        test_parse_body = self.test_list.get_parsed_body(self.new_msg)



    #TODO Change "In-Reply-To" in all files to another string without hyphens possibly "In_Reply_To"

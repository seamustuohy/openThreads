import unittest

from openThreads import list_struc

class testFunctions(unittest.TestCase):

    def setUp(self):
        self.list_file = "data/testEmail"


    def test_get_json(self):
        single_json = email_io.get_json("data/single_json.json")
        print(single_json)
        self.assertEqual(1,1)

import unittest
import openthreads


class testFunctions(unittest.TestCase):

    def setUp(self):
        self.listSrv = openthreads.openThread("tests/testEmail")

    def test_init(self):
        #Test that messages and first messages are created upon class instatiation.
        self.assertNotEqual(self.listSrv.messages, [])
        self.assertIsNotNone(self.listSrv.messages)
        self.assertIsNotNone(self.listSrv.First)

    def test_compactDate(self):
        #test that computed date is being correctly computed
        dateResult = self.listSrv.compactDate("Sun, 13 Jul 2008 22:11:01 -0700")
        testDate = '2008713221101'
        self.assertEqual(dateResult, testDate) 

    def test_getRaw(self):
        raw = self.listSrv.getArchive('tests/rawSmall')
        self.assertEqual(raw, 'abcdefg')

    def test_split(self):
        """Test that the split function splits a list-serv into seperate e-mails"""
        raw = self.listSrv.getArchive('tests/testEmail')
        split = self.listSrv.split(raw)
        self.assertEqual(len(split), 5)

    def test_dictifying(self):
        test = {
         'Body': '\n\n\nI am a second messsage. I am From: testie McTesterson.\n\nLOVE Testie\n',
         'From': 'testie at cs.testuni.edu (Testie McTesterson)',
         'Name': 'Testie McTesterson',
         'compactDate': '2008713221101',
         'References': [],
         'Date': ' Sun, 13 Jul 2008 22:11:01 -0700',
         'Reply': [],
         'ID': ' <a5ca47180807251726k34b5a5b5wda031814a3c36a4f@mail.gmail.com>',
         'Subject': '[email-list] The Second Message'}
        self.assertEqual(test, self.listSrv.messages[1])

    def test_couchDB(self):
        print("TODO Create a CouchDB test")




if __name__ == '__main__':
    unittest.main()

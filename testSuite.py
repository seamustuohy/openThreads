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

    

if __name__ == '__main__':
    unittest.main()

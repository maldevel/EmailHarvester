import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import EmailHarvester

class TestMyParser(unittest.TestCase):
    def setUp(self):
        self.testParser = EmailHarvester.myparser()

    def test_extract(self):
        self.testParser.extract("some results", "example.com")
        self.assertEqual("some results", self.testParser.results)
        self.assertEqual("example.com", self.testParser.word)


    def test_genericClean(self):
        self.testParser.extract("<KW>test</KW>%2f<em>email</em>", "example.com")
        self.testParser.genericClean()
        expected_result = "test email"
        self.assertEqual(expected_result, self.testParser.results)

    def test_emails(self):
        self.testParser.extract("Contact us at info@example.com and support@example.com", "example.com")
        emails = self.testParser.emails()
        expected_emails = ["info@example.com", "support@example.com"]
        self.assertEqual(set(expected_emails), set(emails))

    def test_unique(self):
        self.testParser.temp = ["duplicate@example.com", "unique@example.com", "duplicate@example.com"]
        unique_emails = self.testParser.unique()
        expected_unique_emails = ["duplicate@example.com", "unique@example.com"]
        self.assertEqual(set(expected_unique_emails), set(unique_emails))


if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from plugins.googleplus import Plugin, search

class TestGooglePlusPlugin(unittest.TestCase):
    def setUp(self):
        self.app_mock = MagicMock()
        self.config = {'useragent':'test-agent', 'proxy': None}
        self.plugin = Plugin(self.app_mock, self.config)

    def test_plugin_init(self):
        self.app_mock.register_plugin.assert_called_once_with('googleplus', {'search': search})

    @patch('plugins.googleplus.app_emailharvester')
    def test_search(self, mock_app_emailharvester):
        mock_app_emailharvester.init_search = MagicMock()
        mock_app_emailharvester.process = MagicMock()
        mock_app_emailharvester.get_emails = MagicMock(return_value = ['john_doe@email.com'])

        domain = "email.com"
        limit = 10
        result = search(domain,limit)

        expected_url = 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Aplus.google.com+intext:"Works at"+-inurl:photos+-inurl:about+-inurl:posts+-inurl:plusones+%40{word}'

        mock_app_emailharvester.init_search(expected_url, domain, limit, 0, 100, 'Google+')
        mock_app_emailharvester.process.assert_called_once()
        mock_app_emailharvester.get_emails.assert_called_once()

        self.assertEqual(['john_doe@email.com'], result)

if __name__ == '__main__':
    unittest.main()
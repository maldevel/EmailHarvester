import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from plugins.ask import Plugin, search, AskSearch

class TestAskPlugin(unittest.TestCase):
    def setUp(self):
        self.app_mock = MagicMock()
        self.config = {'useragent':'test-agent', 'proxy': None}
        self.plugin = Plugin(self.app_mock, self.config)

    def test_plugin_init(self):
        self.app_mock.register_plugin.assert_called_once_with('ask', {'search': search})

    @patch('plugins.ask.config', new_callable=dict)
    @patch('plugins.ask.requests.get')
    @patch('plugins.ask.app_emailharvester')
    def test_search(self, mock_app_emailharvester, mock_requests_get, mock_config):
        # Setup mock configuration
        mock_config['proxy'] = None
        mock_config['useragent'] = 'test-agent'

        # Mock parser methods
        mock_app_emailharvester.parser = MagicMock()
        mock_app_emailharvester.parser.extract = MagicMock()
        mock_app_emailharvester.parser.emails = MagicMock(return_value=['john_doe@email.com'])
        
        # Mock the HTTP response from requests.get
        mock_response = MagicMock()
        mock_response.content.decode.return_value = "response content"
        mock_response.encoding = 'utf-8'
        mock_requests_get.return_value = mock_response

        domain = "email.com"
        limit = 10

        # Execute the search function
        result = search(domain, limit)

        #---

        expected_url_template = 'http://www.ask.com/web?q=%40{word}&page={page}'

        # Extract called URLs from requests.get
        urls_called = [call[0][0] for call in mock_requests_get.call_args_list]

        # Generate expected URLs
        expected_urls = [expected_url_template.format(word=domain, page=i+1) for i in range(limit // 10)]

        # Verify that each expected URL was called
        for expected_url in expected_urls:
            self.assertIn(expected_url, urls_called, f"{expected_url} was not called")

        #---

        # Verify that the parser methods were called correctly
        mock_app_emailharvester.parser.extract.assert_called_once_with("response content", domain)
        mock_app_emailharvester.parser.emails.assert_called_once()

        # Check the result of the search function
        self.assertEqual(['john_doe@email.com'], result)

if __name__ == '__main__':
    unittest.main()
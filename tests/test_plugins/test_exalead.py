import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from plugins.exalead import Plugin, search


class TestExaleadPlugin(unittest.TestCase):
    def setUp(self):
        self.app_mock = MagicMock()
        self.config = {'useragent':'test-agent', 'proxy': None}
        self.plugin = Plugin(self.app_mock, self.config)
    
    def test_plugin_init(self):
        self.app_mock.register_plugin.assert_called_once_with('exalead', {'search': search})

    @patch('plugins.exalead.app_emailharvester')
    def test_search(self, mock_app_emailharvester):
        mock_app_emailharvester.init_search = MagicMock()
        mock_app_emailharvester.process = MagicMock()
        mock_app_emailharvester.get_emails = MagicMock(return_value = ['john_doe@email.com'])

        domain = "email.com"
        limit = 10
        result = search(domain,limit)

        expected_url = 'http://www.exalead.com/search/web/results/?q=%40{word}&elements_per_page=10&start_index={counter}'

        mock_app_emailharvester.init_search(expected_url, domain, limit, 0, 50, 'Exalead')
        mock_app_emailharvester.process.assert_called_once()
        mock_app_emailharvester.get_emails.assert_called_once()

        self.assertEqual(['john_doe@email.com'], result)





if __name__ == '__main__':
    unittest.main()
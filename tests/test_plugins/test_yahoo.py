import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from plugins.yahoo import Plugin, search

class TestYahooPlugin(unittest.TestCase):
    def setUp(self):
        self.app_mock = MagicMock()
        self.config = {'useragent':'test-agent', 'proxy': None}
        self.plugin = Plugin(self.app_mock, self.config)

    def test_plugin_init(self):
        self.app_mock.register_plugin.assert_called_once_with('yahoo', {'search': search})

    @patch('plugins.yahoo.app_emailharvester')
    def test_search(self, mock_app_emailharvester):
        mock_app_emailharvester.init_search = MagicMock()
        mock_app_emailharvester.process = MagicMock()
        mock_app_emailharvester.get_emails = MagicMock(return_value = ['john_doe@email.com'])

        domain = "email.com"
        limit = 10
        result = search(domain,limit)

        expected_url = "http://search.yahoo.com/search?p=%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={counter}"
        
        mock_app_emailharvester.init_search(expected_url, domain, limit, 1, 100, 'Yahoo')
        mock_app_emailharvester.process.assert_called_once()
        mock_app_emailharvester.get_emails.assert_called_once()

        self.assertEqual(['john_doe@email.com'], result)

        

if __name__ == '__main__':
    unittest.main()
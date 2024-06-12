import unittest
from unittest.mock import MagicMock, patch, Mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import EmailHarvester

class TestEmailHarvester(unittest.TestCase):
    def setUp(self):
        self.userAgent = 'test-agent'
        self.proxy = None
        self.emailHarvester = EmailHarvester.EmailHarvester(self.userAgent, self.proxy)

    def test_register_plugin(self):
        mock_function = MagicMock()

        self.emailHarvester.register_plugin('test_method', {'function': mock_function})

        self.assertIn('test_method', self.emailHarvester.plugins)
        self.assertEqual({'function': mock_function}, self.emailHarvester.plugins['test_method'])

    def test_get_plugins(self):
        mock_function1 = MagicMock()
        self.emailHarvester.register_plugin('test_method1', {'function1': mock_function1})

        mock_function2 = MagicMock()
        self.emailHarvester.register_plugin('test_method2', {'function2': mock_function2})

        self.assertEqual(self.emailHarvester.get_plugins(), self.emailHarvester.plugins)

    @patch('builtins.print')
    def test_show_message(self, mock_print):
        test_message = "Test message"
        self.emailHarvester.show_message(test_message)
        mock_print.assert_called_once_with(test_message)

    def test_init_search(self):
        url = 'http://example.com/search?q={word}&start={counter}' 
        word = 'test' 
        limit = 100
        counterInit = 0
        counterStep = 10 
        engineName = 'Test-Engine'

        self.emailHarvester.init_search(url, word, limit, counterInit, counterStep, engineName)

        self.assertEqual(url, self.emailHarvester.url)
        self.assertEqual(word, self.emailHarvester.word)
        self.assertEqual(limit, self.emailHarvester.limit)
        self.assertEqual(counterInit, self.emailHarvester.counter)
        self.assertEqual(counterStep, self.emailHarvester.step)
        self.assertEqual(engineName, self.emailHarvester.activeEngine)
        self.assertEqual("",self.emailHarvester.results)
        self.assertEqual("", self.emailHarvester.totalresults)

    @patch('requests.get')
    def test_do_search(self, mock_get):
        url = "http://example.com/search?q={word}&start={counter}"
        word = "test"
        response_content = "Search results content"
        mock_response = Mock()
        mock_response.content = response_content.encode('utf-8')
        mock_response.encoding = 'utf-8'
        mock_get.return_value = mock_response

        self.emailHarvester.init_search(url, word, 1, 0, 1, "ExampleEngine")
        self.emailHarvester.do_search()

        expected_url = url.format(counter = '0', word = word)
        mock_get.assert_called_once_with(expected_url, headers={'User-Agent': self.userAgent})
        self.assertEqual(response_content, self.emailHarvester.results)
        self.assertEqual(response_content, self.emailHarvester.totalresults)

    @patch('time.sleep', return_value = None)
    @patch('requests.get')
    @patch('builtins.print')    
    def test_process(self, mock_print, mock_get, mock_sleep):
        url = "http://example.com/search?q={word}&start={counter}"
        word = "test"
        response_content = "Search results content"
        mock_response = Mock()
        mock_response.content = response_content.encode('utf-8')
        mock_response.encoding = 'utf-8'
        mock_get.return_value = mock_response

        self.emailHarvester.init_search(url, word, 20, 0, 10, "ExampleEngine")
        self.emailHarvester.process()

        self.assertEqual(2, mock_get.call_count)
        self.assertEqual(20, self.emailHarvester.counter)
        self.assertEqual(response_content * 2, self.emailHarvester.totalresults)

    def test_get_emails(self):
        self.emailHarvester.totalresults = "Contact us at info@example.com and support@example.com"
        self.emailHarvester.word = "example.com"
        emails = self.emailHarvester.get_emails()
        expected_emails = ["info@example.com", "support@example.com"]
        self.assertEqual(set(expected_emails), set(emails))

if __name__ == '__main__':
    unittest.main()
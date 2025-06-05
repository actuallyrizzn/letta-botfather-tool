import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import requests
from botfather import provision_botfather_message, main

class TestBotFatherTool(unittest.TestCase):
    @patch('requests.post')
    def test_provision_botfather_message_success(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'messages': [
                'BotFather reply 1',
                'BotFather reply 2',
                'BotFather reply 3'
            ]
        }
        mock_post.return_value = mock_response

        # Test the function
        result = provision_botfather_message('/newbot')

        # Verify the result
        self.assertEqual(result, [
            'BotFather reply 1',
            'BotFather reply 2',
            'BotFather reply 3'
        ])

        # Verify the request was made correctly
        mock_post.assert_called_once_with(
            'http://localhost:57431/send_message',
            json={'message': '/newbot'}
        )

    @patch('requests.post')
    def test_provision_botfather_message_invalid_response(self, mock_post):
        # Mock response with invalid format
        mock_response = MagicMock()
        mock_response.json.return_value = {'invalid': 'response'}
        mock_post.return_value = mock_response

        # Test the function
        with self.assertRaises(ValueError):
            provision_botfather_message('/newbot')

    @patch('requests.post')
    def test_provision_botfather_message_connection_error(self, mock_post):
        # Mock connection error
        mock_post.side_effect = requests.RequestException('Connection error')

        # Test the function
        with self.assertRaises(requests.RequestException):
            provision_botfather_message('/newbot')

    @patch('sys.argv', ['botfather.py', '/newbot'])
    @patch('botfather.provision_botfather_message')
    def test_cli_success(self, mock_provision):
        # Mock successful function call
        mock_provision.return_value = [
            'BotFather reply 1',
            'BotFather reply 2',
            'BotFather reply 3'
        ]

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Run the CLI
        main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify output
        output = captured_output.getvalue()
        self.assertIn('BotFather reply 1', output)
        self.assertIn('BotFather reply 2', output)
        self.assertIn('BotFather reply 3', output)

    @patch('sys.argv', ['botfather.py', '/newbot'])
    @patch('botfather.provision_botfather_message')
    def test_cli_error(self, mock_provision):
        # Mock function raising an exception
        mock_provision.side_effect = requests.RequestException('Connection error')

        # Capture stdout (since error is printed to stdout)
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Run the CLI and expect SystemExit
        with self.assertRaises(SystemExit) as cm:
            main()
        # Restore stdout
        sys.stdout = sys.__stdout__
        # Verify error message
        output = captured_output.getvalue()
        self.assertIn('Error:', output)
        self.assertIn('Connection error', output)
        # Assert exit code is 1
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main() 
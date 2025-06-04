""" test_local_model.py

Copyright 2025, Cornell University

Cornell University asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including online repositories
such as Github.

Sharing solutions with current or future students of ENMGT5400 is
prohibited and subject to being investigated as a Code of Academic Integrity violation.

-----do not edit anything above this line---
"""

import unittest
from unittest.mock import patch, Mock
from local_model import generate_response, recommend_trade, select_short, select_long


class TestLocalModel(unittest.TestCase):

    def test_generate_response(self):
        prompt = "SAY ONLY ONE WORD: Hello"
        model_response = generate_response(prompt)
        # Check that the model_response contains hello
        self.assertIn("hello", model_response.lower())

    def test_recommend_trade_short(self):

        country = "United States"
        event_summary = f"DO NOT INVEST IN {country}"
        expected_recommendation = select_short(country)
        recommendation = recommend_trade(country, event_summary)
        self.assertEqual(recommendation, expected_recommendation)

    def test_recommend_trade_long(self):

        country = "United States"
        event_summary = f"INVEST IN {country}"
        expected_recommendation = select_long(country)
        recommendation = recommend_trade(country, event_summary)
        self.assertEqual(recommendation, expected_recommendation)

    @patch("ollama.Client")
    def test_generate_response_called_once(self, MockClient):
        """
        Tests that ollama.Client is called once.
        """
        mock_client_instance = Mock()
        mock_response = {"response": "Some response"}
        mock_client_instance.generate.return_value = mock_response

        MockClient.return_value = mock_client_instance

        model = "llama3.2"
        prompt = "Hello World!"

        # Call the function that uses ollama.Client
        result = generate_response(prompt)

        MockClient.assert_called_once()
        mock_client_instance.generate.assert_called_once_with(
            model=model, prompt=prompt
        )

    @patch("local_model.ollama.Client")
    def test_recommend_trade_calls_chat(self, MockClient):
        """
        Tests that ollama.Client is called at least once and the chat method is called at least once.
        """
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_tool_call = Mock()
        mock_tool_call.function.name = "select_long"
        mock_tool_call.function.arguments = {"country": "USA"}
        mock_message = Mock()
        mock_message.tool_calls = [mock_tool_call]
        mock_response.message = mock_message
        mock_client_instance.chat.return_value = mock_response

        MockClient.return_value = mock_client_instance

        country_of_interest = "USA"
        event_summary = "Positive economic indicators."

        result = recommend_trade(country_of_interest, event_summary)

        MockClient.assert_called_once()
        mock_client_instance.chat.assert_called_once()
        self.assertEqual(result, "Long USA")

    @patch("local_model.ollama.Client")
    def test_recommend_trade_calls_chat_short(self, MockClient):
        """
        Tests that ollama.Client is called at least once and the chat method is called at least once, short case.
        """
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_tool_call = Mock()
        mock_tool_call.function.name = "select_short"
        mock_tool_call.function.arguments = {"country": "China"}
        mock_message = Mock()
        mock_message.tool_calls = [mock_tool_call]
        mock_response.message = mock_message
        mock_client_instance.chat.return_value = mock_response

        MockClient.return_value = mock_client_instance

        country_of_interest = "China"
        event_summary = "Negative economic indicators."

        result = recommend_trade(country_of_interest, event_summary)

        MockClient.assert_called_once()
        mock_client_instance.chat.assert_called_once()
        self.assertEqual(result, "Short China")


if __name__ == "__main__":
    unittest.main()

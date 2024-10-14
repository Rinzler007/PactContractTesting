import atexit
import unittest
from pact import Consumer, Provider, Like, EachLike
import requests
import os
import warnings

# Suppress Deprecation Warnings (Temporary Measure)
warnings.filterwarnings("ignore", category=DeprecationWarning)

os.environ['NO_PROXY'] = 'localhost,127.0.0.1'

# Define Pact between the Consumer and Provider
pact = Consumer('toolbar-chat-api').has_pact_with(
    Provider('unv-bcd-chat-pdr'),
    pact_dir='./pacts',
    port=1235
)
pact.start_service()
atexit.register(pact.stop_service)  # Ensure service is stopped at exit


class GetChatDataConsumerTest(unittest.TestCase):

    def setUp(self):
        """Set up before each test case."""
        self.pact = pact

    def tearDown(self):
        """Clean up after each test case."""
        pass  # The mock service is already stopped by atexit

    def define_interaction(self, description, consumer_type, expected_response, status_code=200):
        """Helper method to define Pact interactions."""
        # Define the expected interaction with the Provider
        (self.pact
         .given(f'Chat data of {consumer_type} consumer exists')
         .upon_receiving(description)
         .with_request(
             'GET',
             '/actions/bcd/chat-template',
             query={'consumer': consumer_type}
         )
         .will_respond_with(status_code, body=expected_response))

    def test_get_chat_data_fullserve(self):
        """Test case for consumer 'fullserve'."""
        consumer_type = 'fullserve'
        expected_interaction = {
            "data": {
                "type": "ChatTemplate",
                "attributes": {
                    "templates": EachLike(
                        {
                            "id": Like("2"),
                            "consumer": "fullserve",
                            "title": Like("title2"),
                            "category": Like("category2"),
                            "message": Like("message2"),
                            "queues": EachLike("queue3")
                        }
                    )
                }
            }
        }

        # Define the expected concrete response for assertions
        expected_response = {
            "data": {
                "type": "ChatTemplate",
                "attributes": {
                    "templates": [
                        {
                            "id": "2",
                            "consumer": "fullserve",
                            "title": "title2",
                            "category": "category2",
                            "message": "message2",
                            "queues": ["queue3"]
                        },
                        # Add more concrete templates if needed
                    ]
                }
            }
        }

        # Define interaction
        self.define_interaction(
            description='A request to get chat data for fullserve',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            status_code=200
        )

        # Run the test: Make the actual request
        with self.pact:
            result = requests.get(f'{pact.uri}/actions/bcd/chat-template?consumer={consumer_type}')

        # Assert that the result matches the expectation
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_response)

    def test_get_chat_data_veripark(self):
        """Test case for consumer 'veripark'."""
        consumer_type = 'veripark'
        expected_interaction = {
            "data": {
                "type": "ChatTemplate",
                "attributes": {
                    "templates": EachLike(
                        {
                            "id": Like("3"),
                            "consumer": "veripark",
                            "title": Like("title3"),
                            "category": Like("category3"),
                            "message": Like("message3"),
                            "queues": EachLike("queue4")
                        }
                    )
                }
            }
        }

        # Define the expected concrete response for assertions
        expected_response = {
            "data": {
                "type": "ChatTemplate",
                "attributes": {
                    "templates": [
                        {
                            "id": "3",
                            "consumer": "veripark",
                            "title": "title3",
                            "category": "category3",
                            "message": "message3",
                            "queues": ["queue4"]
                        },
                        # Add more concrete templates if needed
                    ]
                }
            }
        }

        # Define interaction
        self.define_interaction(
            description='A request to get chat data for veripark',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            status_code=200
        )

        # Run the test: Make the actual request
        with self.pact:
            result = requests.get(f'{pact.uri}/actions/bcd/chat-template?consumer={consumer_type}')

        # Assert that the result matches the expectation
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_response)

    def test_get_chat_data_salesforce(self):
        """Test case for consumer 'salesforce'."""
        consumer_type = 'salesforce'
        expected_interaction = {
            "data": {
                "type": "ChatTemplate",
                "attributes": {
                    "templates": EachLike(
                        {
                            "id": Like("4"),
                            "consumer": "salesforce",
                            "title": Like("title4"),
                            "category": Like("category4"),
                            "message": Like("message4"),
                            "queues": EachLike("queue5")
                        }
                    )
                }
            }
        }

        # Define the expected concrete response for assertions
        expected_response = {
            "data": {
                "type": "ChatTemplate",
                "attributes": {
                    "templates": [
                        {
                            "id": "4",
                            "consumer": "salesforce",
                            "title": "title4",
                            "category": "category4",
                            "message": "message4",
                            "queues": ["queue5"]
                        },
                        # Add more concrete templates if needed
                    ]
                }
            }
        }

        # Define interaction
        self.define_interaction(
            description='A request to get chat data for salesforce',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            status_code=200
        )

        # Run the test: Make the actual request
        with self.pact:
            result = requests.get(f'{pact.uri}/actions/bcd/chat-template?consumer={consumer_type}')

        # Assert that the result matches the expectation
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_response)

    def test_get_chat_data_invalid_consumer(self):
        """Test case for an invalid consumer."""
        consumer_type = 'invalid'
        expected_interaction = {
            "error": {
                "code": 404,
                "message": "Consumer not found."
            }
        }

        # Define interaction for invalid consumer
        self.define_interaction(
            description='A request to get chat data for an invalid consumer',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            status_code=404
        )

        # Run the test: Make the actual request
        with self.pact:
            result = requests.get(f'{pact.uri}/actions/bcd/chat-template?consumer={consumer_type}')

        # Assert the 404 response for invalid consumer
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.json(), expected_interaction)


if __name__ == '__main__':
    unittest.main()

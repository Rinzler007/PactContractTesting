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

    def define_interaction(self, description, consumer_type, expected_response, status_code=200, auth_required=True, token=None):
        """Helper method to define Pact interactions."""
        headers = {}
        if auth_required and token:
            headers = {"Authorization": f"Bearer {token}"}

        # Define the expected interaction with the Provider
        (self.pact
         .given(f'Chat data of {consumer_type} consumer exists')
         .upon_receiving(description)
         .with_request(
             'GET',
             '/bcd-dev/actions/bcd/chat-template',
             headers=headers,
             query={'consumer': consumer_type}
         )
         .will_respond_with(status_code, body=expected_response))

    def test_get_chat_data_fullserve(self):
        """Test case for consumer 'fullserve'."""
        consumer_type = 'fullserve'
        expected_interaction = {
            "data": {
                "type": "ChatTemplates",
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
                "type": "ChatTemplates",
                "attributes": {
                    "templates": [
                        {
                            "id": "2",
                            "consumer": "fullserve",
                            "title": "title2",
                            "category": "category2",
                            "message": "message2",
                            "queues": ["queue3"]
                        }
                    ]
                }
            }
        }

        # Manually provide the token
        token = 'your_dynamic_token_here'

        # Define interaction
        self.define_interaction(
            description='A request to get chat data for fullserve',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            token=token
        )

        # Run the test: Make the actual request
        with self.pact:
            result = requests.get(f'{pact.uri}/bcd-dev/actions/bcd/chat-template?consumer={consumer_type}', headers={"Authorization": f"Bearer {token}"})

        # Assert that the result matches the expectation
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_response)

    def test_get_chat_data_veripark(self):
        """Test case for consumer 'veripark'."""
        consumer_type = 'veripark'
        expected_interaction = {
            "data": {
                "type": "ChatTemplates",
                "attributes": {
                    "templates": EachLike(
                        {
                            "id": Like("2"),
                            "consumer": "veripark",
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
                "type": "ChatTemplates",
                "attributes": {
                    "templates": [
                        {
                            "id": "2",
                            "consumer": "veripark",
                            "title": "title2",
                            "category": "category2",
                            "message": "message2",
                            "queues": ["queue3"]
                        }
                    ]
                }
            }
        }

        # Manually provide the token
        token = 'your_dynamic_token_here'

        # Define interaction
        self.define_interaction(
            description='A request to get chat data for veripark',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            token=token
        )

        # Run the test: Make the actual request
        with self.pact:
            result = requests.get(f'{pact.uri}/bcd-dev/actions/bcd/chat-template?consumer={consumer_type}', headers={"Authorization": f"Bearer {token}"})

        # Assert that the result matches the expectation
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_response)

    def test_get_chat_data_salesforce(self):
        """Test case for consumer 'salesforce'."""
        consumer_type = 'salesforce'
        expected_interaction = {
            "data": {
                "type": "ChatTemplates",
                "attributes": {
                    "templates": EachLike(
                        {
                            "id": Like("2"),
                            "consumer": "salesforce",
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
                "type": "ChatTemplates",
                "attributes": {
                    "templates": [
                        {
                            "id": "2",
                            "consumer": "salesforce",
                            "title": "title2",
                            "category": "category2",
                            "message": "message2",
                            "queues": ["queue3"]
                        }
                    ]
                }
            }
        }

        # Manually provide the token
        token = 'your_dynamic_token_here'

        # Define interaction
        self.define_interaction(
            description='A request to get chat data for salesforce',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            token=token
        )

        # Run the test: Make the actual request
        with self.pact:
            result = requests.get(f'{pact.uri}/bcd-dev/actions/bcd/chat-template?consumer={consumer_type}', headers={"Authorization": f"Bearer {token}"})

        # Assert that the result matches the expectation
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_response)

    def test_get_chat_data_blank_consumer(self):
        """Test case for blank consumer."""
        consumer_type = ''
        expected_interaction = {
            "errors": [
                {
                    "title": "BadRequest",
                    "detail": "Empty consumer id",
                    "status": "400"
                }
            ]
        }

        # Manually provide the token
        token = 'your_dynamic_token_here'

        # Define interaction for blank consumer
        self.define_interaction(
            description='A request with blank consumer',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            status_code=400,
            token=token
        )

        # Run the test: Make the actual request
        with self.pact:
            result = requests.get(f'{pact.uri}/bcd-dev/actions/bcd/chat-template?consumer={consumer_type}', headers={"Authorization": f"Bearer {token}"})

        # Assert the 400 response for blank consumer
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.json(), expected_interaction)

    def test_get_chat_data_invalid_consumer(self):
        """Test case for an invalid consumer should return 200 with an empty template list."""
        consumer_type = 'invalid'
        expected_interaction = {
            "data": {
                "type": "ChatTemplates",
                "attributes": {
                    "templates": []
                }
            }
        }

        # Manually provide the token
        token = 'your_dynamic_token_here'

        # Define interaction for invalid consumer
        self.define_interaction(
            description='A request to get chat data for an invalid consumer',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            token=token
        )

        # Run the test: Make the actual request
        with self.pact:
            result = requests.get(f'{pact.uri}/bcd-dev/actions/bcd/chat-template?consumer={consumer_type}', headers={"Authorization": f"Bearer {token}"})

        # Assert that the result matches the expectation
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_interaction)

    def test_get_chat_data_no_authorization(self):
        """Test case for missing Authorization header should return 401."""
        consumer_type = 'fullserve'
        expected_interaction = {
            "message": "Unauthorized"
        }

        # Define interaction for missing Authorization
        self.define_interaction(
            description='A request with no Authorization header',
            consumer_type=consumer_type,
            expected_response=expected_interaction,
            status_code=401,
            auth_required=False
        )

        # Run the test: Make the actual request without Authorization header
        with self.pact:
            result = requests.get(f'{pact.uri}/bcd-dev/actions/bcd/chat-template?consumer={consumer_type}')

        # Assert the 401 response for missing Authorization
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.json(), expected_interaction)


if __name__ == '__main__':
    unittest.main()

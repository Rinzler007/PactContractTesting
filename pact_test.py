import atexit
import unittest
from pact import Consumer, Provider
import requests

# Define Pact between the Consumer and Provider
pact = Consumer('toolbar-chat-api').has_pact_with(Provider('unv-bcd-chat-pdr'), pact_dir='./pacts')
pact.start_service()
atexit.register(pact.stop_service)  # Ensure service is stopped at exit

class GetChatDataConsumerTest(unittest.TestCase):

    def test_get_chat_data(self):
        expected = {
            "data": {
                "type": "ChatTemplate",
                "attributes": {
                    "templates": [
                        {
                            "id": "1",
                            "consumer": "fullserve",
                            "title": "title1",
                            "category": "category1",
                            "message": "message1",
                            "queues": ["queue1", "queue2"]
                        },
                        {
                            "id": "2",
                            "consumer": "fullserve",
                            "title": "title2",
                            "category": "category2",
                            "message": "message2",
                            "queues": ["queue3", "queue4"]
                        }
                    ]
                }
            }
        }

        # Define the expected interaction with the Provider
        (pact
         .given('Chat data of fullserve consumer exists')
         .upon_receiving('A request to get chat data')
         .with_request('get', '/actions/bcd/chat-template')
         .will_respond_with(200, body=expected))

        # Run the test: Make the actual request
        with pact:
            result = requests.get(f'{pact.uri}/actions/bcd/chat-template')

        # Assert that the result matches the expectation
        self.assertEqual(result.json(), expected)
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()

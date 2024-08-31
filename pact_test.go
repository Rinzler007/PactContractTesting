package main

import (
	"encoding/json"
	"testing"

	"github.com/pact-foundation/pact-go/dsl"
	"github.com/stretchr/testify/assert"
)

func GetChatData() string {
	chatData := ProducerResponseAttributes{
		ProducerChatTemplates: []ProducerChatTemplate{
			{
				Id:       "1",
				Consumer: "fullserve",
				Title:    "title1",
				Category: "category1",
				Message:  "message1",
				Queues:   []string{"queue1", "queue2"},
			},
			{
				Id:       "2",
				Consumer: "fullserve",
				Title:    "title2",
				Category: "category2",
				Message:  "message2",
				Queues:   []string{"queue3", "queue4"},
			},
			{
				Id:       "3",
				Consumer: "fullserve",
				Title:    "title3",
				Category: "category3",
				Message:  "message3",
				Queues:   []string{"queue5"},
			},
			{
				Id:       "4",
				Consumer: "fullserve",
				Title:    "title4",
				Category: "category4",
				Message:  "message4",
				Queues:   []string{"queue6", "queue7", "queue8"},
			},
		},
	}
	byteArr, _ := json.Marshal(chatData)
	return string(byteArr)
}

func TestConsumerPact(t *testing.T) {
	pact := &dsl.Pact{
		Consumer:                 "GoConsumerContractTesting",
		Provider:                 "GoProviderContractTesting",
		DisableToolValidityCheck: true,
		PactDir:                  "./pacts",
		LogDir:                   "./logs",
		Host:                     "localhost",
	}
	defer pact.Teardown()
	pact.AddInteraction().Given("Chat data of fullserve consumer exists").
		UponReceiving("A request to get chat data").
		WithRequest(dsl.Request{
			Method:  "GET",
			Path:    dsl.String("/actions/bcd/chat-template"),
			Headers: dsl.MapMatcher{"Content-Type": dsl.String("application/json")},
		}).
		WillRespondWith(dsl.Response{
			Status:  200,
			Headers: dsl.MapMatcher{"Content-Type": dsl.String("application/json")},
			Body: dsl.Like(ProducerResponseWrapper{
				Data: ProducerResponseData{
					Type: "ChatTemplate",
					Attributes: ProducerResponseAttributes{
						ProducerChatTemplates: []ProducerChatTemplate{
							{
								Id:       "1",
								Consumer: "fullserve",
								Title:    "title1",
								Category: "category1",
								Message:  "message1",
								Queues:   []string{"queue1", "queue2"},
							},
							{
								Id:       "2",
								Consumer: "fullserve",
								Title:    "title2",
								Category: "category2",
								Message:  "message2",
								Queues:   []string{"queue3", "queue4"},
							},
							{
								Id:       "3",
								Consumer: "fullserve",
								Title:    "title3",
								Category: "category3",
								Message:  "message3",
								Queues:   []string{"queue5"},
							},
							{
								Id:       "4",
								Consumer: "fullserve",
								Title:    "title4",
								Category: "category4",
								Message:  "message4",
								Queues:   []string{"queue6", "queue7", "queue8"},
							},
						},
					},
				},
			}),
		})
	err := pact.Verify(func() error {
		producerResponse, err := callProducerAPI()
		assert.NoError(t, err)
		assert.NotEmpty(t, producerResponse.Data.Attributes.ProducerChatTemplates)
		return nil
	})
	assert.NoError(t, err)
}

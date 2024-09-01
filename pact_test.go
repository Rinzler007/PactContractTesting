package main

import (
	"fmt"
	"net/http"
	"os"
	"testing"

	"github.com/google/martian/log"
	"github.com/pact-foundation/pact-go/dsl"
	"github.com/pact-foundation/pact-go/types"
	"github.com/stretchr/testify/assert"
)

func GetChatData() ProducerResponseWrapper {
	return ProducerResponseWrapper{
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
	}
}

func hitChatDataAPI() (err error) {
	url := fmt.Sprintf("http://localhost:%d/actions/bcd/chat-template", pact.Server.Port)
	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("Content-Type", "application/json")

	http.DefaultClient.Do(req)

	return
}

var pact dsl.Pact
var dir, _ = os.Getwd()
var pactDir = fmt.Sprintf("%s/pacts", dir)
var logDir = fmt.Sprintf("%s/logs", dir)

func TestMain(m *testing.M) {
	// Setup Pact and related test stuff
	pact = dsl.Pact{
		Consumer:                 "toolbar-chat-api",
		Provider:                 "unv-bcd-chat-pdr",
		DisableToolValidityCheck: true,
		PactDir:                  pactDir,
		LogDir:                   logDir,
	}

	// Proactively start service to get access to the port
	pact.Setup(true)

	// Run all the tests
	code := m.Run()

	// Shutdown the Mock Service and write pact files to disk
	err := pact.WritePact()
	if err != nil {
		log.Infof("Failed to write your contract")
		return
	}

	pact.Teardown()
	os.Exit(code)
}

func TestConsumerPact(t *testing.T) {
	chatData := GetChatData()
	pact.AddInteraction().Given("Chat data of fullserve consumer exists").
		UponReceiving("A request to get chat data").
		WithRequest(dsl.Request{
			Method: "GET",
			Path:   dsl.Term("/actions/bcd/chat-template", "/actions/bcd/chat-template"),
			Headers: dsl.MapMatcher{
				"Content-Type": dsl.Term("application/json", `application\/json`),
			},
		}).
		WillRespondWith(dsl.Response{
			Status: 200,
			Headers: dsl.MapMatcher{
				"Content-Type": dsl.Term("application/json", `application\/json`),
			},
			Body: chatData,
		})
	err := pact.Verify(hitChatDataAPI)
	if err != nil {
		t.Fatalf("Error on Verify: %v", err)
	}
	assert.NoError(t, err)

	// Store contract remotely
	publisher := dsl.Publisher{}
	err = publisher.Publish(types.PublishRequest{
		PactURLs:        []string{"pacts/toolbar-chat-api-unv-bcd-chat-pdr.json"},
		PactBroker:      "https://harsh.pactflow.io/", //link to your remote Contract broker
		BrokerToken:     "2_KfMXbOMRXKAd30PwopTg",     //your PactFlow token
		ConsumerVersion: "1.0.0",
		Tags:            []string{"1.0.0", "latest"},
	})
	if err != nil {
		t.Fatal(err)
	}
	assert.NoError(t, err)
}

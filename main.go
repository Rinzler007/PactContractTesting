package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"

	"github.com/aws/aws-lambda-go/events"
)

type ProducerResponseWrapper struct {
	Data ProducerResponseData `json:"data"`
}

type ProducerResponseData struct {
	Type       string                     `json:"type"`
	Attributes ProducerResponseAttributes `json:"attributes"`
}

type ProducerResponseAttributes struct {
	ProducerChatTemplates []ProducerChatTemplate `json:"templates"`
}

type ProducerChatTemplate struct {
	Id             string   `json:"id"`
	Consumer       string   `json:"consumer"`
	Title          string   `json:"title"`
	Category       string   `json:"category"`
	Message        string   `json:"message"`
	Queues         []string `json:"queues" dynamodbav:"-"`
	QueueList      []Queue  `json:"-" dynamodbav:"queues"`
	RecordDisabled bool     `json:"recordDisabled"`
}

type Queue struct {
	QueueName string `json:"queueName"`
	QueueARN  string `json:"queueArn"`
}

func callProducerAPI() (ProducerResponseWrapper, error) {
	resp, err := http.Get("http://localhost:8080/actions/bcd/chat-template")
	if err != nil {
		return ProducerResponseWrapper{}, err
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return ProducerResponseWrapper{}, err
	}
	producerResponse := ProducerResponseWrapper{}
	err = json.Unmarshal(body, &producerResponse)
	if err != nil {
		return ProducerResponseWrapper{}, err
	}
	return producerResponse, nil
}

func Handler() (events.APIGatewayProxyResponse, error) {
	producerResponse, err := callProducerAPI()
	if err != nil {
		return events.APIGatewayProxyResponse{
			StatusCode: http.StatusInternalServerError,
			Body:       err.Error(),
		}, nil
	}
	responseBody, _ := json.Marshal(producerResponse)
	return events.APIGatewayProxyResponse{
		StatusCode: http.StatusOK,
		Headers:    map[string]string{"Content-Type": "application/json"},
		Body:       string(responseBody),
	}, nil
}

func main() {
	http.HandleFunc("/fullserve/toolbar/chat/templates", func(w http.ResponseWriter, r *http.Request) {
		resp, err := Handler()
		if err != nil {
			http.Error(w, err.Error(), resp.StatusCode)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(resp.StatusCode)
		w.Write([]byte(resp.Body))
	})
	log.Fatal(http.ListenAndServe(":8081", nil))
}

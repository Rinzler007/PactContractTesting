package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
)

// Struct Definitions

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
	RecordDisabled bool     `json:"recordDisabled,omitempty"` // Added `omitempty`
}

type Queue struct {
	QueueName string `json:"queueName"`
	QueueARN  string `json:"queueArn"`
}

// AllowedConsumers defines the set of valid consumer values
var AllowedConsumers = map[string]bool{
	"fullserve":  true,
	"veripark":   true,
	"salesforce": true,
}

// callProducerAPI makes an HTTP GET request to the Producer API with the given consumer
func callProducerAPI(consumer string) (ProducerResponseWrapper, error) {
	// Construct the Producer API URL with the consumer query parameter
	producerURL := fmt.Sprintf("http://localhost:8080/actions/bcd/chat-template?consumer=%s", consumer)

	// Make the GET request
	resp, err := http.Get(producerURL)
	if err != nil {
		return ProducerResponseWrapper{}, fmt.Errorf("failed to call Producer API: %w", err)
	}
	defer resp.Body.Close()

	// Read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return ProducerResponseWrapper{}, fmt.Errorf("failed to read Producer API response: %w", err)
	}

	// Check if Producer API returned a non-200 status code
	if resp.StatusCode != http.StatusOK {
		return ProducerResponseWrapper{}, fmt.Errorf("Producer API returned status %d: %s", resp.StatusCode, string(body))
	}

	// Unmarshal the JSON response into ProducerResponseWrapper
	producerResponse := ProducerResponseWrapper{}
	err = json.Unmarshal(body, &producerResponse)
	if err != nil {
		return ProducerResponseWrapper{}, fmt.Errorf("failed to unmarshal Producer API response: %w", err)
	}

	return producerResponse, nil
}

// Handler processes the HTTP request and returns the appropriate response
func Handler(consumer string) (int, string) {
	// Call the Producer API with the validated consumer
	producerResponse, err := callProducerAPI(consumer)
	if err != nil {
		// If the error is due to an invalid consumer, return 404
		if strings.Contains(err.Error(), "Producer API returned status 404") {
			return http.StatusNotFound, `{"error": "Consumer not found"}`
		}
		// For other errors, return 500
		log.Printf("Internal Server Error: %v", err)
		return http.StatusInternalServerError, `{"error": "Internal Server Error"}`
	}

	// Marshal the Producer API response to JSON
	responseBody, err := json.Marshal(producerResponse)
	if err != nil {
		log.Printf("JSON Marshaling Error: %v", err)
		return http.StatusInternalServerError, `{"error": "Internal Server Error"}`
	}

	// Return the successful response
	return http.StatusOK, string(responseBody)
}

// main sets up the HTTP server and routes
func main() {
	// Define the handler function
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Expected path format: /{consumer}/toolbar/chat/templates
		// Example: /fullserve/toolbar/chat/templates
		path := r.URL.Path
		segments := strings.Split(path, "/")

		// Validate the path segments
		// segments[0] is "", segments[1] is {consumer}, segments[2] is "toolbar", segments[3] is "chat", segments[4] is "templates"
		if len(segments) != 5 || segments[2] != "toolbar" || segments[3] != "chat" || segments[4] != "templates" {
			http.NotFound(w, r)
			return
		}

		// Extract the consumer from the path
		consumer := segments[1]

		// Validate the consumer
		if _, valid := AllowedConsumers[consumer]; !valid {
			http.NotFound(w, r)
			return
		}

		// Call the Handler with the valid consumer
		statusCode, responseBody := Handler(consumer)

		// Set the appropriate headers and status code
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(statusCode)
		w.Write([]byte(responseBody))
	})

	// Start the HTTP server on port 8081
	log.Println("Consumer API server is running on port 8081")
	log.Fatal(http.ListenAndServe(":8081", nil))
}

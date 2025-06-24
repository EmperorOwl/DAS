package main

import (
	"fmt"
	"os"
)

const (
	port = "8080"
)

var workerPool *WorkerPool

func main() {
	// Create the worker pool
	var err error
	workerPool, err = NewWorkerPool(4)
	if err != nil {
		panic(fmt.Sprintf("Failed to start worker pool: %v", err))
	}

	// Start the server
	router := SetupRouter()
	fmt.Printf("Server starting on port %s...\n", port)
	if err := router.Run(":" + port); err != nil {
		fmt.Printf("Error starting server: %v\n", err)
		os.Exit(1)
	}
}

package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type Request map[string]interface{}

type Response struct {
	// 200 OK response containing OR
	Pretty map[string]interface{} `json:"pretty"` // string or string[]
	Image  *string                `json:"image"`
	Answer interface{}            `json:"answer"` // string, string[], or nil
	// 400 Bad Request response containing
	ErrorName    *string `json:"name"`
	ErrorMessage *string `json:"message"`
}

func HandleOperation(operation string, timeout time.Duration) gin.HandlerFunc {
	return func(c *gin.Context) {
		// Parse the request
		var args Request
		if err := c.ShouldBindJSON(&args); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		req := map[string]interface{}{
			"operation": operation,
			"args":      args,
		}

		// Offload the request to a worker
		worker := workerPool.GetWorker()
		if worker == nil {
			errMsg := "No available workers"
			c.JSON(http.StatusInternalServerError, gin.H{"error": errMsg})
			return
		}
		resp, err := worker.SendRequest(req, timeout)
		if err != nil {
			if err.Error() == "worker timed out and was killed" {
				errMsg := fmt.Sprintf("Exceeded time limit of %v seconds",
					timeout)
				c.JSON(http.StatusRequestEntityTooLarge, gin.H{"error": errMsg})
				return
			}
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		// Parse the JSON output
		var result Response
		if err := json.Unmarshal(resp, &result); err != nil {
			errMsg := "error parsing JSON output: " + err.Error()
			c.JSON(http.StatusInternalServerError, gin.H{"error": errMsg})
			return
		}

		if result.ErrorName != nil {
			c.JSON(http.StatusBadRequest, &result)
			return
		}

		c.JSON(http.StatusOK, &result)
	}
}

# API

This is the API component of the Discord Algebra System (DAS).
It is a REST API built with Go and the Gin web framework. Each request is processed in a Python subprocess, which can be efficiently terminated based on a configured timeout.

## Running the API

### Dependencies

The API requires:
- Go 1.21 or higher
- Python environment with required packages (see requirements.txt)

### Local Development

1. Make sure you're in the `api` directory
    ```shell
    cd api
    ```
2. Start the server
    ```shell
    go run app/main.go app/server.go app/controller.go
    ```

## Testing

### Unit Tests

1. Make sure you're in the `api` directory
    ```shell
    cd api
    ```
2. Run the unit tests
    ```
    clear; python -m scripts.tests.run_tests
    clear; python -m scripts.tests.test_algebra
    ```

### Integration Tests

1. Make sure you're in the `api/app` directory
    ```shell
    cd api/app
    ```
2. Run the unit tests
    ```shell
    clear; go test
    clear; go test -run TestEvaluateEndpoint
    ```

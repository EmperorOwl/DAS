# Build stage for Go
FROM golang:1.21-alpine AS go-builder

WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the source code
COPY app/ ./app/

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -o main ./app

# Python stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python scripts
COPY scripts/ ./scripts/
COPY --from=go-builder /app/main ./app/main

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["./app/main"] 
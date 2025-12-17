#!/bin/bash

# Stop any existing wiremock container
docker rm -f wiremock 2>/dev/null

# Start WireMock on port 9090 with mappings from test/wiremock
docker run -d \
  --name wiremock \
  -p 9090:8080 \
  -v $(pwd)/test/wiremock:/home/wiremock \
  wiremock/wiremock:latest

if [ $? -eq 0 ]; then
    echo "WireMock started on port 9090"
    echo "Container ID: $(docker ps -qf name=wiremock)"
else
    echo "Failed to start WireMock"
fi

#!/bin/bash

# Stop any existing jmeter container
docker rm -f jmeter 2>/dev/null

# Start JMeter on port 9091 with test plans from test/jmeter
docker run -d \
  --name jmeter \
  -p 9091:8080 \
  -v "$(pwd)/test/jmeter":/jmeter \
  justb4/jmeter:latest

if [ $? -eq 0 ]; then
    echo "JMeter started on port 9091"
    echo "Container ID: $(docker ps -qf name=jmeter)"
else
    echo "Failed to start JMeter"
fi

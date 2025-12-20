#!/bin/bash

docker rm -f jmeter 2>/dev/null

if [ $? -eq 0 ]; then
    echo "JMeter server stopped"
else
    echo "No JMeter container found"
fi

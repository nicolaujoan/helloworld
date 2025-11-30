#!/bin/bash

docker rm -f wiremock 2>/dev/null

if [ $? -eq 0 ]; then
    echo "WireMock server stopped"
else
    echo "No WireMock container found"
fi

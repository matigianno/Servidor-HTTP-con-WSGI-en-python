#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9292/tasks)
if [ "$response" -eq 200 ]; then
  echo "PASS: GET /tasks devolvió 200"
else
  echo "FAIL: GET /tasks devolvió $response"
fi
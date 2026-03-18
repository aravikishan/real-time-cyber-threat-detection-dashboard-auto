#!/bin/bash
set -e
echo "Starting Real-Time Cyber Threat Detection Dashboard..."
uvicorn app:app --host 0.0.0.0 --port 9116 --workers 1

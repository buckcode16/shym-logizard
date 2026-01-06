#!/bin/bash

cd "$(dirname "$0")" || exit 1

if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Error: .venv directory not found."
    exit 1
fi

MAX_RETRIES=3
WAIT_SECONDS=60
attempt=1

while [ $attempt -le $MAX_RETRIES ]; do
    echo "[BatchRunner] Starting attempt #$attempt..."
    
    python3 -m src.main
    
    if [ $? -eq 0 ]; then
        echo "[BatchRunner] Success."
        exit 0
    else
        echo "[BatchRunner] Attempt #$attempt Failed."
        if [ $attempt -lt $MAX_RETRIES ]; then
            echo "[BatchRunner] Waiting ${WAIT_SECONDS}s..."
            sleep $WAIT_SECONDS
            ((attempt++))
        else
            echo "[BatchRunner] All attempts failed. Exiting."
            exit 1
        fi
    fi
done
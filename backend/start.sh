#!/bin/bash
echo "Creating test data..."
python create_test_data.py

echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
#!/bin/bash

# Test script for Round 1A - PDF Outline Extraction

echo "Testing Round 1A - PDF Outline Extraction"
echo "=========================================="

# Create test directories
mkdir -p test_input test_output

# Build Docker image
echo "Building Docker image..."
cd round1a
docker build --platform linux/amd64 -t pdf-outline-extractor:test .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Docker build failed"
    exit 1
fi

# Run the container
echo "Running PDF outline extraction..."
docker run --rm \
    -v $(pwd)/../test_input:/app/input \
    -v $(pwd)/../test_output:/app/output \
    --network none \
    pdf-outline-extractor:test

if [ $? -eq 0 ]; then
    echo "✅ Container executed successfully"
    echo "Output files:"
    ls -la ../test_output/
else
    echo "❌ Container execution failed"
    exit 1
fi

cd ..
echo "Round 1A test completed!"

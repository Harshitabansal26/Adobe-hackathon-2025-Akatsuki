#!/bin/bash

# Test script for Round 1B - Persona-Driven Intelligence

echo "Testing Round 1B - Persona-Driven Intelligence"
echo "=============================================="

# Create test directories
mkdir -p test_input_1b test_output_1b

# Create sample config file
cat > test_input_1b/config.json << EOF
{
  "documents": [
    "/app/input/sample1.pdf",
    "/app/input/sample2.pdf"
  ],
  "persona": "PhD Researcher in Computer Science",
  "job_to_be_done": "Analyze machine learning methodologies and performance benchmarks for research paper review"
}
EOF

# Build Docker image
echo "Building Docker image..."
cd round1b
docker build --platform linux/amd64 -t persona-intelligence:test .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Docker build failed"
    exit 1
fi

# Run the container
echo "Running persona-driven intelligence..."
docker run --rm \
    -v $(pwd)/../test_input_1b:/app/input \
    -v $(pwd)/../test_output_1b:/app/output \
    --network none \
    persona-intelligence:test

if [ $? -eq 0 ]; then
    echo "✅ Container executed successfully"
    echo "Output files:"
    ls -la ../test_output_1b/
else
    echo "❌ Container execution failed"
    exit 1
fi

cd ..
echo "Round 1B test completed!"

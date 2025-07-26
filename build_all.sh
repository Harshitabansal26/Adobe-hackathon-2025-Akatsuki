#!/bin/bash

# Build script for Adobe Hackathon Challenge
# Builds both Round 1A and Round 1B Docker images

echo "Adobe Hackathon Challenge - Build Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed or not in PATH"
    exit 1
fi

print_status "Docker found: $(docker --version)"

# Build Round 1A
print_status "Building Round 1A - PDF Outline Extractor..."
cd round1a

if docker build --platform linux/amd64 -t pdf-outline-extractor:latest .; then
    print_status "✅ Round 1A Docker image built successfully"
else
    print_error "❌ Round 1A Docker build failed"
    exit 1
fi

cd ..

# Build Round 1B
print_status "Building Round 1B - Persona-Driven Intelligence..."
cd round1b

if docker build --platform linux/amd64 -t persona-intelligence:latest .; then
    print_status "✅ Round 1B Docker image built successfully"
else
    print_error "❌ Round 1B Docker build failed"
    exit 1
fi

cd ..

# List built images
print_status "Built Docker images:"
docker images | grep -E "(pdf-outline-extractor|persona-intelligence)"

echo ""
print_status "Build completed successfully!"
print_status "You can now run the solutions using:"
echo ""
echo "Round 1A:"
echo "docker run --rm -v \$(pwd)/input:/app/input -v \$(pwd)/output:/app/output --network none pdf-outline-extractor:latest"
echo ""
echo "Round 1B:"
echo "docker run --rm -v \$(pwd)/input:/app/input -v \$(pwd)/output:/app/output --network none persona-intelligence:latest"

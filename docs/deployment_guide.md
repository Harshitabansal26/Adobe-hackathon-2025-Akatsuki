# Deployment Guide

This guide provides step-by-step instructions for deploying the Adobe Hackathon Challenge solutions.

## System Requirements

### Hardware
- **CPU**: AMD64 (x86_64) architecture
- **RAM**: Minimum 8GB, Recommended 16GB
- **Storage**: At least 5GB free space for Docker images and processing
- **Network**: Internet access for initial setup (Docker image building)

### Software
- **Docker**: Version 20.0 or higher
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Platform**: Must support linux/amd64 containers

## Pre-Deployment Setup

### 1. Verify Docker Installation

```bash
# Check Docker version
docker --version

# Test Docker functionality
docker run hello-world

# Verify platform support
docker buildx ls
```

### 2. Clone/Download Project

```bash
# If using git
git clone <repository-url>
cd adobe-hackathon-challenge

# Or extract from archive
unzip adobe-hackathon-challenge.zip
cd adobe-hackathon-challenge
```

### 3. Verify Project Structure

```
├── README.md
├── round1a/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src/pdf_outline_extractor.py
│   └── README.md
├── round1b/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src/persona_intelligence.py
│   └── README.md
├── samples/
├── docs/
└── build_all.sh
```

## Deployment Steps

### Option 1: Automated Build (Recommended)

```bash
# Make build script executable (Linux/macOS)
chmod +x build_all.sh

# Run automated build
./build_all.sh

# For Windows
build_all.bat
```

### Option 2: Manual Build

#### Round 1A - PDF Outline Extractor

```bash
cd round1a
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
cd ..
```

#### Round 1B - Persona Intelligence

```bash
cd round1b
docker build --platform linux/amd64 -t persona-intelligence:latest .
cd ..
```

### 3. Verify Deployment

```bash
# List built images
docker images | grep -E "(pdf-outline-extractor|persona-intelligence)"

# Expected output:
# pdf-outline-extractor    latest    <image-id>    <time>    <size>
# persona-intelligence     latest    <image-id>    <time>    <size>
```

## Running the Solutions

### Round 1A - PDF Outline Extraction

```bash
# Create input/output directories
mkdir -p input output

# Place PDF files in input directory
cp your-pdfs/*.pdf input/

# Run extraction
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest

# Check results
ls output/
```

### Round 1B - Persona-Driven Intelligence

```bash
# Create input/output directories
mkdir -p input_1b output_1b

# Create configuration file
cat > input_1b/config.json << EOF
{
  "documents": [
    "/app/input/doc1.pdf",
    "/app/input/doc2.pdf"
  ],
  "persona": "Your persona description",
  "job_to_be_done": "Your job description"
}
EOF

# Place PDF files in input directory
cp your-pdfs/*.pdf input_1b/

# Run intelligence analysis
docker run --rm \
  -v $(pwd)/input_1b:/app/input \
  -v $(pwd)/output_1b:/app/output \
  --network none \
  persona-intelligence:latest

# Check results
cat output_1b/challenge1b_output.json
```

## Production Deployment Considerations

### 1. Resource Allocation

```bash
# Run with resource limits
docker run --rm \
  --memory=2g \
  --cpus=2 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
```

### 2. Batch Processing

```bash
# Process multiple batches
for batch in batch1 batch2 batch3; do
  docker run --rm \
    -v $(pwd)/$batch:/app/input \
    -v $(pwd)/output_$batch:/app/output \
    --network none \
    pdf-outline-extractor:latest
done
```

### 3. Monitoring and Logging

```bash
# Run with logging
docker run --rm \
  --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
```

## Troubleshooting

### Common Issues

1. **Platform Architecture Mismatch**
   ```bash
   # Force AMD64 platform
   docker build --platform linux/amd64 -t image-name .
   ```

2. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER input output
   chmod -R 755 input output
   ```

3. **Memory Issues**
   ```bash
   # Increase Docker memory limit
   # Docker Desktop: Settings > Resources > Memory
   # Or run with memory limit
   docker run --memory=4g ...
   ```

4. **Network Connectivity During Build**
   ```bash
   # Check internet connection
   ping google.com
   
   # Use different package index if needed
   docker build --build-arg PIP_INDEX_URL=https://pypi.org/simple/ ...
   ```

### Debug Commands

```bash
# Check container logs
docker logs <container-name>

# Run container interactively
docker run -it --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  pdf-outline-extractor:latest /bin/bash

# Inspect image
docker inspect pdf-outline-extractor:latest
```

## Performance Optimization

### 1. Docker Image Optimization

```bash
# Remove unused images
docker image prune

# Multi-stage builds (already implemented)
# Minimal base images (already using python:3.9-slim)
```

### 2. Processing Optimization

```bash
# Parallel processing for multiple files
docker run --rm \
  --cpus=4 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
```

### 3. Storage Optimization

```bash
# Use tmpfs for temporary files
docker run --rm \
  --tmpfs /tmp:rw,noexec,nosuid,size=1g \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
```

## Security Considerations

1. **Network Isolation**: Always use `--network none` in production
2. **File Permissions**: Ensure proper file permissions on mounted volumes
3. **Resource Limits**: Set appropriate CPU and memory limits
4. **Image Security**: Regularly update base images and dependencies

## Maintenance

### Regular Updates

```bash
# Update base images
docker pull python:3.9-slim

# Rebuild images
./build_all.sh

# Clean up old images
docker image prune -a
```

### Monitoring

```bash
# Monitor resource usage
docker stats

# Check disk usage
docker system df

# View container processes
docker ps -a
```
